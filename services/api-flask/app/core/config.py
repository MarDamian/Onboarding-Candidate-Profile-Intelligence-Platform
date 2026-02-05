from pydantic_settings import BaseSettings
from dotenv import load_dotenv

import os

load_dotenv(os.path.join(os.path.dirname(__file__), "../../../infra/.env"))

class Settings(BaseSettings):
    # Configuración de Framework
    APP_NAME: str = "wTreData Admin API"
    DEBUG: bool = True
    
    # Base de datos
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    REDIS_URL: str = os.getenv("REDIS_URL")
    QDRANT_HOST: str = os.getenv("QDRANT_HOST")
    
    COHERE_API_KEY: str = os.getenv("COHERE_API_KEY")

settings = Settings()