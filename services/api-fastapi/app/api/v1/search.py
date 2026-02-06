from fastapi import APIRouter, HTTPException, Query
from app.schemas.search import SearchRequest
from app.core.config import settings
from pipelines.utils.search_service import SearchService

router = APIRouter(prefix="/semantic_search", tags=["search"])

search_service = SearchService(
    qdrant_url=settings.QDRANT_URL
)
 
@router.post("/")
def semantic_search(search_params: SearchRequest):
    """Realiza búsqueda semántica de candidatos.

    Args:
        search_params (SearchRequest): Esquema de la Request (query, limit ...)

    Raises:
        HTTPException: Status 500 busqueda no se pudo realizar o error del servidor

    Returns:
        dict: Datos de query, total de resultados y resultados de perfiles
    """
    try:
        results = search_service.search(
            query_text=search_params.query,
            limit=search_params.limit,
            score_threshold=search_params.score_threshold,
            skills_filter=search_params.skills_filter,
            name_filter=search_params.name_filter
        )
        
        return {
            "query": search_params.query,
            "total_results": len(results),
            "results": results
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error: {str(e)}."
        )
        
@router.get("/similar/{candidate_id}")
def search_similar(
    candidate_id: int,
    limit: int = Query(5, ge=1, le=50),
    score_threshold: float = Query(0.0, ge=0.0, le=1.0)
):
    """Encuentra candidatos similares a uno existente.

    Args:
        candidate_id (int): Identificador del candidato
        limit (int, optional): Limite de perfiles encontrados. Defaults to Query(5, ge=1, le=50).
        score_threshold (float, optional): Puntaje de proximidad o similitud. Defaults to Query(0.0, ge=0.0, le=1.0).

    Raises:
        HTTPException: Status 404 de candidato no encontrado en qdrant
        HTTPException: status 500 error por parte del servidor

    Returns:
        dict: Un diccionario de los datos del resultado de candidatos similares
    """
    try:
        results = search_service.find_similar(
            candidate_id=candidate_id,
            limit=limit,
            score_threshold=score_threshold
        )

        if results is None:
            raise HTTPException(
                status_code=404,
                detail=f"Candidate with ID {candidate_id} not found in Qdrant"
            )

        return {
            "query": f"Similares al candidato",
            "total_results": len(results),
            "results": results
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error: {str(e)}"
        )