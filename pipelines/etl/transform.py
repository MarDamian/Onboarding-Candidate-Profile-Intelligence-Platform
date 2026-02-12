from pipelines.utils.embeddings_service import EmbeddingsService
import logging

logger = logging.getLogger(__name__)

class Transformer:
    def __init__(self):
        """Inicializa el transformador con el servicio de embeddings."""
        self.embeddings_service = EmbeddingsService()
    
    def _validate_row(self, row):
        """Validación interna y sencilla sin dependencias externas.
        
        Verifica campos esenciales para el proceso de indexing.
        """
        required_fields = ['id', 'name', 'summary', 'skills', 'experience']
        for field in required_fields:
            value = getattr(row, field, None)
            if value is None or (isinstance(value, str) and not value.strip()):
                logger.warning(f"Validación fallida: Campo '{field}' ausente o vacío en registro {getattr(row, 'id', 'desconocido')}")
                return False
        return True

    def prepare_vector(self, candidate_row):
        """Valida internamente y genera el embedding.

        Args:
            candidate_row: Fila de la base de datos (SQLAlchemy Row).

        Returns:
            dict: Información procesada o None si falla la validación.
        """
        try:
            if not self._validate_row(candidate_row):
                return None
            
            # Construcción segura del contexto
            name = getattr(candidate_row, 'name', '')
            summary = getattr(candidate_row, 'summary', '')
            skills = getattr(candidate_row, 'skills', 'N/A')
            experience = getattr(candidate_row, 'experience', 'N/A')
            
            context_text = f"{name} | {summary} | Skills: {skills} | Experience: {experience}"
            
            vector = self.embeddings_service.generate_embedding(context_text, input_type="search_document")
            
            return {
                "id": candidate_row.id,
                "vector": vector,
                "payload": {
                    "name": name,
                    "text_content": context_text,
                    "update_at": str(getattr(candidate_row, 'updated_at', ''))
                }
            }
        except Exception as e:
            logger.error(f"Error procesando candidato {getattr(candidate_row, 'id', 'unknown')}: {e}")
            return None

