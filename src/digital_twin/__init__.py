from fastapi import FastAPI
from sqlalchemy import create_engine, text

from digital_twin.config import settings
from digital_twin.models import Base
from digital_twin.database import engine

app = FastAPI()


@app.get("/")
def hello_db():
    engine = create_engine(settings.DATABASE_URL)
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version()")).scalar_one()
    return result


def main():
    print(f"Hello from {settings.PROJECT_NAME}!")
    print(f"{settings.DATABASE_URL}")
    

    Base.metadata.create_all(engine)
