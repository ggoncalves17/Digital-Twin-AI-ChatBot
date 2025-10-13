"""SQLalchemy Model for hobby."""

from unittest.mock import Base
from src.digital_twin.schemas.hobby import HobbyFrequency, HobbyType
from sqlalchemy import Column, Enum, Integer, String

class Hobby(Base):
    """SQLAlchemy model representing a hobby."""

    __tablename__ = "hobbies"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    type = Column(Enum(HobbyType), nullable=False)
    name = Column(String(100), nullable=False)
    freq = Column(Enum(HobbyFrequency), nullable=False)
    persona_id = Column(Integer, ForeignKey("personas.id"), nullable=False)
    # Add any additional fields or relationships as necessary
    

    def __repr__(self) -> str:
        return f"<Hobby(id={self.id}, type={self.type}, name={self.name}, freq={self.freq})>"