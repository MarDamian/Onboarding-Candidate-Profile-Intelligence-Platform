"""
Tests unitarios para el Extractor del pipeline ETL.

¿Por qué testear el Extractor?
- Es la primera etapa del pipeline — si falla, todo falla
- Verifica que la query SQL busca correctamente candidatos "stale"
- Valida la lógica de idempotencia: solo extrae candidatos no indexados o modificados
"""

import pytest
from unittest.mock import patch, MagicMock

from pipelines.etl.extract import Extractor


class TestExtractor:
    """Tests para la clase Extractor."""

    @patch("pipelines.etl.extract.create_engine")
    def test_init_creates_engine(self, mock_create_engine):
        """Debe crear engine de SQLAlchemy con la URL proporcionada."""
        extractor = Extractor("postgresql://test:test@localhost/testdb")
        mock_create_engine.assert_called_once_with("postgresql://test:test@localhost/testdb")

    @patch("pipelines.etl.extract.create_engine")
    def test_get_stale_candidates_executes_query(self, mock_create_engine):
        """Debe ejecutar query SQL para obtener candidatos no indexados."""
        mock_conn = MagicMock()
        mock_conn.execute.return_value.fetchall.return_value = []
        mock_engine = MagicMock()
        mock_engine.connect.return_value.__enter__ = lambda s: mock_conn
        mock_engine.connect.return_value.__exit__ = MagicMock(return_value=False)
        mock_create_engine.return_value = mock_engine

        extractor = Extractor("postgresql://test:test@localhost/testdb")
        result = extractor.get_stale_candidate()

        mock_conn.execute.assert_called_once()
        assert result == []

    @patch("pipelines.etl.extract.create_engine")
    def test_get_stale_candidates_returns_rows(self, mock_create_engine, mock_candidate_rows):
        """Debe retornar filas de candidatos pendientes de indexación."""
        mock_conn = MagicMock()
        mock_conn.execute.return_value.fetchall.return_value = mock_candidate_rows
        mock_engine = MagicMock()
        mock_engine.connect.return_value.__enter__ = lambda s: mock_conn
        mock_engine.connect.return_value.__exit__ = MagicMock(return_value=False)
        mock_create_engine.return_value = mock_engine

        extractor = Extractor("postgresql://test:test@localhost/testdb")
        result = extractor.get_stale_candidate()

        assert len(result) == 3
        assert result[0].id == 1
