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
    """Tests para POST /v1/admin/qdrant/reindex (asíncrono via Worker Rust)"""

    @patch("app.api.qdrant_routes.etl_service")
    def test_reindex_success(self, mock_etl_service, client):
        """Debe encolar un full_reindex y retornar 202 Accepted."""
        mock_etl_service.trigger_full_reindex.return_value = {
            "status": "job_queued",
            "queue": "jobs:etl",
            "job_payload": {"job_type": "full_reindex"}
        }

        response = client.post("/v1/admin/qdrant/reindex")
        assert response.status_code == 202
        data = response.get_json()
        assert data["status"] == "accepted"
        mock_etl_service.trigger_full_reindex.assert_called_once_with(requested_by="flask:reindex")

    @patch("app.api.qdrant_routes.etl_service")
    def test_reindex_pipeline_error(self, mock_etl_service, client):
        """Debe retornar 500 cuando el encolamiento falla."""
        mock_etl_service.trigger_full_reindex.side_effect = Exception("Redis connection error")

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
    """Tests para POST /v1/admin/qdrant/rebuild (asíncrono via Worker Rust)"""

    @patch("app.api.qdrant_routes.etl_service")
    def test_rebuild_success(self, mock_etl_service, client):
        """Debe encolar un full_reindex y retornar 202 Accepted."""
        mock_etl_service.trigger_full_reindex.return_value = {
            "status": "job_queued",
            "queue": "jobs:etl",
            "job_payload": {"job_type": "full_reindex"}
        }

        response = client.post("/v1/admin/qdrant/rebuild")
        assert response.status_code == 202
        data = response.get_json()
        assert data["status"] == "accepted"
        mock_etl_service.trigger_full_reindex.assert_called_once_with(requested_by="flask:rebuild")

    @patch("app.api.qdrant_routes.etl_service")
    def test_rebuild_error(self, mock_etl_service, client):
        """Debe retornar 500 cuando el encolamiento falla."""
        mock_etl_service.trigger_full_reindex.side_effect = Exception("Redis unreachable")

        response = client.post("/v1/admin/qdrant/rebuild")
        assert response.status_code == 500
