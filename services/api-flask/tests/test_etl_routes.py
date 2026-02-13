"""
Tests para los endpoints de ETL (Admin API - Flask).

¿Por qué testear las rutas ETL?
- Son operaciones administrativas críticas que afectan el pipeline de datos
- Un error en ETL puede dejar candidatos sin indexar (invisibles en búsqueda)
- Validamos que los jobs se encolan correctamente en Redis
- Verificamos manejo de errores cuando Redis o el pipeline fallan

Cobertura:
- POST /v1/admin/etl/sync → encola job async en Redis
- POST /v1/admin/etl/sync/direct → ejecución síncrona (legacy)
- GET /v1/admin/etl/status → historial de ejecuciones
"""

import pytest
from unittest.mock import patch, MagicMock
import json


class TestHealthCheck:
    """Tests para GET /health"""

    def test_health_returns_200(self, client):
        """Debe retornar status healthy."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.get_json()
        assert data["status"] == "healthy"


class TestETLSync:
    """Tests para POST /v1/admin/etl/sync"""

    @patch("app.api.etl_routes.etl_service")
    def test_sync_queues_job(self, mock_etl, client):
        """Debe encolar job ETL y retornar 202 Accepted."""
        mock_etl.trigger_sync.return_value = {
            "status": "job_queued",
            "queue": "jobs:etl",
            "job_payload": {
                "job_type": "etl_sync",
                "requested_by": "api",
                "timestamp": "2026-02-11T00:00:00Z"
            }
        }

        response = client.post("/v1/admin/etl/sync",
                              data=json.dumps({"requested_by": "test_user"}),
                              content_type="application/json")
        
        assert response.status_code == 202
        data = response.get_json()
        assert data["status"] == "success"
        assert data["message"] == "ETL job queued successfully"

    @patch("app.api.etl_routes.etl_service")
    def test_sync_without_body(self, mock_etl, client):
        """Debe funcionar sin body (usa default 'api')."""
        mock_etl.trigger_sync.return_value = {
            "status": "job_queued",
            "queue": "jobs:etl",
            "job_payload": {}
        }

        response = client.post("/v1/admin/etl/sync")
        assert response.status_code == 202

    @patch("app.api.etl_routes.etl_service")
    def test_sync_error_returns_500(self, mock_etl, client):
        """Debe retornar 500 cuando el ETL falla."""
        mock_etl.trigger_sync.side_effect = Exception("Redis connection refused")

        response = client.post("/v1/admin/etl/sync")
        assert response.status_code == 500
        assert "error" in response.get_json()


class TestETLSyncDirect:
    """Tests para POST /v1/admin/etl/sync/direct"""

    @patch("app.api.etl_routes.etl_service")
    def test_sync_direct_success(self, mock_etl, client):
        """Debe ejecutar ETL síncrono y retornar registros procesados."""
        mock_etl.trigger_sync_direct.return_value = 15

        response = client.post("/v1/admin/etl/sync/direct")
        assert response.status_code == 200
        data = response.get_json()
        assert data["status"] == "success"
        assert data["records_processed"] == 15

    @patch("app.api.etl_routes.etl_service")
    def test_sync_direct_error(self, mock_etl, client):
        """Debe retornar 500 cuando la ejecución síncrona falla."""
        mock_etl.trigger_sync_direct.side_effect = Exception("DB connection failed")

        response = client.post("/v1/admin/etl/sync/direct")
        assert response.status_code == 500


class TestETLStatus:
    """Tests para GET /v1/admin/etl/status"""

    @patch("app.api.etl_routes.etl_service")
    def test_status_returns_executions(self, mock_etl, client):
        """Debe retornar historial de ejecuciones."""
        mock_etl.get_executions.return_value = [
            {"timestamp": "2026-02-11T10:00:00", "status": "success", "processed": 20},
            {"timestamp": "2026-02-11T09:00:00", "status": "error", "processed": 0}
        ]

        response = client.get("/v1/admin/etl/status")
        assert response.status_code == 200
        data = response.get_json()
        assert len(data["executions"]) == 2

    @patch("app.api.etl_routes.etl_service")
    def test_status_empty_history(self, mock_etl, client):
        """Debe retornar lista vacía cuando no hay ejecuciones."""
        mock_etl.get_executions.return_value = []

        response = client.get("/v1/admin/etl/status")
        assert response.status_code == 200
        assert response.get_json()["executions"] == []

    @patch("app.api.etl_routes.etl_service")
    def test_status_error(self, mock_etl, client):
        """Debe retornar 500 cuando Redis no está accesible."""
        mock_etl.get_executions.side_effect = Exception("Redis timeout")

        response = client.get("/v1/admin/etl/status")
        assert response.status_code == 500
