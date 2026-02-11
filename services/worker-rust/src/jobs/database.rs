use anyhow::{Context, Result};
use tokio_postgres::{Client, NoTls};
use tokio::time::{timeout, Duration};
use tracing::{info, error};

#[derive(Debug, Clone)]
pub struct Candidate {
    pub id: i32,
    pub name: String,
    pub summary: String,
    pub skills: String,
    pub experience: String,
    pub updated_at: String,
}

pub struct DatabaseService {
    client: Client,
}

impl DatabaseService {
    pub async fn new(database_url: &str) -> Result<Self> {
        let (client, connection) = timeout(
            Duration::from_secs(10),
            tokio_postgres::connect(database_url, NoTls)
        )
        .await
        .context("Connection to PostgreSQL timed out")?
        .context("Failed to connect to PostgreSQL")?;

        // Maneja la conexión de la base de datos
        tokio::spawn(async move {
            if let Err(e) = connection.await {
                error!("PostgreSQL connection error: {}", e);
            }
        });

        info!("PostgreSQL connected successfully");
        Ok(Self { client })
    }

    /// Extrae candidatos que nunca se han indexado o que cambiaron después de indexarse
    pub async fn get_stale_candidates(&self) -> Result<Vec<Candidate>> {
        let query = "
            SELECT id, 
                   COALESCE(name, '') as name, 
                   COALESCE(summary, '') as summary, 
                   COALESCE(skills, '') as skills, 
                   COALESCE(experience, '') as experience, 
                   COALESCE(updated_at::text, '') as updated_at
            FROM candidates
            WHERE last_indexed_at IS NULL OR updated_at > last_indexed_at
        ";

        let rows = timeout(
            Duration::from_secs(10),
            self.client.query(query, &[])
        )
        .await
        .context("Query for stale candidates timed out")?
        .context("Failed to query stale candidates")?;

        let candidates: Vec<Candidate> = rows
            .iter()
            .map(|row| Candidate {
                id: row.get(0),
                name: row.get(1),
                summary: row.get(2),
                skills: row.get(3),
                experience: row.get(4),
                updated_at: row.get(5),
            })
            .collect();

        info!("Found {} stale candidates", candidates.len());
        Ok(candidates)
    }

    /// Marca candidatos como indexados actualizando last_indexed_at
    pub async fn mark_as_indexed(&self, candidate_ids: &[i32]) -> Result<()> {
        if candidate_ids.is_empty() {
            return Ok(());
        }

        let query = "UPDATE candidates SET last_indexed_at = NOW() WHERE id = ANY($1)";
        
        timeout(
            Duration::from_secs(10),
            self.client.execute(query, &[&candidate_ids])
        )
        .await
        .context("Updating last_indexed_at timed out")?
        .context("Failed to mark candidates as indexed")?;

        info!("Marked {} candidates as indexed", candidate_ids.len());
        Ok(())
    }
}
