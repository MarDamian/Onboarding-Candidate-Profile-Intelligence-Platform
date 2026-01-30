from dotenv import load_dotenv
import os

load_dotenv("../../infra/.env")

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")

settings = Settings()
