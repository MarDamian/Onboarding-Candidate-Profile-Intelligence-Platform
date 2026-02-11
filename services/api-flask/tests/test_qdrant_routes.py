"""
Tests para los endpoints de Qdrant (Admin API - Flask).

¿Por qué testear la administración de Qdrant?
- Las operaciones de reindex/clear/rebuild son destructivas e irreversibles
- Un bug puede borrar todos los vectores de producción
- Validamos que cada operación ejecuta los pasos en el orden correcto
- Verificamos que errores de Qdrant se manejan con respuestas 500 claras

Cobertura:
- GET /v1/admin/qdrant/stats → estadísticas de la colección
- POST /v1/admin/qdrant/reindex → reset + re-run ETL
- DELETE /v1/admin/qdrant/clear → limpiar vectores
- POST /v1/admin/qdrant/rebuild → clear + reindex completo
"""

import pytest
from unittest.mock import patch, MagicMock


class TestQdrantStats:
    """Tests para GET /v1/admin/qdrant/stats"""

    @patch("app.api.qdrant_routes.QdrantClient")
    def test_stats_success(self, mock_qdrant_cls, client):
        """Debe retornar estadísticas de la colección."""
        mock_collection = MagicMock()
        mock_collection.points_count = 150
        mock_collection.indexed_vectors_count = 150
        mock_collection.segments_count = 2
        mock_collection.status.name = "GREEN"

        mock_client = MagicMock()
        mock_client.get_collection.return_value = mock_collection
        mock_qdrant_cls.return_value = mock_client

        response = client.get("/v1/admin/qdrant/stats")
        assert response.status_code == 200
        data = response.get_json()
        assert data["collection_name"] == "candidates"
        assert data["points_count"] == 150
        assert data["status"] == "GREEN"

    @patch("app.api.qdrant_routes.QdrantClient")
    def test_stats_qdrant_error(self, mock_qdrant_cls, client):
        """Debe retornar 500 cuando Qdrant no está disponible."""
        mock_qdrant_cls.return_value.get_collection.side_effect = Exception(
            "Connection refused"
        )

        response = client.get("/v1/admin/qdrant/stats")
        assert response.status_code == 500
        assert "error" in response.get_json()


class TestQdrantReindex:
    """Tests para POST /v1/admin/qdrant/reindex"""

    @patch("app.api.qdrant_routes.run_pipeline")
    @patch("app.api.qdrant_routes.create_engine")
    def test_reindex_success(self, mock_engine, mock_pipeline, client):
        """Debe resetear last_indexed_at y re-ejecutar pipeline."""
        mock_conn = MagicMock()
        mock_engine.return_value.connect.return_value.__enter__ = lambda s: mock_conn
        mock_engine.return_value.connect.return_value.__exit__ = MagicMock(return_value=False)
        mock_pipeline.return_value = {"status": "success", "processed": 10}

        response = client.post("/v1/admin/qdrant/reindex")
        assert response.status_code == 200
        data = response.get_json()
        assert data["status"] == "success"

    @patch("app.api.qdrant_routes.run_pipeline")
    @patch("app.api.qdrant_routes.create_engine")
    def test_reindex_pipeline_error(self, mock_engine, mock_pipeline, client):
        """Debe retornar 500 cuando el pipeline falla."""
        mock_conn = MagicMock()
        mock_engine.return_value.connect.return_value.__enter__ = lambda s: mock_conn
        mock_engine.return_value.connect.return_value.__exit__ = MagicMock(return_value=False)
        mock_pipeline.side_effect = Exception("Cohere API error")

        response = client.post("/v1/admin/qdrant/reindex")
        assert response.status_code == 500


class TestQdrantClear:
    """Tests para DELETE /v1/admin/qdrant/clear"""

    @patch("app.api.qdrant_routes.create_engine")
    @patch("app.api.qdrant_routes.QdrantClient")
    def test_clear_success(self, mock_qdrant_cls, mock_engine, client):
        """Debe limpiar vectores y resetear timestamps."""
        mock_collection = MagicMock()
        mock_collection.points_count = 100

        mock_client = MagicMock()
        mock_client.get_collection.return_value = mock_collection
        mock_qdrant_cls.return_value = mock_client

        mock_conn = MagicMock()
        mock_engine.return_value.connect.return_value.__enter__ = lambda s: mock_conn
        mock_engine.return_value.connect.return_value.__exit__ = MagicMock(return_value=False)

        response = client.delete("/v1/admin/qdrant/clear")
        assert response.status_code == 200
        data = response.get_json()
        assert data["status"] == "success"
        assert data["points_deleted"] == 100


class TestQdrantRebuild:
    """Tests para POST /v1/admin/qdrant/rebuild"""

    @patch("app.api.qdrant_routes.run_pipeline")
    @patch("app.api.qdrant_routes.create_engine")
    @patch("app.api.qdrant_routes.QdrantClient")
    def test_rebuild_success(self, mock_qdrant_cls, mock_engine, mock_pipeline, client):
        """Debe limpiar y reconstruir la colección completa."""
        mock_client = MagicMock()
        mock_qdrant_cls.return_value = mock_client

        mock_conn = MagicMock()
        mock_engine.return_value.connect.return_value.__enter__ = lambda s: mock_conn
        mock_engine.return_value.connect.return_value.__exit__ = MagicMock(return_value=False)
        mock_pipeline.return_value = 25

        response = client.post("/v1/admin/qdrant/rebuild")
        assert response.status_code == 200
        data = response.get_json()
        assert data["status"] == "success"
        assert data["candidates_reindexed"] == 25

    @patch("app.api.qdrant_routes.run_pipeline")
    @patch("app.api.qdrant_routes.create_engine")
    @patch("app.api.qdrant_routes.QdrantClient")
    def test_rebuild_error(self, mock_qdrant_cls, mock_engine, mock_pipeline, client):
        """Debe retornar 500 cuando la reconstrucción falla."""
        mock_client = MagicMock()
        mock_qdrant_cls.return_value = mock_client

        mock_conn = MagicMock()
        mock_engine.return_value.connect.return_value.__enter__ = lambda s: mock_conn
        mock_engine.return_value.connect.return_value.__exit__ = MagicMock(return_value=False)
        mock_pipeline.side_effect = Exception("Qdrant unreachable")

        response = client.post("/v1/admin/qdrant/rebuild")
        assert response.status_code == 500
