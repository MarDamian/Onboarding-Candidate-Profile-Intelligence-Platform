use super::database::DatabaseService;
use super::embeddings::EmbeddingsService;
use super::qdrant_service::QdrantService;
use super::types::{JobPayload, JobType};
use anyhow::{Context, Result};
use std::collections::HashMap;
use tracing::{info, warn};

pub struct JobProcessor {
    db: DatabaseService,
    embeddings: EmbeddingsService,
    qdrant: QdrantService,
}

impl JobProcessor {
    pub async fn new(
        database_url: String,
        qdrant_url: String,
        cohere_api_key: String,
        embedding_model: String,
        embedding_dimension: usize,
        embedding_distance: String,
    ) -> Result<Self> {
        let db = DatabaseService::new(&database_url)
            .await
            .context("Failed to initialize database service")?;

        let embeddings = EmbeddingsService::new(cohere_api_key, embedding_model, embedding_dimension);

        let qdrant = QdrantService::new(
            &qdrant_url,
            "candidates".to_string(),
            embedding_dimension as u64,
            &embedding_distance,
        )
        .await
        .context("Failed to initialize Qdrant service")?;

        info!("JobProcessor initialized successfully");

        Ok(Self {
            db,
            embeddings,
            qdrant,
        })
    }

    pub async fn process(&self, payload: &str) -> Result<()> {
        let job: JobPayload = serde_json::from_str(payload)
            .context("Failed to parse job JSON payload")?;

        info!("Processing job: {:?}", job);

        match job.get_job_type() {
            JobType::EtlSync => {
                info!("Job type: ETL Sync");
                self.process_etl_sync(&job).await?;
            }
            JobType::EmbeddingBatch => {
                info!("Job type: Embedding Batch");
                self.process_embedding_batch(&job).await?;
            }
            JobType::SingleIndex => {
                info!("Job type: Single Index");
                self.process_single_index(&job).await?;
            }
            JobType::DeletePoint => {
                info!("Job type: Delete Point");
                self.process_delete_point(&job).await?;
            }
            JobType::FullReindex => {
                info!("Job type: Full Reindex");
                self.process_full_reindex(&job).await?;
            }
            JobType::Unknown(job_type) => {
                warn!("Unknown job type: {}", job_type);
            }
        }

        Ok(())
    }

    async fn process_etl_sync(&self, job: &JobPayload) -> Result<()> {
        info!("Starting ETL Sync job");
        info!("Requested by: {:?}", job.requested_by);
        info!("Timestamp: {:?}", job.timestamp);

        // 1. Ensure Qdrant collection exists
        info!("Ensuring Qdrant collection exists...");
        self.qdrant
            .ensure_collection()
            .await
            .context("Failed to ensure Qdrant collection")?;

        // 2. Extract: Get stale candidates from database
        info!("Extracting stale candidates from database...");
        let candidates = self
            .db
            .get_stale_candidates()
            .await
            .context("Failed to get stale candidates")?;

        if candidates.is_empty() {
            info!("No stale candidates to process");
            return Ok(());
        }

        info!("Found {} candidates to process", candidates.len());

        // 3. Transform: Generate embeddings in batch
        info!("Generating embeddings (batch)...");

        // Prepare context texts for all candidates
        let context_texts: Vec<String> = candidates
            .iter()
            .map(|c| {
                format!(
                    "{} | {} | Skills: {} | Experience: {}",
                    c.name, c.summary, c.skills, c.experience
                )
            })
            .collect();

        // Generate all embeddings in a single API call
        let vectors = self
            .embeddings
            .generate_embeddings_batch(context_texts.clone())
            .await
            .context("Failed to generate embeddings batch")?;

        info!("   Generated {} embeddings in batch", vectors.len());

        // Build points data combining candidates + vectors + payloads
        let mut points_data = Vec::new();
        for (i, candidate) in candidates.iter().enumerate() {
            let mut payload = HashMap::new();
            payload.insert("name".to_string(), candidate.name.clone());
            payload.insert("text_content".to_string(), context_texts[i].clone());
            payload.insert("updated_at".to_string(), candidate.updated_at.clone());

            points_data.push((candidate.id, vectors[i].clone(), payload));
        }

        // 4. Load: Upsert points to Qdrant
        info!("Loading {} points to Qdrant...", points_data.len());
        self.qdrant
            .load_points(points_data)
            .await
            .context("Failed to load points to Qdrant")?;

        // 5. Mark candidates as indexed
        info!("Marking candidates as indexed in database...");
        let candidate_ids: Vec<i32> = candidates.iter().map(|c| c.id).collect();
        self.db
            .mark_as_indexed(&candidate_ids)
            .await
            .context("Failed to mark candidates as indexed")?;

        info!("   ETL Sync completed successfully");
        info!("   Processed: {} candidates", candidates.len());

        Ok(())
    }

    async fn process_embedding_batch(&self, job: &JobPayload) -> Result<()> {
        info!("   Starting Embedding Batch job");
        info!("   Requested by: {:?}", job.requested_by);
        info!("   Timestamp: {:?}", job.timestamp);

        // Similar to ETL sync but could have different logic
        // For now, use the same implementation
        self.process_etl_sync(job).await
    }

    /// Indexa un único candidato por ID (para create/update automático)
    async fn process_single_index(&self, job: &JobPayload) -> Result<()> {
        let candidate_id = job.candidate_id.context(
            "single_index job requires candidate_id"
        )?;

        info!("Indexing single candidate: {}", candidate_id);

        // 1. Ensure collection exists
        self.qdrant.ensure_collection().await
            .context("Failed to ensure Qdrant collection")?;

        // 2. Get candidate from database
        let candidate = self.db.get_candidate_by_id(candidate_id).await
            .context("Failed to get candidate from database")?;

        let candidate = match candidate {
            Some(c) => c,
            None => {
                warn!("Candidate {} not found in database, skipping", candidate_id);
                return Ok(());
            }
        };

        // 3. Generate embedding
        let context_text = format!(
            "{} | {} | Skills: {} | Experience: {}",
            candidate.name, candidate.summary, candidate.skills, candidate.experience
        );

        let vectors = self.embeddings
            .generate_embeddings_batch(vec![context_text.clone()])
            .await
            .context("Failed to generate embedding for single candidate")?;

        let vector = vectors.into_iter().next()
            .context("No embedding returned for candidate")?;

        // 4. Upsert to Qdrant
        let mut payload = HashMap::new();
        payload.insert("name".to_string(), candidate.name.clone());
        payload.insert("text_content".to_string(), context_text);
        payload.insert("updated_at".to_string(), candidate.updated_at.clone());

        self.qdrant.load_points(vec![(candidate.id, vector, payload)]).await
            .context("Failed to upsert single point to Qdrant")?;

        // 5. Mark as indexed
        self.db.mark_as_indexed(&[candidate.id]).await
            .context("Failed to mark candidate as indexed")?;

        info!("Single candidate {} indexed successfully", candidate_id);
        Ok(())
    }

    /// Elimina un punto de Qdrant (para delete automático)
    async fn process_delete_point(&self, job: &JobPayload) -> Result<()> {
        let candidate_id = job.candidate_id.context(
            "delete_point job requires candidate_id"
        )?;

        info!("Deleting point for candidate: {}", candidate_id);

        self.qdrant.delete_point(candidate_id).await
            .context("Failed to delete point from Qdrant")?;

        info!("Point for candidate {} deleted successfully", candidate_id);
        Ok(())
    }

    /// Full reindex: resetea todos los candidatos y re-procesa todo via Rust 
    async fn process_full_reindex(&self, job: &JobPayload) -> Result<()> {
        info!("Starting full reindex");
        info!("Requested by: {:?}", job.requested_by);

        // 1. Clear all points from Qdrant
        self.qdrant.clear_all_points().await
            .context("Failed to clear Qdrant collection")?;

        // 2. Reset all last_indexed_at in database
        let reset_count = self.db.reset_all_indexed().await
            .context("Failed to reset indexed status")?;
        info!("Reset {} candidates for reindexing", reset_count);

        // 3. Run the standard ETL sync (will pick up all candidates)
        self.process_etl_sync(job).await
            .context("Failed to process ETL sync during full reindex")?;

        info!("Full reindex completed successfully");
        Ok(())
    }
}
