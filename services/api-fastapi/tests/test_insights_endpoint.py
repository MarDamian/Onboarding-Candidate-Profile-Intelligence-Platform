"""
Tests para el endpoint de insights LLM.

¿Por qué mockear el Agent?
- El LLM Agent llama a Cohere (~2-5s por request, ~$0.01 por llamada)
- Los resultados del LLM son no-determinísticos
- En CI no hay API key de Cohere ni de LangChain
- Mockeamos el Agent para verificar que el endpoint:
  1. Busca el candidato en DB
  2. Comprime el contexto
  3. Invoca al agent
  4. Retorna la estructura correcta
"""

import pytest
from unittest.mock import patch, AsyncMock, MagicMock


class TestInsightsEndpoint:
    """Tests para GET /v1/insights/{id}"""

    @patch("app.api.v1.insights.Agent")
    @patch("app.api.v1.insights.SessionLocal")
    def test_generate_insights_success(self, mock_session_cls, mock_agent_cls, client):
        """Debe generar insights para un candidato existente."""
        # Mock del candidato en DB
        mock_candidate = MagicMock()
        mock_candidate.id = 1
        mock_candidate.summary = "Desarrollador Python senior"
        mock_candidate.skills = "Python,FastAPI,Docker"
        
        mock_session = MagicMock()
        mock_session.query.return_value.filter.return_value.first.return_value = mock_candidate
        mock_session_cls.return_value = mock_session

        # Mock del Agent
        mock_agent_instance = MagicMock()
        mock_agent_instance.generate_insight = AsyncMock(return_value={
            "summary": "Candidato con alto potencial",
            "score": 85,
            "strengths": ["Python", "Backend"],
            "weaknesses": ["Frontend"],
            "suggested_role": "Senior Backend Developer"
        })
        mock_agent_cls.return_value = mock_agent_instance

        response = client.get("/v1/insights/1")
        assert response.status_code == 200
        data = response.json()
        assert data["candidate_id"] == 1
        assert "insights" in data

    @patch("app.api.v1.insights.SessionLocal")
    def test_insights_candidate_not_found(self, mock_session_cls, client):
        """Debe retornar 404 si el candidato no existe."""
        mock_session = MagicMock()
        mock_session.query.return_value.filter.return_value.first.return_value = None
        mock_session_cls.return_value = mock_session

        response = client.get("/v1/insights/9999")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
