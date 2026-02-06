from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue, MatchText, MatchAny
from pipelines.utils.embeddings_service import EmbeddingsService
from typing import Optional


class SearchService:
    """Servicio para búsqueda semántica en Qdrant con filtros avanzados."""
    
    def __init__(self, qdrant_url: str ):
        """Inicializa el servicio de búsqueda.
        
        Args:
            qdrant_url: Host del servidor Qdrant
        """
        self.client = QdrantClient(url=qdrant_url)
        self.embeddings_service = EmbeddingsService()
        self.collection_name = "candidates"
    
    def search(
        self,
        query_text: str,
        limit: int = 10,
        score_threshold: float = 0.5,
        skills_filter: Optional[list[str]] = None,
        name_filter: Optional[str] = None
    ):
        """Realiza búsqueda semántica con filtros opcionales.
        
        Args:
            query_text: Texto de la consulta (ej: "desarrollador python con 5 años de experiencia")
            limit: Número máximo de resultados
            score_threshold: Umbral mínimo de similitud (0-1)
            skills_filter: Lista de skills que debe contener (búsqueda parcial)
            name_filter: Filtro por nombre del candidato (búsqueda parcial)
            
        Returns:
            Lista de candidatos ordenados por relevancia con sus scores
        """

        query_vector = self.embeddings_service.generate_embedding(
            query_text, 
            input_type="search_query"
        )
        
        must_conditions = []
        should_conditions = []
        
        if skills_filter:
            # Skills con OR: debe tener AL MENOS UNA de las skills
            for skill in skills_filter:
                should_conditions.append(
                    FieldCondition(
                        key="text_content",
                        match=MatchText(text=skill)
                    )
                )
        
        if name_filter:
            # Name con AND: debe cumplir el nombre
            must_conditions.append(
                FieldCondition(
                    key="name",
                    match=MatchText(text=name_filter)
                )
            )
        
        # Construir filtro: must (AND) para nombre, should (OR) para skills
        query_filter = None
        if must_conditions or should_conditions:
            query_filter = Filter(
                must=must_conditions if must_conditions else None,
                should=should_conditions if should_conditions else None
            )
        
        search_result = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=limit,
            score_threshold=score_threshold,
            query_filter=query_filter
        ).points
        
        results = []
        for point in search_result:
            results.append({
                "id": point.id,
                "score": point.score,
                "name": point.payload.get("name"),
                "text_content": point.payload.get("text_content"),
                "updated_at": point.payload.get("update_at")
            })
        
        return results
    
    def find_similar(
        self,
        candidate_id: int,
        limit: int = 10,
        score_threshold: float = 0.0
    ):
        """Encuentra candidatos similares a uno existente.
        
        Args:
            candidate_id: ID del candidato de referencia
            limit: Número máximo de resultados
            score_threshold: Umbral mínimo de similitud
            
        Returns:
            Lista de candidatos similares o None si el candidato no existe
        """
        try:
            # Obtener el punto del candidato de referencia
            point = self.client.retrieve(
                collection_name=self.collection_name,
                ids=[candidate_id],
                with_vectors=True
            )
            
            if not point or len(point) == 0:
                return None
            
            # Obtener el vector del candidato
            candidate_vector = point[0].vector
            
            # Buscar candidatos similares
            search_result = self.client.query_points(
                collection_name=self.collection_name,
                query=candidate_vector,
                limit=limit + 1,  # +1 porque incluirá el mismo candidato
                score_threshold=score_threshold
            ).points
            
            # Filtrar el candidato original y formatear resultados
            results = []
            for point in search_result:
                # Excluir el candidato de referencia
                if point.id != candidate_id:
                    results.append({
                        "id": point.id,
                        "score": point.score,
                        "name": point.payload.get("name"),
                        "text_content": point.payload.get("text_content"),
                        "updated_at": point.payload.get("update_at")
                    })
            
            return results[:limit]
        
        except Exception as e:
            raise Exception(f"Error buscando similares: {str(e)}")