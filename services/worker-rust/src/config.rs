use std::env;

#[derive(Debug, Clone)]
pub struct Config {
    pub redis_url: String,
    pub queue_name: String,
}

impl Config {
    pub fn from_env() -> Self {
        Self {
            redis_url: env::var("REDIS_URL")
                .unwrap_or_else(|_| "redis://redis:6379".to_string()),
            queue_name: env::var("REDIS_QUEUE")
                .unwrap_or_else(|_| "jobs:etl".to_string()),
        }
    }
}
