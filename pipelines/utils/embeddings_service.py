import cohere
from typing import List
from dotenv import load_dotenv
import os
import warnings

warnings.filterwarnings("ignore", message=".*clean_up_tokenization_spaces.*")

load_dotenv()

class EmbeddingsService:
    """Servicio centralizado para generación de embeddings usando sentence-transformers."""
    
    def __init__(self):
        """Inicializa el servicio con el modelo especificado.
        """
        self.api_key = os.getenv("COHERE_API_KEY")
        self.client = cohere.Client(self.api_key)
        self.model = os.getenv("EMBEDDING_MODEL")
        self.dimension = os.getenv("EMBEDDING_DIMENSION")
        
    def generate_embedding(self, text: str, input_type: str = "search_document") -> List[float]:
        """Genera el vector de embedding para un texto dado.
        
        Args:
            text: Texto a convertir en embedding
            
        Returns:
            Lista de floats representando el vector de embedding
        """
        response = self.client.embed(
            texts=[text],
            model=self.model,
            input_type=input_type,
            embedding_types=['float']
        )

        return response.embeddings.float[0]
