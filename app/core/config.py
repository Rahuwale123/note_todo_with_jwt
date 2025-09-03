from pydantic_settings import BaseSettings
from typing import Optional
from urllib.parse import quote_plus


class Settings(BaseSettings):
    database_url: str = "mysql+mysqlconnector://root:" + quote_plus("QWer12@*") + "@localhost:3306/fastapi_backend"
    jwt_secret_key: str = "your-super-secret-jwt-key-change-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440
    api_v1_str: str = "/api/v1"
    project_name: str = "FastAPI Backend"
    backend_cors_origins: list = ["http://localhost:3000", "http://localhost:8080"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
