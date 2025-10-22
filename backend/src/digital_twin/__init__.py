from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any

import alembic.command
from alembic.config import Config
from fastapi import APIRouter, FastAPI
from sqlalchemy import text

from digital_twin.config import settings
from digital_twin.database import engine
from digital_twin.routers import (
    educations,
    hobbies,
    occupations,
    personas,
    users,
)

from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    alembic_cfg = Config("./alembic.ini")
    alembic.command.upgrade(alembic_cfg, "head")
    yield


def create_app() -> FastAPI:
    return FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.DESCRIPTION,
        version=settings.VERSION,
        license_info=settings.LICENSE,
        lifespan=lifespan
    )


# Instantiate FastAPI
app = create_app()

# TODO include routers
router = APIRouter(prefix=settings.API_V1_STR)
router.include_router(educations.router)
router.include_router(hobbies.router)
router.include_router(occupations.router)
router.include_router(personas.router)
router.include_router(users.router)
app.include_router(router)

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    import uvicorn

    uvicorn.run("digital_twin:app", host="0.0.0.0", port=8000, reload=True)
