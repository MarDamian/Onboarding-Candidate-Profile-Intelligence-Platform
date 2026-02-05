from flask import Flask, jsonify
from flask_cors import CORS
from app.core.config import settings

def create_app():
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