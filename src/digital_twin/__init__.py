from digital_twin.config import settings
from digital_twin.models import Base
from digital_twin.database import engine


def main():
    print(f"Hello from {settings.PROJECT_NAME}!")

    Base.metadata.create_all(engine)
