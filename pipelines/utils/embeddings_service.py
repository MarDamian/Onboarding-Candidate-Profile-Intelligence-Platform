from sentence_transformers import SentenceTransformer
from typing import List
import os
import warnings

warnings.filterwarnings("ignore", message=".*clean_up_tokenization_spaces.*")


class EmbeddingsService:
    """Servicio centralizado para generación de embeddings usando sentence-transformers."""
    
    def __init__(self, model_name: str = None):
        """Inicializa el servicio con el modelo especificado.
        
        Args:
            model_name: Nombre del modelo de sentence-transformers a usar.
                       Si no se especifica, se lee de EMBEDDING_MODEL env var.
        """
        if model_name is None:
            model_name = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
        
        self.model = SentenceTransformer(model_name)
        self.dimension = int(os.getenv("EMBEDDING_DIMENSION", "384"))
        
    def generate_embedding(self, text: str) -> List[float]:
        """Genera el vector de embedding para un texto dado.
        
        Args:
            text: Texto a convertir en embedding
            
        Returns:
            Lista de floats representando el vector de embedding
        """
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding.tolist()
