use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct JobPayload {
    pub job_type: String,
    pub requested_by: Option<String>,
    pub timestamp: Option<String>,
}

#[derive(Debug, Clone, PartialEq)]
pub enum JobType {
    EtlSync,
    EmbeddingBatch,
    Unknown(String),
}

impl From<&str> for JobType {
    fn from(s: &str) -> Self {
        match s {
            "etl_sync" => JobType::EtlSync,
            "embedding_batch" => JobType::EmbeddingBatch,
            unknown => JobType::Unknown(unknown.to_string()),
        }
    }
}

impl JobPayload {
    pub fn get_job_type(&self) -> JobType {
        JobType::from(self.job_type.as_str())
    }
}
