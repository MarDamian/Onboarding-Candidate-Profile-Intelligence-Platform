from dotenv import load_dotenv
from pydantic_settings import BaseSettings
import os

load_dotenv()

class Settings(BaseSettings):
     # API keys
    COHERE_API_KEY: str = os.getenv("COHERE_API_KEY")
    LANGCHAIN_TRACING_V2: bool = os.getenv("LANGCHAIN_TRACING_V2")
    LANGCHAIN_API_KEY: str = os.getenv("LANGCHAIN_API_KEY")
    
    # Configuración del LLM
    MODEL_NAME: str = os.getenv("MODEL_NAME")
    TEMPERATURE: int = os.getenv("TEMPERATURE")
    LLM_TIMEOUT: int = os.getenv("LLM_TIMEOUT")
    MAX_TOKENS: int = os.getenv("MAX_TOKENS")

    # Configuración de reintentos
    MAX_RETRIES: int = os.getenv("MAX_RETRIES")
    RETRY_MIN_WAIT: int = os.getenv("RETRY_MIN_WAIT")
    RETRY_MAX_WAIT: int = os.getenv("RETRY_MAX_WAIT")
    
    # Base de datos
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    QDRANT_URL: str = os.getenv("QDRANT_URL")
    
    # Redis (para encolar jobs al worker Rust)
    REDIS_URL: str = os.getenv("REDIS_URL")
    REDIS_QUEUE: str = os.getenv("REDIS_QUEUE")

settings = Settings()
