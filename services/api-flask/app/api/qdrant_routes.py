from flask import Blueprint, jsonify, make_response
from qdrant_client import QdrantClient
from qdrant_client.models import Filter
from pipelines.etl.main import DB_URL, run_pipeline
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.services.etl_manager import ETLManager

qdrant_bp = Blueprint('qdrant', __name__, url_prefix='/v1/admin/qdrant')
etl_service = ETLManager()


@qdrant_bp.route('/reindex', methods=['POST'])
def reindex_all():
    """
    Encola un full_reindex asíncrono al worker Rust.
    El worker: limpia Qdrant → resetea last_indexed_at → re-procesa todos los candidatos.
    """
    try:
        result = etl_service.trigger_full_reindex(requested_by="flask:reindex")
        
        return jsonify({
            'status': 'accepted', 
            'message': 'Full reindex job queued for async processing by Rust worker',
            'data': result
        }), 202
    except Exception as e:
        return make_response(jsonify({
            "error": f"Error queueing re-index: {str(e)}"
        }), 500)


@qdrant_bp.route('/reindex/sync', methods=['POST'])
def reindex_all_sync():
    """
    Reindex síncrono (legacy/fallback) — ejecuta pipeline Python directamente.
    """
    try:
        engine = create_engine(DB_URL)
        with engine.connect() as conn:
            conn.execute(text("UPDATE candidates SET last_indexed_at = NULL"))
            conn.commit()
        
        result = run_pipeline()
        
        return jsonify({
            'status': 'success', 
            'message': 'Reindexing completed (sync)', 
            'details': result
        }), 200
    except Exception as e:
        return make_response(jsonify({
            "error": f"Error during re-indexing: {str(e)}"
        }), 500)


@qdrant_bp.route('/stats', methods=['GET'])
def get_stats():
    try:
        client = QdrantClient(url=settings.QDRANT_URL)
        collection_info = client.get_collection(collection_name="candidates")
        
        return jsonify({
            "collection_name": "candidates",
            "points_count": collection_info.points_count,
            "indexed_vectors_count": collection_info.indexed_vectors_count,
            "segments_count": collection_info.segments_count,
            "status": collection_info.status.name
        }), 200
    except Exception as e:
        return make_response(jsonify({
            "error": f"Error obteniendo estadísticas: {str(e)}"
        }), 500)


@qdrant_bp.route('/clear', methods=['DELETE'])
def clear_collection():
    try:
        client = QdrantClient(url=settings.QDRANT_URL)
        
        collection_info = client.get_collection(collection_name="candidates")
        points_count = collection_info.points_count
        
        client.delete(
            collection_name="candidates",
            points_selector=Filter(must=[])
        )
        
        engine = create_engine(settings.DATABASE_URL)
        with engine.connect() as conn:
            conn.execute(text("UPDATE candidates SET last_indexed_at = NULL"))
            conn.commit()
        
        return jsonify({
            "status": "success",
            "message": "Colección limpiada exitosamente. Ejecuta /reindex para re-poblarla.",
            "points_deleted": points_count
        }), 200
    except Exception as e:
        return make_response(jsonify({
            "error": f"Error limpiando colección: {str(e)}"
        }), 500)


@qdrant_bp.route('/rebuild', methods=['POST'])
def rebuild_collection():
    """
    Encola un full_reindex asíncrono al worker Rust.
    El worker limpia Qdrant, resetea la BD y re-indexa todo.
    """
    try:
        result = etl_service.trigger_full_reindex(requested_by="flask:rebuild")
        
        return jsonify({
            "status": "accepted",
            "message": "Rebuild job queued for async processing by Rust worker",
            "data": result
        }), 202
    except Exception as e:
        return make_response(jsonify({
            "error": f"Error queueing rebuild: {str(e)}"
        }), 500)


@qdrant_bp.route('/rebuild/sync', methods=['POST'])
def rebuild_collection_sync():
    """
    Rebuild síncrono (legacy/fallback).
    """
    try:
        client = QdrantClient(url=settings.QDRANT_URL)
        
        client.delete(
            collection_name="candidates",
            points_selector=Filter(must=[])
        )
        
        engine = create_engine(settings.DATABASE_URL)
        with engine.connect() as conn:
            conn.execute(text("UPDATE candidates SET last_indexed_at = NULL"))
            conn.commit()
        
        records_processed = run_pipeline()
        
        return jsonify({
            "status": "success",
            "message": "Colección reconstruida exitosamente (sync)",
            "candidates_reindexed": records_processed
        }), 200
    except Exception as e:
        return make_response(jsonify({
            "error": f"Error reconstruyendo colección: {str(e)}"
        }), 500)
