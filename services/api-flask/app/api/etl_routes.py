from flask import Blueprint, jsonify, make_response, request
from app.services.etl_manager import ETLManager

etl_bp = Blueprint('etl', __name__, url_prefix='/v1/admin/etl')
etl_service = ETLManager()

@etl_bp.route('/sync', methods=['POST'])
def sync():
    """
    Envía un job de ETL a la cola de Redis para procesamiento asíncrono.
    """
    try:
        # Obtener requested_by del body o usar default
        data = request.get_json() if request.is_json else {}
        requested_by = data.get('requested_by', 'api')
        
        result = etl_service.trigger_sync(requested_by=requested_by)
        
        return jsonify({
            "status": "success",
            "message": "ETL job queued successfully",
            "data": result
        }), 202  # 202 Accepted para procesamiento asíncrono
    except Exception as e:
        return make_response(jsonify({
            "error": str(e)
        }), 500)

@etl_bp.route('/sync/direct', methods=['POST'])
def sync_direct():
    """
    Ejecuta el ETL de forma síncrona (legacy/debugging).
    """
    try:
        records = etl_service.trigger_sync_direct()
        
        return jsonify({
            "status": "success",
            "message": "ETL pipeline executed synchronously",
            "records_processed": records
        }), 200
    except Exception as e:
        return make_response(jsonify({
            "error": str(e)
        }), 500)

@etl_bp.route('/status', methods=['GET'])
def status():
    try:
        executions = etl_service.get_executions()
        return jsonify({"executions": executions}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500