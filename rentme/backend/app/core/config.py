"""
렌트미 설정
"""
from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    # App
    APP_NAME: str = "렌트미"
    DEBUG: bool = True

    # Supabase
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""

    # JWT
    JWT_SECRET_KEY: str = "rentme-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24시간

    # OpenAI
    OPENAI_API_KEY: str = ""

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]

    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()
