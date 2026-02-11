"""
Configuración compartida para tests de FastAPI.

¿Por qué conftest.py?
- Centraliza fixtures reutilizables (DB, client HTTP, datos de prueba)
- pytest lo detecta automáticamente sin imports explícitos
- Cada test recibe una DB limpia (SQLite in-memory) para aislamiento total

¿Por qué SQLite in-memory en lugar de PostgreSQL?
- No requiere infraestructura externa (Docker, servicios)
- Cada test corre en milisegundos
- Garantiza aislamiento: cada test parte de una DB vacía
- Ideal para CI donde no hay servicios externos disponibles
"""

import pytest
from unittest.mock import patch, MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

# Mock de settings ANTES de importar módulos que lo usen
mock_settings = MagicMock()
mock_settings.DATABASE_URL = "sqlite:///./test.db"
mock_settings.QDRANT_URL = "http://localhost:6333"
mock_settings.COHERE_API_KEY = "test-key"
mock_settings.MODEL_NAME = "command-a-03-2025"
mock_settings.TEMPERATURE = 0
mock_settings.MAX_TOKENS = 500
mock_settings.LLM_TIMEOUT = 30
mock_settings.LANGCHAIN_TRACING_V2 = False
mock_settings.LANGCHAIN_API_KEY = "test-key"

with patch.dict("os.environ", {
    "DATABASE_URL": "sqlite:///./test.db",
    "QDRANT_URL": "http://localhost:6333",
    "COHERE_API_KEY": "test-key",
    "MODEL_NAME": "command-a-03-2025",
    "TEMPERATURE": "0",
    "MAX_TOKENS": "500",
    "LLM_TIMEOUT": "30",
    "LANGCHAIN_TRACING_V2": "false",
    "LANGCHAIN_API_KEY": "test-key",
}):
    with patch("app.core.config.settings", mock_settings):
        from app.db.database import Base, get_db
        from app.main import app

# SQLite in-memory para tests
SQLALCHEMY_TEST_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_TEST_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """
    Crea tablas frescas para cada test y las destruye al terminar.
    Garantiza aislamiento total entre tests.
    """
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """
    Cliente HTTP de testing que usa la DB de prueba.
    Override de get_db asegura que los endpoints usen nuestra DB de test.
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def sample_candidate():
    """Datos de ejemplo para crear un candidato en tests."""
    return {
        "name": "Ana García",
        "email": "ana.garcia@example.com",
        "phone": "+5491155551234",
        "location": "Buenos Aires, Argentina",
        "headline": "Senior Python Developer",
        "summary": "Desarrolladora con 8 años de experiencia en Python y FastAPI",
        "role": "Backend Developer",
        "experience": "8 años en desarrollo backend con Python, Django, FastAPI",
        "skills": "Python, FastAPI, Django, PostgreSQL, Docker, AWS",
        "education": "Ing. en Sistemas - UBA"
    }


@pytest.fixture
def sample_candidate_update():
    """Datos parciales para actualizar un candidato."""
    return {
        "name": "Ana García López",
        "role": "Staff Engineer",
        "skills": "Python, FastAPI, Django, PostgreSQL, Docker, AWS, Kubernetes"
    }
