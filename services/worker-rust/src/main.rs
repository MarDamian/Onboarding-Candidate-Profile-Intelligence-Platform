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
        .with_env_filter("info")
        .init();

    // Load configuration
    let config = Config::from_env();
    
    info!("Rust Worker starting...");
    info!("Redis URL: {}", config.redis_url);
    info!("Queue: {}", config.queue_name);

    // Initialize Redis queue and processor
    let redis_queue = RedisQueue::new(&config.redis_url)?;
    let mut conn = redis_queue.connect().await?;
    let processor = JobProcessor::new();

    info!("Worker ready. Listening for jobs...");

    // Main event loop
    loop {
        match RedisQueue::pop_job(&mut conn, &config.queue_name).await {
            Ok(Some(payload)) => {
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

