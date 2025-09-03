import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db
from app.models.base import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


class TestAuth:
    def test_signup_new_user(self):
        response = client.post(
            "/api/v1/auth/signup",
            json={"username": "testuser", "password": "testpass"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"
        assert "id" in data
        assert data["role"] == "ADMIN"
    
    def test_signup_existing_username(self):
        client.post(
            "/api/v1/auth/signup",
            json={"username": "existinguser", "password": "testpass"}
        )
        
        response = client.post(
            "/api/v1/auth/signup",
            json={"username": "existinguser", "password": "testpass"}
        )
        assert response.status_code == 400
        assert "Username already registered" in response.json()["detail"]
    
    def test_login_valid_credentials(self):
        client.post(
            "/api/v1/auth/signup",
            json={"username": "loginuser", "password": "testpass"}
        )
        
        response = client.post(
            "/api/v1/auth/login",
            json={"username": "loginuser", "password": "testpass"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_invalid_credentials(self):
        response = client.post(
            "/api/v1/auth/login",
            json={"username": "nonexistent", "password": "wrongpass"}
        )
        assert response.status_code == 401
        assert "Incorrect username or password" in response.json()["detail"]
