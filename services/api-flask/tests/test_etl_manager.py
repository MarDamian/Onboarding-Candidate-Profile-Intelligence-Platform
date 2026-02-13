"""
Tests unitarios para ETLManager (servicio de gestión ETL).

¿Por qué testear ETLManager como unidad?
- Es la capa de lógica de negocio entre los endpoints y Redis/Pipeline
- Verifica que los payloads de jobs se construyen correctamente
- Valida que la cola Redis recibe el formato esperado por Worker Rust
- El worker Rust espera un JSON específico — si cambias el format, el job falla silenciosamente
"""

import pytest
from unittest.mock import patch, MagicMock
import json


class TestETLManager:
    """Tests unitarios para ETLManager."""

    @patch("app.services.etl_manager.redis.from_url")
    def test_trigger_sync_queues_job(self, mock_redis_url):
        """Debe encolar job con formato correcto en Redis."""
        mock_redis = MagicMock()
        mock_redis_url.return_value = mock_redis

        from app.services.etl_manager import ETLManager
        manager = ETLManager()
        
        result = manager.trigger_sync(requested_by="test_user")
        
        assert result["status"] == "job_queued"
        assert result["queue"] == "jobs:etl"
        assert result["job_payload"]["job_type"] == "etl_sync"
        assert result["job_payload"]["requested_by"] == "test_user"
        
        # Verificar que se llamó rpush
        mock_redis.rpush.assert_called_once()
        call_args = mock_redis.rpush.call_args
        assert call_args[0][0] == "jobs:etl"  # nombre de cola
        
        # Verificar que el payload es JSON válido
        payload = json.loads(call_args[0][1])
        assert payload["job_type"] == "etl_sync"

    @patch("app.services.etl_manager.redis.from_url")
    def test_trigger_sync_default_requested_by(self, mock_redis_url):
        """Debe usar 'api' como default para requested_by."""
        mock_redis = MagicMock()
        mock_redis_url.return_value = mock_redis

        from app.services.etl_manager import ETLManager
        manager = ETLManager()
        
        result = manager.trigger_sync()
        assert result["job_payload"]["requested_by"] == "api"

    @patch("app.services.etl_manager.run_pipeline")
    @patch("app.services.etl_manager.redis.from_url")
    def test_trigger_sync_direct(self, mock_redis_url, mock_pipeline):
        """Debe ejecutar pipeline directamente y retornar conteo."""
        mock_redis_url.return_value = MagicMock()
        mock_pipeline.return_value = 12

        from app.services.etl_manager import ETLManager
        manager = ETLManager()
        
        result = manager.trigger_sync_direct()
        assert result == 12
        mock_pipeline.assert_called_once()

    @patch("app.services.etl_manager.redis.from_url")
    def test_get_executions(self, mock_redis_url):
        """Debe retornar historial de ejecuciones desde Redis."""
        mock_redis = MagicMock()
        mock_redis.lrange.return_value = [
            json.dumps({"status": "success", "processed": 10}).encode(),
            json.dumps({"status": "error", "processed": 0}).encode()
        ]
        mock_redis_url.return_value = mock_redis

        from app.services.etl_manager import ETLManager
        manager = ETLManager()
        
        executions = manager.get_executions(limit=50)
        assert len(executions) == 2
        assert executions[0]["status"] == "success"

    @patch("app.services.etl_manager.redis.from_url")
    def test_get_execution_history_no_data(self, mock_redis_url):
        """Debe retornar status idle cuando no hay jobs."""
        mock_redis = MagicMock()
        mock_redis.get.return_value = None
        mock_redis_url.return_value = mock_redis

        from app.services.etl_manager import ETLManager
        manager = ETLManager()
        
        result = manager.get_execution_history()
        assert result["status"] == "idle"
