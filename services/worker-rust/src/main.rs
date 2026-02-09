use anyhow::{Context, Result};
use redis::AsyncCommands;
use serde::{Deserialize, Serialize};
use tracing::{error, info};

#[derive(Debug, Serialize, Deserialize)]
struct JobPayload {
    job_type: String,
    requested_by: Option<String>,
    timestamp: Option<String>,
}

#[tokio::main]
async fn main() -> Result<()> {
    dotenvy::dotenv().ok();

    tracing_subscriber::fmt()
        .with_env_filter("info")
        .init();

    let redis_url =
        std::env::var("REDIS_URL").unwrap_or_else(|_| "redis://redis:6379".to_string());

    let queue_name = std::env::var("REDIS_QUEUE").unwrap_or_else(|_| "jobs:etl".to_string());

    info!("Rust Worker starting...");
    info!("Redis URL: {}", redis_url);
    info!("Queue: {}", queue_name);

    let client = redis::Client::open(redis_url).context("Failed to create Redis client")?;
    let mut conn = client
        .get_multiplexed_async_connection()
        .await
        .context("Failed to connect to Redis")?;

    loop {
        // BLPOP blocks until there is an item
        let result: Option<(String, String)> = conn
            .blpop(&queue_name, 0.0)
            .await
            .context("Redis BLPOP failed")?;

        if let Some((_queue, raw_payload)) = result {
            info!("Job received: {}", raw_payload);

            let parsed: Result<JobPayload> = serde_json::from_str(&raw_payload)
                .context("Failed to parse job JSON payload");

            match parsed {
                Ok(job) => {
                    info!("Job type: {}", job.job_type);
                    info!("Job processing not yet implemented");
                }
                Err(e) => {
                    error!("Invalid job payload: {:?}", e);
                }
            }
        }
    }
}

