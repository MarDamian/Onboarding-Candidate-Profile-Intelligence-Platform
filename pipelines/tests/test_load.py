"""
Tests unitarios para el Loader del pipeline ETL.

¿Por qué testear el Loader?
- Es la etapa final y más crítica: escribe en Qdrant y actualiza PostgreSQL
- Un bug aquí puede dejar vectores huérfanos o candidatos marcados como indexados sin estarlo
- Verifica la lógica de ensure_collection (creación condicional)
- Valida que mark_as_indexed actualiza los timestamps para idempotencia
"""

import pytest
from unittest.mock import patch, MagicMock
import os


class TestLoader:
    """Tests para la clase Loader."""

    @patch.dict(os.environ, {"EMBEDDING_DIMENSION": "1024", "EMBEDDING_DISTANCE": "Cosine"})
    @patch("pipelines.etl.load.create_engine")
    @patch("pipelines.etl.load.QdrantClient")
    def test_ensure_collection_creates_when_missing(self, mock_qdrant_cls, mock_engine):
        """Debe crear colección en Qdrant si no existe."""
        mock_client = MagicMock()
        mock_client.get_collections.return_value.collections = []
        mock_qdrant_cls.return_value = mock_client

        from pipelines.etl.load import Loader
        loader = Loader("http://localhost:6333", "sqlite:///test.db")
        loader.ensure_collection()

        mock_client.create_collection.assert_called_once()

    @patch.dict(os.environ, {"EMBEDDING_DIMENSION": "1024", "EMBEDDING_DISTANCE": "Cosine"})
    @patch("pipelines.etl.load.create_engine")
    @patch("pipelines.etl.load.QdrantClient")
    def test_ensure_collection_skips_existing(self, mock_qdrant_cls, mock_engine):
        """No debe crear colección si ya existe."""
        mock_existing = MagicMock()
        mock_existing.name = "candidates"
        mock_client = MagicMock()
        mock_client.get_collections.return_value.collections = [mock_existing]
        mock_qdrant_cls.return_value = mock_client

        from pipelines.etl.load import Loader
        loader = Loader("http://localhost:6333", "sqlite:///test.db")
        loader.ensure_collection()

        mock_client.create_collection.assert_not_called()

    @patch.dict(os.environ, {"EMBEDDING_DIMENSION": "1024", "EMBEDDING_DISTANCE": "Cosine"})
    @patch("pipelines.etl.load.create_engine")
    @patch("pipelines.etl.load.QdrantClient")
    def test_load_points_upserts_to_qdrant(self, mock_qdrant_cls, mock_engine):
        """Debe hacer upsert de puntos en la colección de Qdrant."""
        mock_client = MagicMock()
        mock_qdrant_cls.return_value = mock_client

        from pipelines.etl.load import Loader
        loader = Loader("http://localhost:6333", "sqlite:///test.db")
        
        points_data = [
            {"id": 1, "vector": [0.1] * 1024, "payload": {"name": "Test"}},
            {"id": 2, "vector": [0.2] * 1024, "payload": {"name": "Test2"}},
        ]
        loader.load_points(points_data)

        mock_client.upsert.assert_called_once()
        call_kwargs = mock_client.upsert.call_args
        assert call_kwargs[1]["collection_name"] == "candidates"

    @patch.dict(os.environ, {"EMBEDDING_DIMENSION": "1024", "EMBEDDING_DISTANCE": "Cosine"})
    @patch("pipelines.etl.load.create_engine")
    @patch("pipelines.etl.load.QdrantClient")
    def test_mark_as_indexed_updates_postgres(self, mock_qdrant_cls, mock_engine):
        """Debe actualizar last_indexed_at en PostgreSQL."""
        mock_conn = MagicMock()
        mock_eng = MagicMock()
        mock_eng.connect.return_value.__enter__ = lambda s: mock_conn
        mock_eng.connect.return_value.__exit__ = MagicMock(return_value=False)
        mock_engine.return_value = mock_eng

        from pipelines.etl.load import Loader
        loader = Loader("http://localhost:6333", "sqlite:///test.db")
        loader.mark_as_indexed([1, 2, 3])

        mock_conn.execute.assert_called_once()
        mock_conn.commit.assert_called_once()

    @patch.dict(os.environ, {"EMBEDDING_DIMENSION": "1024", "EMBEDDING_DISTANCE": "Cosine"})
    @patch("pipelines.etl.load.create_engine")
    @patch("pipelines.etl.load.QdrantClient")
    def test_mark_as_indexed_skips_empty(self, mock_qdrant_cls, mock_engine):
        """No debe ejecutar query si no hay IDs para marcar."""
        mock_conn = MagicMock()
        mock_eng = MagicMock()
        mock_eng.connect.return_value.__enter__ = lambda s: mock_conn
        mock_eng.connect.return_value.__exit__ = MagicMock(return_value=False)
        mock_engine.return_value = mock_eng

        from pipelines.etl.load import Loader
        loader = Loader("http://localhost:6333", "sqlite:///test.db")
        loader.mark_as_indexed([])

        mock_conn.execute.assert_not_called()
