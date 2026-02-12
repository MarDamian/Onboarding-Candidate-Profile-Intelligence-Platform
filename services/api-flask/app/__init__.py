from flask import Flask, jsonify
from flask_cors import CORS
from app.core.config import settings
import logging
import sys
from pythonjsonlogger import jsonlogger

def setup_logging():
    """Configura el logging estructurado para Flask."""
    handler = logging.StreamHandler(sys.stdout)
    formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(name)s %(message)s')
    handler.setFormatter(formatter)
    
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)
    
    # Silenciar logs ruidosos de Flask/Werkzeug si no están en debug
    if not settings.DEBUG:
        logging.getLogger('werkzeug').setLevel(logging.WARNING)

def create_app():
    # Initialize logging
    setup_logging()
    
    app = Flask(__name__)
    app.config.from_object(settings)

    # Configurar CORS para permitir comunicación desde UI
    CORS(app, origins=["http://localhost:5173", "http://localhost:5174"], supports_credentials=True)

    from app.api.etl_routes import etl_bp
    from app.api.qdrant_routes import qdrant_bp
    
    app.register_blueprint(etl_bp)
    app.register_blueprint(qdrant_bp)

    @app.route('/health')
    def health():
        return jsonify({"status": "healthy", "service": settings.APP_NAME})

    return app