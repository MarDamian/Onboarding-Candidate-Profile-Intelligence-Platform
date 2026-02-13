from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from sqlalchemy import create_engine, text
from pipelines.utils.retry import pipeline_retry
import os

class Loader:
    def __init__(self, qdrant_url, db_url):
        self.q_client =QdrantClient(url=qdrant_url)
        self.engine = create_engine(db_url)
        self.collection_name = "candidates"
        self.embedding_dimension = os.getenv("EMBEDDING_DIMENSION")
        self.embedding_distance = os.getenv("EMBEDDING_DISTANCE", "Cosine")
        
    @pipeline_retry
    def ensure_collection(self):
        collections = self.q_client.get_collections().collections
        if not any(c.name == self.collection_name for c in collections):
            distance_map = {
                "Cosine": Distance.COSINE,
                "Euclid": Distance.EUCLID,
                "Dot": Distance.DOT
            }
            self.q_client.create_collection(
                collection_name = self.collection_name,
                vectors_config = VectorParams(
                    size=self.embedding_dimension, 
                    distance=distance_map.get(self.embedding_distance, Distance.COSINE)
                )
            )
    
    @pipeline_retry
    def load_points(self, points_data):
        points = [PointStruct(id=p['id'], vector=p['vector'], payload=p['payload']) for p in points_data]
        self.q_client.upsert(collection_name=self.collection_name, points=points)

    def mark_as_indexed(self, candidate_ids):
        """Actualiza el timestamp en Postgres para garantizar idempotencia."""
        if not candidate_ids: return
        query = text("UPDATE candidates SET last_indexed_at = NOW() WHERE id IN :ids")
        with self.engine.connect() as conn:
            conn.execute(query, {"ids": tuple(candidate_ids)})
            conn.commit()