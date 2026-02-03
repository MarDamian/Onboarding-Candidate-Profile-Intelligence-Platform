from flask import Blueprint, jsonify, request, make_response
from pydantic import BaseModel, Field, ValidationError
from typing import Optional
import os

from pipelines.utils.search_service import SearchService

search_bp = Blueprint('search', __name__, url_prefix='/v1/search')

# Inicializar servicio de búsqueda
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
search_service = SearchService(qdrant_host=QDRANT_HOST, qdrant_port=6333)


class SearchRequest(BaseModel):
    """Schema para búsqueda semántica."""
    query: str = Field(..., min_length=3, description="Texto de búsqueda")
    limit: int = Field(default=10, ge=1, le=50, description="Número máximo de resultados")
    score_threshold: float = Field(default=0.2, ge=0.0, le=1.0, description="Umbral mínimo de similitud")
    skills_filter: Optional[list[str]] = Field(default=None, description="Filtrar por skills específicas")
    name_filter: Optional[str] = Field(default=None, description="Filtrar por nombre del candidato")


@search_bp.route('/', methods=['POST'])
def semantic_search():
    """
    Realiza búsqueda semántica de candidatos.
    
    Body (JSON):
        query (str): Texto de búsqueda en lenguaje natural
        limit (int): Número máximo de resultados (1-50, default: 10)
        score_threshold (float): Umbral mínimo de similitud 0-1 (default: 0.2)
        skills_filter (list[str]): Lista de skills para filtrar (opcional)
        name_filter (str): Nombre del candidato para filtrar (opcional)
    
    Returns:
        JSON con resultados de búsqueda ordenados por relevancia
    """
    try:
        data = request.get_json()
        
        if not data:
            return make_response(jsonify({
                "error": "Request body is required"
            }), 400)
        
        # Validar con Pydantic
        search_params = SearchRequest(**data)
        
        # Ejecutar búsqueda
        results = search_service.search(
            query_text=search_params.query,
            limit=search_params.limit,
            score_threshold=search_params.score_threshold,
            skills_filter=search_params.skills_filter,
            name_filter=search_params.name_filter
        )
        
        return jsonify({
            "query": search_params.query,
            "total_results": len(results),
            "results": results
        }), 200
    
    except ValidationError as e:
        return make_response(jsonify({
            "error": "Validation error",
            "details": e.errors()
        }), 400)
    
    except Exception as e:
        return make_response(jsonify({
            "error": f"Error durante la búsqueda: {str(e)}"
        }), 500)


@search_bp.route('/similar/<int:candidate_id>', methods=['GET'])
def search_similar(candidate_id: int):
    """
    Encuentra candidatos similares a uno existente.
    
    Args:
        candidate_id (int): ID del candidato de referencia
    
    Query params:
        limit (int): Número máximo de resultados (default: 5)
        score_threshold (float): Umbral mínimo de similitud (default: 0.0)
    
    Returns:
        JSON con candidatos similares ordenados por relevancia
    """
    try:
        # Obtener parámetros de query
        limit = request.args.get('limit', default=5, type=int)
        score_threshold = request.args.get('score_threshold', default=0.0, type=float)
        
        # Validar límites
        if limit < 1 or limit > 50:
            return make_response(jsonify({
                "error": "limit debe estar entre 1 y 50"
            }), 400)
        
        if score_threshold < 0.0 or score_threshold > 1.0:
            return make_response(jsonify({
                "error": "score_threshold debe estar entre 0.0 y 1.0"
            }), 400)
        
        # Ejecutar búsqueda de similares
        results = search_service.find_similar(
            candidate_id=candidate_id,
            limit=limit,
            score_threshold=score_threshold
        )
        
        if results is None:
            return make_response(jsonify({
                "error": f"Candidato con ID {candidate_id} no encontrado en Qdrant"
            }), 404)
        
        return jsonify({
            "query": f"Similares al candidato ID {candidate_id}",
            "total_results": len(results),
            "results": results
        }), 200
    
    except Exception as e:
        return make_response(jsonify({
            "error": f"Error buscando similares: {str(e)}"
        }), 500)
