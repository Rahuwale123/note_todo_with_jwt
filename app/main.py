from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import auth, organizations, notes, todos
from app.database import engine
from app.models import base

base.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.project_name,
    openapi_url=f"{settings.api_v1_str}/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix=settings.api_v1_str)
app.include_router(organizations.router, prefix=settings.api_v1_str)
app.include_router(notes.router, prefix=settings.api_v1_str)
app.include_router(todos.router, prefix=settings.api_v1_str)


@app.get("/")
def read_root():
    return {
        "message": "FastAPI Backend API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
