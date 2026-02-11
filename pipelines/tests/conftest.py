"""
Configuración compartida para tests de pipelines ETL.

¿Por qué aislamos tests de pipelines?
- Los pipelines son el corazón de la indexación de datos
- Dependen de PostgreSQL, Cohere API y Qdrant
- Mock completo de todas las dependencias externas
- Cada componente (Extract, Transform, Load) se testea de forma aislada
"""

import pytest
from unittest.mock import MagicMock, patch
import os

# Variables de entorno para tests
os.environ.setdefault("DATABASE_URL", "sqlite:///./test_pipeline.db")
os.environ.setdefault("QDRANT_URL", "http://localhost:6333")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")
os.environ.setdefault("COHERE_API_KEY", "test-key")
os.environ.setdefault("EMBEDDING_MODEL", "embed-multilingual-v3.0")
os.environ.setdefault("EMBEDDING_DIMENSION", "1024")
os.environ.setdefault("EMBEDDING_DISTANCE", "Cosine")


@pytest.fixture
def mock_candidate_row():
    """Simula una fila de candidato tal como la retorna SQLAlchemy."""
    row = MagicMock()
    row.id = 1
    row.name = "Ana García"
    row.summary = "Desarrolladora Python senior con 8 años de experiencia"
    row.skills = "Python, FastAPI, Docker, PostgreSQL"
    row.experience = "8 años en desarrollo backend"
    row.updated_at = "2026-02-10 12:00:00"
    return row


@pytest.fixture
def mock_candidate_rows():
    """Simula múltiples filas de candidatos."""
    rows = []
    for i in range(3):
        row = MagicMock()
        row.id = i + 1
        row.name = f"Candidato {i + 1}"
        row.summary = f"Resumen del candidato {i + 1}"
        row.skills = f"Skill{i}A, Skill{i}B"
        row.experience = f"{i + 2} años de experiencia"
        row.updated_at = f"2026-02-{10 + i} 12:00:00"
        rows.append(row)
    return rows


@pytest.fixture
def sample_embedding():
    """Vector de embedding de prueba (1024 dimensiones)."""
    return [0.1] * 1024
