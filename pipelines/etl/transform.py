from pipelines.utils.embeddings_service import EmbeddingsService
from app.schemas.candidate import CandidateRead
import logging

logger = logging.getLogger(__name__)

class Transformer:
    def __init__(self):
        """Inicializa el transformador con el servicio de embeddings.
        
        El modelo se carga una sola vez para optimizar rendimiento.
        """
        self.embeddings_service = EmbeddingsService()
    
    def prepare_vector(self, candidate_row):
        """Valida y concatena los datos para generar el embedding.

        Args:
            candidate_row: Fila de la base de datos (SQLAlchemy Row).

        Returns:
            dict: Información de embeddings y data del candidate actual, o None si falla la validación.
        """
        try:
            # Validar usando el esquema de Pydantic
            candidate = CandidateRead.model_validate(candidate_row)
            
            context_text = f"{candidate.name} | {candidate.summary} | Skills: {candidate.skills} | Experience: {candidate.experience}"
            
            vector = self.embeddings_service.generate_embedding(context_text, input_type="search_document")
            
            return {
                "id": candidate.id,
                "vector": vector,
                "payload": {
                    "name": candidate.name,
                    "text_content": context_text,
                    "update_at": str(candidate.updated_at)
                }
            }
        except Exception as e:
            logger.error(f"Error validando/transformando candidato {getattr(candidate_row, 'id', 'unknown')}: {e}")
            return None
