mod config;
mod jobs;
mod queue;

use anyhow::Result;
use config::Config;
use jobs::JobProcessor;
use queue::RedisQueue;
use tracing::{error, info};

#[tokio::main]
async fn main() -> Result<()> {
    // Initialize environment and logging
    dotenvy::dotenv().ok();
    tracing_subscriber::fmt()
        .json()
        .with_env_filter("info")
        .init();

    // Load configuration
    let config = Config::from_env()?;
    
    info!("   Worker Rust starting...");
    info!("   Redis URL: {}", config.redis_url);
    info!("   Queue: {}", config.queue_name);
    info!("   Database URL: {}", mask_password(&config.database_url));
    info!("   Qdrant URL: {}", config.qdrant_url);
    info!("   Embedding Model: {}", config.embedding_model);
    info!("   Embedding Dimension: {}", config.embedding_dimension);

    // Initialize Redis queue
    let redis_queue = RedisQueue::new(&config.redis_url)?;
    let mut conn = redis_queue.connect().await?;
    
    // Initialize processor with all services
    info!("Initializing services...");
    let processor = JobProcessor::new(
        config.database_url.clone(),
        config.qdrant_url.clone(),
        config.cohere_api_key.clone(),
        config.embedding_model.clone(),
        config.embedding_dimension,
        config.embedding_distance.clone(),
    )
    .await?;

    info!("Worker ready. Listening for jobs on queue: {}", config.queue_name);

    // Main event loop
    loop {
        match RedisQueue::pop_job(&mut conn, &config.queue_name).await {
            Ok(Some(payload)) => {
                info!("Received job from queue");
                if let Err(e) = processor.process(&payload).await {
                    error!("Failed to process job: {:?}", e);
                }
            }
            Ok(None) => {
                // No job available (shouldn't happen with blocking pop)
                continue;
            }
            Err(e) => {
                error!("Error popping job from queue: {:?}", e);
                // Add a small delay before retrying to avoid busy loop
                tokio::time::sleep(tokio::time::Duration::from_secs(1)).await;
            }
        }
    }
}

/// Masks password in database URL for logging
fn mask_password(url: &str) -> String {
    if let Some(at_pos) = url.rfind('@') {
        if let Some(proto_end) = url.find("://") {
            let proto = &url[..proto_end + 3];
            let after_at = &url[at_pos..];
            return format!("{}***{}", proto, after_at);
        }
    }
    url.to_string()
}

