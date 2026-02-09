use anyhow::{Context, Result};
use std::env;

#[derive(Debug, Clone)]
pub struct Config {
    pub redis_url: String,
    pub queue_name: String,
    pub database_url: String,
    pub qdrant_url: String,
    pub cohere_api_key: String,
    pub embedding_model: String,
    pub embedding_dimension: usize,
    pub embedding_distance: String,
}

impl Config {
    pub fn from_env() -> Result<Self> {
        Ok(Self {
            redis_url: env::var("REDIS_URL")
                .unwrap_or_else(|_| "redis://redis:6379".to_string()),
            queue_name: env::var("REDIS_QUEUE")
                .unwrap_or_else(|_| "candidate_jobs".to_string()),
            database_url: env::var("DATABASE_URL")
                .context("DATABASE_URL must be set")?,
            qdrant_url: env::var("QDRANT_URL")
                .context("QDRANT_URL must be set")?,
            cohere_api_key: env::var("COHERE_API_KEY")
                .context("COHERE_API_KEY must be set")?,
            embedding_model: env::var("EMBEDDING_MODEL")
                .unwrap_or_else(|_| "embed-multilingual-light-v3.0".to_string()),
            embedding_dimension: env::var("EMBEDDING_DIMENSION")
                .unwrap_or_else(|_| "384".to_string())
                .parse()
                .context("EMBEDDING_DIMENSION must be a valid number")?,
            embedding_distance: env::var("EMBEDDING_DISTANCE")
                .unwrap_or_else(|_| "Cosine".to_string()),
        })
    }
}
