from flask import Blueprint, jsonify, make_response
from qdrant_client import QdrantClient
from qdrant_client.models import Filter
from pipelines.etl.main import run_pipeline
from sqlalchemy import create_engine, text
import os

qdrant_bp = Blueprint('qdrant', __name__, url_prefix='/v1/admin/qdrant')

QDRANT_HOST = os.getenv("QDRANT_HOST")
DB_URL = os.getenv("DATABASE_URL")


@qdrant_bp.route('/reindex', methods=['POST'])
def reindex_all():
    try:
        engine = create_engine(DB_URL)
        with engine.connect() as conn:
            result = conn.execute(text("UPDATE candidates SET last_indexed_at = NULL"))
            conn.commit()
        
        records_processed = run_pipeline()
        
        return jsonify({
            "status": "success",
            "message": "Re-indexación completada exitosamente",
            "candidates_reindexed": records_processed
        }), 200
    except Exception as e:
        return make_response(jsonify({
            "error": f"Error durante re-indexación: {str(e)}"
        }), 500)


@qdrant_bp.route('/stats', methods=['GET'])
def get_stats():
    try:
        client = QdrantClient(host=QDRANT_HOST, port=6333)
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
        client = QdrantClient(host=QDRANT_HOST, port=6333)
        
        collection_info = client.get_collection(collection_name="candidates")
        points_count = collection_info.points_count
        
        client.delete(
            collection_name="candidates",
            points_selector=Filter(must=[])
        )
        
        engine = create_engine(DB_URL)
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
    try:
        client = QdrantClient(host=QDRANT_HOST, port=6333)
        
        client.delete(
            collection_name="candidates",
            points_selector=Filter(must=[])
        )
        
        engine = create_engine(DB_URL)
        with engine.connect() as conn:
            conn.execute(text("UPDATE candidates SET last_indexed_at = NULL"))
            conn.commit()
        
        records_processed = run_pipeline()
        
        return jsonify({
            "status": "success",
            "message": "Colección reconstruida exitosamente",
            "candidates_reindexed": records_processed
        }), 200
    except Exception as e:
        return make_response(jsonify({
            "error": f"Error reconstruyendo colección: {str(e)}"
        }), 500)
