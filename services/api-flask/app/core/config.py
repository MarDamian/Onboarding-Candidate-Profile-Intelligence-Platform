from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.path.dirname(__file__), "../../../infra/.env"))

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    APP_NAME: str = "wTreData Admin API"
    DEBUG: bool = True
    REDIS_URL: str = os.getenv("REDIS_URL")
    QDRANT_HOST: str = os.getenv("QDRANT_HOST")

settings = Settings()