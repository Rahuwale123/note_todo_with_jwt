from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://postgres:QWer12@*@localhost:5432/fastapi_backend"
    
    # JWT Configuration
    jwt_secret_key: str = "your-super-secret-jwt-key-change-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440
    
    # API Configuration
    api_v1_str: str = "/api/v1"
    project_name: str = "FastAPI Backend - RBAC System"
    
    # CORS Configuration
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    backend_cors_origins: List[str] = ["http://localhost:3000", "http://localhost:8000"]

    class Config:
        env_file = ".env"


settings = Settings()
