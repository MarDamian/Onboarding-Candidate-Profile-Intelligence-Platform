use anyhow::{Context, Result};
use qdrant_client::{
    client::QdrantClient,
    qdrant::{
        vectors_config::Config, CreateCollection, Distance, PointStruct,
        VectorParams, VectorsConfig,
    },
};
use serde_json::Map;
use std::collections::HashMap;
use std::time::Duration;
use tracing::info;

pub struct QdrantService {
    client: QdrantClient,
    collection_name: String,
    dimension: u64,
    distance: Distance,
}

impl QdrantService {
    pub async fn new(
        url: &str,
        collection_name: String,
        dimension: u64,
        distance_metric: &str,
    ) -> Result<Self> {
        let mut config = QdrantClient::from_url(url);
        config.set_timeout(Duration::from_secs(10));
        config.set_connect_timeout(Duration::from_secs(5));
        let client = config
            .build()
            .context("Failed to create Qdrant client")?;

        let distance = match distance_metric {
            "Cosine" => Distance::Cosine,
            "Euclid" => Distance::Euclid,
            "Dot" => Distance::Dot,
            _ => Distance::Cosine,
        };

        info!("Qdrant client connected to: {}", url);

        Ok(Self {
            client,
            collection_name,
            dimension,
            distance,
        })
    }

    /// Asegura que la colección existe, creándola si es necesario
    pub async fn ensure_collection(&self) -> Result<()> {
        let collections = self
            .client
            .list_collections()
            .await
            .context("Failed to list Qdrant collections")?;

        let exists = collections
            .collections
            .iter()
            .any(|c| c.name == self.collection_name);

        if !exists {
            info!("Creating collection: {}", self.collection_name);

            self.client
                .create_collection(&CreateCollection {
                    collection_name: self.collection_name.clone(),
                    vectors_config: Some(VectorsConfig {
                        config: Some(Config::Params(VectorParams {
                            size: self.dimension,
                            distance: self.distance.into(),
                            ..Default::default()
                        })),
                    }),
                    ..Default::default()
                })
                .await
                .context("Failed to create Qdrant collection")?;

            info!("Collection created successfully: {}", self.collection_name);
        } else {
            info!("Collection already exists: {}", self.collection_name);
        }

        Ok(())
    }

    /// Carga puntos en la colección de Qdrant
    pub async fn load_points(
        &self,
        points_data: Vec<(i32, Vec<f32>, HashMap<String, String>)>,
    ) -> Result<()> {
        if points_data.is_empty() {
            return Ok(());
        }

        let points: Vec<PointStruct> = points_data
            .into_iter()
            .map(|(id, vector, payload)| {
                let mut payload_map = Map::new();
                for (k, v) in payload {
                    payload_map.insert(k, serde_json::json!(v));
                }

                PointStruct::new(id as u64, vector, payload_map)
            })
            .collect();

        let count = points.len();

        self.client
            .upsert_points_blocking(&self.collection_name, None, points, None)
            .await
            .context("Failed to upsert points to Qdrant")?;

        info!("Upserted {} points to Qdrant", count);
        Ok(())
    }
}
