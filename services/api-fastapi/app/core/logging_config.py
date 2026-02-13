import logging
import sys
from pythonjsonlogger import jsonlogger

def setup_logging():
    """Configura el logging estructurado para la aplicación."""
    logger = logging.getLogger()
    
    # Evitar duplicados si ya está configurado
    if logger.handlers:
        return

    log_handler = logging.StreamHandler(sys.stdout)
    
    # Formato JSON con campos útiles
    formatter = jsonlogger.JsonFormatter(
        '%(asctime)s %(levelname)s %(name)s %(message)s'
    )
    log_handler.setFormatter(formatter)
    
    logger.addHandler(log_handler)
    logger.setLevel(logging.INFO)
    
    # Silenciar logs ruidosos de librerías de terceros
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.error").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

    logging.info("FastAPI structured logging initialized")
