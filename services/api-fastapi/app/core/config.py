from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from typing import Optional
import os

load_dotenv("../../infra/.env")

class Settings(BaseSettings):
     # API keys
    COHERE_API_KEY: str = os.getenv("COHERE_API_KEY")
    LANGCHAIN_TRACING_V2: bool = False
    LANGCHAIN_API_KEY: str = " "
    
    # Configuración del LLM
    MODEL_NAME: str = "command-a-03-2025"
    TEMPERATURE: int = 0
    
    # Base de datos
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    QDRANT_HOST: str = os.getenv("QDRANT_HOST")
    QDRANT_PORT: int = 6333

settings = Settings()
