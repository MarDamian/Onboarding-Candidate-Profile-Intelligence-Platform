use anyhow::{Context, Result};
use redis::{aio::MultiplexedConnection, AsyncCommands, Client};
use tracing::info;

pub struct RedisQueue {
    client: Client,
}

impl RedisQueue {
    pub fn new(redis_url: &str) -> Result<Self> {
        let client = Client::open(redis_url).context("Failed to create Redis client")?;
        Ok(Self { client })
    }

    pub async fn connect(&self) -> Result<MultiplexedConnection> {
        self.client
            .get_multiplexed_async_connection()
            .await
            .context("Failed to connect to Redis")
    }

    pub async fn pop_job(
        conn: &mut MultiplexedConnection,
        queue_name: &str,
    ) -> Result<Option<String>> {
        let result: Option<(String, String)> = conn
            .blpop(queue_name, 0.0)
            .await
            .context("Redis BLPOP failed")?;

        if let Some((_queue, payload)) = result {
            info!("Job received from queue: {}", queue_name);
            Ok(Some(payload))
        } else {
            Ok(None)
        }
    }
}
