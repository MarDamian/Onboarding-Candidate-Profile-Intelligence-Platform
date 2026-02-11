"""
Configuración compartida para tests de Flask (Admin API).

¿Por qué fixtures separados para Flask?
- Flask usa un patrón diferente (app factory con create_app)
- El test client de Flask no es el mismo que FastAPI (WSGI vs ASGI)
- Los servicios de Flask dependen de Redis, Qdrant y SQLAlchemy
- Todos los servicios externos se mockean para aislamiento

¿Por qué mockear Redis?
- Flask usa Redis para:
  1. Encolar jobs ETL (rpush a jobs:etl)
  2. Almacenar historial de ejecuciones
  3. Tracking de estado de jobs
- En tests, no queremos un Redis real
"""

import pytest
from unittest.mock import patch, MagicMock

# Mock de environment variables antes de importar la app
import os
os.environ.setdefault("DATABASE_URL", "sqlite:///./test_flask.db")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")
os.environ.setdefault("QDRANT_URL", "http://localhost:6333")
os.environ.setdefault("COHERE_API_KEY", "test-key")
os.environ.setdefault("EMBEDDING_MODEL", "embed-multilingual-v3.0")
os.environ.setdefault("EMBEDDING_DIMENSION", "1024")
os.environ.setdefault("EMBEDDING_DISTANCE", "Cosine")


@pytest.fixture
def app():
    """Crea instancia de la app Flask para testing."""
    from app import create_app
    app = create_app()
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    """Cliente HTTP de testing para Flask."""
    return app.test_client()


@pytest.fixture
def mock_redis():
    """Mock de conexión Redis."""
    with patch("redis.from_url") as mock:
        mock_instance = MagicMock()
        mock.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def mock_qdrant():
    """Mock del cliente Qdrant."""
    with patch("qdrant_client.QdrantClient") as mock:
        mock_instance = MagicMock()
        mock.return_value = mock_instance
        yield mock_instance
