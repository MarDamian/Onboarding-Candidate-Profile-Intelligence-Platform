"""
Tests unitarios para EmbeddingsService.

¿Por qué testear el servicio de embeddings?
- Es el puente entre los datos del candidato y la representación vectorial
- Una dimensión incorrecta del vector rompe toda la búsqueda semántica
- Validamos que el modelo y input_type se pasan correctamente a Cohere
- Verificamos la validación de dimensiones del vector
"""

import pytest
from unittest.mock import patch, MagicMock
import os


class TestEmbeddingsService:
    """Tests para EmbeddingsService."""

    @patch.dict(os.environ, {
        "COHERE_API_KEY": "test-key",
        "EMBEDDING_MODEL": "embed-multilingual-v3.0",
        "EMBEDDING_DIMENSION": "1024"
    })
    @patch("pipelines.utils.embeddings_service.cohere.Client")
    def test_generate_embedding_returns_vector(self, mock_cohere_cls):
        """Debe retornar vector de la dimensión correcta."""
        mock_response = MagicMock()
        mock_response.embeddings.float = [[0.1] * 1024]
        
        mock_client = MagicMock()
        mock_client.embed.return_value = mock_response
        mock_cohere_cls.return_value = mock_client

        from pipelines.utils.embeddings_service import EmbeddingsService
        service = EmbeddingsService()
        vector = service.generate_embedding("test text")

        assert len(vector) == 1024
        mock_client.embed.assert_called_once()

    @patch.dict(os.environ, {
        "COHERE_API_KEY": "test-key",
        "EMBEDDING_MODEL": "embed-multilingual-v3.0",
        "EMBEDDING_DIMENSION": "1024"
    })
    @patch("pipelines.utils.embeddings_service.cohere.Client")
    def test_passes_correct_input_type(self, mock_cohere_cls):
        """Debe pasar el input_type correcto a Cohere."""
        mock_response = MagicMock()
        mock_response.embeddings.float = [[0.1] * 1024]
        
        mock_client = MagicMock()
        mock_client.embed.return_value = mock_response
        mock_cohere_cls.return_value = mock_client

        from pipelines.utils.embeddings_service import EmbeddingsService
        service = EmbeddingsService()
        service.generate_embedding("query text", input_type="search_query")

        call_kwargs = mock_client.embed.call_args[1]
        assert call_kwargs["input_type"] == "search_query"

    @patch.dict(os.environ, {
        "COHERE_API_KEY": "test-key",
        "EMBEDDING_MODEL": "embed-multilingual-v3.0",
        "EMBEDDING_DIMENSION": "1024"
    })
    @patch("pipelines.utils.embeddings_service.cohere.Client")
    def test_dimension_mismatch_raises_error(self, mock_cohere_cls):
        """Debe lanzar ValueError si la dimensión del vector no coincide."""
        mock_response = MagicMock()
        mock_response.embeddings.float = [[0.1] * 512]  # 512 en lugar de 1024
        
        mock_client = MagicMock()
        mock_client.embed.return_value = mock_response
        mock_cohere_cls.return_value = mock_client

        from pipelines.utils.embeddings_service import EmbeddingsService
        service = EmbeddingsService()

        with pytest.raises(ValueError, match="Dimensión del vector"):
            service.generate_embedding("test text")
