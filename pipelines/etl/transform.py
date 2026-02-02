class Transformer:
    def __init__(self):
        pass
    
    def prepare_vector(self, candidate):
        """Concatena los datos para dar contexto al vector.

        Args:
            candidate (Candidate): El candidate actual.

        Returns:
            dict: Información de embeddings y data del candidate actual.
        """
        context_text = f"{candidate.name} | {candidate.summary} | Skills: {candidate.skills} | Experience: {candidate.experience}"
        
        vector = [0.1]*384
        
        return {
            "id": candidate.id,
            "vector": vector,
            "payload": {
                "name": candidate.name,
                "text_content": context_text,
                "update_at": str(candidate.updated_at)
            }
        }