use anyhow::{Context, Result};
use reqwest::Client;
use reqwest_middleware::{ClientBuilder, ClientWithMiddleware};
use reqwest_retry::{RetryTransientMiddleware, policies::ExponentialBackoff};
use serde::{Deserialize, Serialize};
use std::time::Duration;
use tracing::warn;

#[derive(Debug, Serialize)]
struct EmbedRequest {
    texts: Vec<String>,
    model: String,
    input_type: String,
    embedding_types: Vec<String>,
}

#[derive(Debug, Deserialize)]
struct EmbedResponse {
    embeddings: Embeddings,
}

#[derive(Debug, Deserialize)]
struct Embeddings {
    #[serde(rename = "float")]
    float_embeddings: Vec<Vec<f32>>,
}

pub struct EmbeddingsService {
    client: ClientWithMiddleware,
    api_key: String,
    model: String,
    expected_dimension: usize,
}

impl EmbeddingsService {
    pub fn new(api_key: String, model: String, dimension: usize) -> Self {
        let retry_policy = ExponentialBackoff::builder().build_with_max_retries(3);
        let client = ClientBuilder::new(
            Client::builder()
                .timeout(Duration::from_secs(30))
                .build()
                .expect("Failed to create reqwest client")
        )
        .with(RetryTransientMiddleware::new_with_policy(retry_policy))
        .build();

        Self {
            client,
            api_key,
            model,
            expected_dimension: dimension,
        }
    }

    /// Genera embedding para un texto dado
    #[allow(dead_code)]
    pub async fn generate_embedding(&self, text: &str) -> Result<Vec<f32>> {
        let request = EmbedRequest {
            texts: vec![text.to_string()],
            model: self.model.clone(),
            input_type: "search_document".to_string(),
            embedding_types: vec!["float".to_string()],
        };

        let response = self.client
            .post("https://api.cohere.ai/v1/embed")
            .header("Authorization", format!("Bearer {}", self.api_key))
            .header("Content-Type", "application/json")
            .json(&request)
            .send()
            .await
            .context("Failed to send request to Cohere API")?;

        if !response.status().is_success() {
            let status = response.status();
            let body = response.text().await.unwrap_or_default();
            anyhow::bail!("Cohere API error ({}): {}", status, body);
        }

        let embed_response: EmbedResponse = response
            .json()
            .await
            .context("Failed to parse Cohere API response")?;

        let vector = embed_response
            .embeddings
            .float_embeddings
            .into_iter()
            .next()
            .context("No embeddings returned from Cohere API")?;

        // Validar dimensión
        if vector.len() != self.expected_dimension {
            warn!(
                "Embedding dimension mismatch: expected {}, got {}",
                self.expected_dimension,
                vector.len()
            );
        }

        Ok(vector)
    }

    /// Genera embeddings para múltiples textos (batch)
    pub async fn generate_embeddings_batch(&self, texts: Vec<String>) -> Result<Vec<Vec<f32>>> {
        if texts.is_empty() {
            return Ok(vec![]);
        }

        let request = EmbedRequest {
            texts,
            model: self.model.clone(),
            input_type: "search_document".to_string(),
            embedding_types: vec!["float".to_string()],
        };

        let response = self.client
            .post("https://api.cohere.ai/v1/embed")
            .header("Authorization", format!("Bearer {}", self.api_key))
            .header("Content-Type", "application/json")
            .json(&request)
            .send()
            .await
            .context("Failed to send batch request to Cohere API")?;

        if !response.status().is_success() {
            let status = response.status();
            let body = response.text().await.unwrap_or_default();
            anyhow::bail!("Cohere API error ({}): {}", status, body);
        }

        let embed_response: EmbedResponse = response
            .json()
            .await
            .context("Failed to parse Cohere API response")?;

        Ok(embed_response.embeddings.float_embeddings)
    }
}
