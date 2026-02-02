from flask import Blueprint, jsonify, make_response
from app.services.etl_manager import ETLManager

etl_bp = Blueprint('etl', __name__, url_prefix='/v1/admin/etl')
etl_service = ETLManager()

@etl_bp.route('/sync', methods=['POST'])
def sync():
    try:
        records = etl_service.trigger_sync()
        
        return jsonify({
            "status": "success",
            "message": "ETL pipeline executed",
            "records_processed": records
        }), 200
    except Exception as e:
        return make_response(jsonify({
            "error": str(e)
        }),500)

@etl_bp.route('/status', methods=['GET'])
def status():
    history = etl_service.get_execution_history()
    return jsonify(history), 200