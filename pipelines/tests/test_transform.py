"""
Tests unitarios para el Transformer del pipeline ETL.

¿Por qué testear el Transformer?
- Construye el texto de contexto que define la calidad del embedding
- Un texto mal formado genera embeddings de baja calidad → búsqueda semántica inútil
- Valida que el vector resultante tiene la estructura correcta para Qdrant
- Mockea Cohere para evitar costos y latencia
"""

import pytest
from unittest.mock import patch, MagicMock

from pipelines.etl.transform import Transformer


class TestTransformer:
    """Tests para la clase Transformer."""

    @patch("pipelines.etl.transform.EmbeddingsService")
    def test_prepare_vector_returns_correct_structure(self, mock_embed_cls, mock_candidate_row, sample_embedding):
        """Debe retornar dict con id, vector y payload."""
        mock_service = MagicMock()
        mock_service.generate_embedding.return_value = sample_embedding
        mock_embed_cls.return_value = mock_service

        transformer = Transformer()
        result = transformer.prepare_vector(mock_candidate_row)

        assert "id" in result
        assert "vector" in result
        assert "payload" in result
        assert result["id"] == 1
        assert len(result["vector"]) == 1024

    @patch("pipelines.etl.transform.EmbeddingsService")
    def test_prepare_vector_builds_context_text(self, mock_embed_cls, mock_candidate_row, sample_embedding):
        """Debe concatenar nombre, resumen, skills y experiencia en el contexto."""
        mock_service = MagicMock()
        mock_service.generate_embedding.return_value = sample_embedding
        mock_embed_cls.return_value = mock_service

        transformer = Transformer()
        result = transformer.prepare_vector(mock_candidate_row)

        # Verificar que el embedding se generó con el texto correcto
        call_args = mock_service.generate_embedding.call_args[0][0]
        assert "Ana García" in call_args
        assert "Python" in call_args
        assert "Skills:" in call_args

    @patch("pipelines.etl.transform.EmbeddingsService")
    def test_prepare_vector_payload_has_name(self, mock_embed_cls, mock_candidate_row, sample_embedding):
        """El payload debe incluir el nombre del candidato para Qdrant."""
        mock_service = MagicMock()
        mock_service.generate_embedding.return_value = sample_embedding
        mock_embed_cls.return_value = mock_service

        transformer = Transformer()
        result = transformer.prepare_vector(mock_candidate_row)

        assert result["payload"]["name"] == "Ana García"
        assert "text_content" in result["payload"]

    @patch("pipelines.etl.transform.EmbeddingsService")
    def test_uses_search_document_input_type(self, mock_embed_cls, mock_candidate_row, sample_embedding):
        """Debe usar input_type='search_document' para documentos (no queries)."""
        mock_service = MagicMock()
        mock_service.generate_embedding.return_value = sample_embedding
        mock_embed_cls.return_value = mock_service

        transformer = Transformer()
        transformer.prepare_vector(mock_candidate_row)

        call_kwargs = mock_service.generate_embedding.call_args
        assert call_kwargs[1]["input_type"] == "search_document"
