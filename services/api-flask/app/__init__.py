from flask import Flask, jsonify
from app.core.config import settings

def create_app():
    app = Flask(__name__)
    app.config.from_object(settings)

    from app.api.etl_routes import etl_bp
    app.register_blueprint(etl_bp)

    @app.route('/health')
    def health():
        return jsonify({"status": "healthy", "service": settings.APP_NAME})

    return app