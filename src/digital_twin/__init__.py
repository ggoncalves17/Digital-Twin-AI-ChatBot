from datetime import datetime
from typing import Any

from fastapi import FastAPI
from sqlalchemy import text

from digital_twin.config import settings
from digital_twin.database import engine
from digital_twin.models import Base


def create_app() -> FastAPI:
    return FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.DESCRIPTION,
        version=settings.VERSION,
        license_info=settings.LICENSE,
    )


# Instantiate FastAPI
app = create_app()

# TODO include routers


@app.get("/db")
def db_version():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version()")).scalar_one()
    return result


# Root endpoints
@app.get("/")
def root() -> dict[str, Any]:
    return {
        "message": "Welcome to the Digital Twin's API",
        "api_version": settings.VERSION,
        "api_route": settings.API_V1_STR,
        "docs": "/docs",
        "redoc": "/redoc",
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/health")
def health_check() -> dict[str, Any]:
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


def main():
    print(f"Hello from {settings.PROJECT_NAME}!")
    print(f"{settings.DATABASE_URL}")

    Base.metadata.create_all(engine)
