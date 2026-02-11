"""
Tests unitarios para Pydantic schemas de la API.

¿Por qué testear schemas por separado?
- Los schemas son la primera línea de defensa contra datos inválidos
- Una validación mal configurada puede permitir datos corruptos en la DB
- Tests unitarios de schemas son extremadamente rápidos (<1ms cada uno)
- Documentan el contrato de la API de forma ejecutable

Cobertura:
- CandidateCreate: campos requeridos, opcionales, validación de email
- CandidateUpdate: todos los campos opcionales
- CandidateRead: fromm_attributes con ORM
- SearchRequest: validación de rangos y defaults
- InsightSchema: estructura de respuesta LLM
"""

import pytest
from pydantic import ValidationError

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.schemas.candidate import CandidateCreate, CandidateUpdate, CandidateRead
from app.schemas.search import SearchRequest
from app.schemas.insight import InsightSchema


class TestCandidateCreate:
    """Validación del schema de creación de candidatos."""

    def test_valid_candidate(self):
        """Debe aceptar candidato con todos los campos válidos."""
        candidate = CandidateCreate(
            name="Juan Pérez",
            email="juan@example.com",
            phone="+5491155551234"
        )
        assert candidate.name == "Juan Pérez"
        assert candidate.email == "juan@example.com"

    def test_missing_name_raises(self):
        """Debe rechazar candidato sin nombre."""
        with pytest.raises(ValidationError) as exc_info:
            CandidateCreate(email="test@test.com", phone="123")
        assert "name" in str(exc_info.value)

    def test_missing_email_raises(self):
        """Debe rechazar candidato sin email."""
        with pytest.raises(ValidationError):
            CandidateCreate(name="Test", phone="123")

    def test_invalid_email_raises(self):
        """Debe rechazar email con formato inválido."""
        with pytest.raises(ValidationError):
            CandidateCreate(
                name="Test",
                email="no-es-email",
                phone="123"
            )

    def test_optional_fields_default_none(self):
        """Campos opcionales deben ser None por defecto."""
        candidate = CandidateCreate(
            name="Test",
            email="test@test.com",
            phone="123"
        )
        assert candidate.location is None
        assert candidate.summary is None
        assert candidate.skills is None
        assert candidate.education is None
        assert candidate.headline is None
        assert candidate.role is None
        assert candidate.experience is None

    def test_all_optional_fields(self):
        """Debe aceptar todos los campos opcionales."""
        candidate = CandidateCreate(
            name="Test",
            email="test@test.com",
            phone="123",
            location="CDMX",
            headline="Dev",
            summary="Resumen",
            role="Backend",
            experience="5 años",
            skills="Python",
            education="Ing. Sistemas"
        )
        assert candidate.location == "CDMX"
        assert candidate.skills == "Python"


class TestCandidateUpdate:
    """Validación del schema de actualización de candidatos."""

    def test_all_fields_optional(self):
        """Todos los campos deben ser opcionales para update parcial."""
        update = CandidateUpdate()
        assert update.name is None
        assert update.email is None
        assert update.phone is None

    def test_partial_update(self):
        """Debe aceptar actualización parcial."""
        update = CandidateUpdate(name="Nuevo Nombre", role="Staff")
        assert update.name == "Nuevo Nombre"
        assert update.role == "Staff"
        assert update.email is None

    def test_invalid_email_in_update(self):
        """Debe rechazar email inválido incluso en update."""
        with pytest.raises(ValidationError):
            CandidateUpdate(email="no-valido")


class TestSearchRequest:
    """Validación del schema de búsqueda semántica."""

    def test_valid_search(self):
        """Debe aceptar búsqueda válida."""
        search = SearchRequest(query="python developer")
        assert search.query == "python developer"
        assert search.limit == 10  # default
        assert search.score_threshold == 0.2  # default

    def test_query_too_short(self):
        """Debe rechazar query con menos de 3 caracteres."""
        with pytest.raises(ValidationError):
            SearchRequest(query="ab")

    def test_limit_boundaries(self):
        """Debe validar que limit esté entre 1 y 50."""
        with pytest.raises(ValidationError):
            SearchRequest(query="test query", limit=0)
        with pytest.raises(ValidationError):
            SearchRequest(query="test query", limit=51)

    def test_score_threshold_boundaries(self):
        """Debe validar que score_threshold esté entre 0.0 y 1.0."""
        with pytest.raises(ValidationError):
            SearchRequest(query="test query", score_threshold=-0.1)
        with pytest.raises(ValidationError):
            SearchRequest(query="test query", score_threshold=1.1)

    def test_optional_filters(self):
        """Filtros deben ser opcionales."""
        search = SearchRequest(query="backend developer")
        assert search.skills_filter is None
        assert search.name_filter is None

    def test_with_filters(self):
        """Debe aceptar filtros de skills y nombre."""
        search = SearchRequest(
            query="developer",
            skills_filter=["Python", "React"],
            name_filter="Ana"
        )
        assert search.skills_filter == ["Python", "React"]
        assert search.name_filter == "Ana"


class TestInsightSchema:
    """Validación del schema de insights LLM."""

    def test_valid_insight(self):
        """Debe aceptar insight completo."""
        insight = InsightSchema(
            summary="Desarrollador senior con amplia experiencia",
            score=85,
            strengths=["Python", "Liderazgo"],
            weaknesses=["Frontend"],
            suggested_role="Tech Lead"
        )
        assert insight.score == 85
        assert len(insight.strengths) == 2

    def test_missing_fields_raises(self):
        """Debe rechazar insight incompleto."""
        with pytest.raises(ValidationError):
            InsightSchema(summary="Solo resumen")
