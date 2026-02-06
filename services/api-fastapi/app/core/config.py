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
    
    # Base de datos
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    QDRANT_URL: str = os.getenv("QDRANT_URL")

settings = Settings()
