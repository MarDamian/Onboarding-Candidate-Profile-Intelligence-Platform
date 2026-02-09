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
}
