from pipelines.utils.embeddings_service import EmbeddingsService


class Transformer:
    def __init__(self):
        """Inicializa el transformador con el servicio de embeddings.
        
        El modelo se carga una sola vez para optimizar rendimiento.
        """
        self.embeddings_service = EmbeddingsService()
    
    def prepare_vector(self, candidate):
        """Concatena los datos para dar contexto al vector y genera embedding real.

        Args:
            candidate (Candidate): El candidate actual.

        Returns:
            dict: Información de embeddings y data del candidate actual.
        """
        context_text = f"{candidate.name} | {candidate.summary} | Skills: {candidate.skills} | Experience: {candidate.experience}"
        
        vector = self.embeddings_service.generate_embedding(context_text)
        
        return {
            "id": candidate.id,
            "vector": vector,
            "payload": {
                "name": candidate.name,
                "text_content": context_text,
                "update_at": str(candidate.updated_at)
            }
        }