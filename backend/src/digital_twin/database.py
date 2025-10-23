
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from digital_twin.config import settings

engine = create_engine(settings.DATABASE_URL)

Session = sessionmaker(bind=engine)


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
