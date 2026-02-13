"""
Tests para endpoints de búsqueda semántica.

¿Por qué mockear Qdrant y Cohere?
- Los servicios de búsqueda dependen de Qdrant (vector DB) y Cohere (embeddings)
- Llamadas reales son lentas (~500ms+), costosas ($) y requieren infraestructura
- Mocks permiten testear la lógica de routing, validación y manejo de errores
- En CI no hay Qdrant ni API keys de Cohere disponibles

¿Qué mockea cada patch?
- search_service.search: simula resultados de Qdrant
- search_service.find_similar: simula búsqueda por candidato similar
"""

import pytest
from unittest.mock import patch, MagicMock


class TestSemanticSearch:
    """Tests para POST /v1/semantic_search/"""

    @patch("app.api.v1.search.search_service")
    def test_search_returns_results(self, mock_service, client):
        """Debe retornar resultados de búsqueda semántica."""
        mock_service.search.return_value = [
            {"id": 1, "name": "Ana García", "score": 0.95},
            {"id": 2, "name": "Carlos López", "score": 0.87},
        ]

        response = client.post("/v1/semantic_search/", json={
            "query": "python developer",
            "limit": 10,
            "score_threshold": 0.5
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["query"] == "python developer"
        assert data["total_results"] == 2
        assert len(data["results"]) == 2

    @patch("app.api.v1.search.search_service")
    def test_search_empty_results(self, mock_service, client):
        """Debe retornar lista vacía cuando no hay coincidencias."""
        mock_service.search.return_value = []

        response = client.post("/v1/semantic_search/", json={
            "query": "especialista en cohetes espaciales"
        })
        
        assert response.status_code == 200
        assert response.json()["total_results"] == 0

    def test_search_invalid_query(self, client):
        """Debe retornar 422 para query demasiado corta."""
        response = client.post("/v1/semantic_search/", json={
            "query": "ab"
        })
        assert response.status_code == 422

    def test_search_missing_query(self, client):
        """Debe retornar 422 cuando falta query."""
        response = client.post("/v1/semantic_search/", json={})
        assert response.status_code == 422

    @patch("app.api.v1.search.search_service")
    def test_search_with_filters(self, mock_service, client):
        """Debe pasar filtros al servicio de búsqueda."""
        mock_service.search.return_value = [
            {"id": 1, "name": "Ana García", "score": 0.92}
        ]

        response = client.post("/v1/semantic_search/", json={
            "query": "backend developer",
            "skills_filter": ["Python", "FastAPI"],
            "name_filter": "Ana"
        })
        
        assert response.status_code == 200
        mock_service.search.assert_called_once_with(
            query_text="backend developer",
            limit=10,
            score_threshold=0.2,
            skills_filter=["Python", "FastAPI"],
            name_filter="Ana"
        )

    @patch("app.api.v1.search.search_service")
    def test_search_service_error(self, mock_service, client):
        """Debe retornar 500 cuando el servicio falla."""
        mock_service.search.side_effect = Exception("Qdrant connection failed")

        response = client.post("/v1/semantic_search/", json={
            "query": "developer python"
        })
        assert response.status_code == 500


class TestSimilarSearch:
    """Tests para GET /v1/semantic_search/similar/{id}"""

    @patch("app.api.v1.search.search_service")
    def test_find_similar(self, mock_service, client):
        """Debe retornar candidatos similares."""
        mock_service.find_similar.return_value = [
            {"id": 2, "name": "Carlos López", "score": 0.91}
        ]

        response = client.get("/v1/semantic_search/similar/1")
        assert response.status_code == 200
        assert response.json()["total_results"] == 1

    @patch("app.api.v1.search.search_service")
    def test_find_similar_not_found(self, mock_service, client):
        """Debe retornar 404 cuando el candidato no existe en Qdrant."""
        mock_service.find_similar.return_value = None

        response = client.get("/v1/semantic_search/similar/9999")
        assert response.status_code == 404

    @patch("app.api.v1.search.search_service")
    def test_find_similar_with_params(self, mock_service, client):
        """Debe respetar parámetros de limit y score_threshold."""
        mock_service.find_similar.return_value = []

        response = client.get("/v1/semantic_search/similar/1?limit=3&score_threshold=0.8")
        assert response.status_code == 200
        mock_service.find_similar.assert_called_once_with(
            candidate_id=1,
            limit=3,
            score_threshold=0.8
        )
