"""SQLalchemy Model for hobby."""

from src.digital_twin.schemas.hobby import HobbyFrequency, HobbyType
from sqlalchemy import Column, Integer, String, Base, ForeignKey, relationship

class Hobby(Base):
    """SQLAlchemy model representing a hobby."""

    __tablename__ = "hobbies"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    type = Column(String(100), nullable=False)
    name = Column(String(100), nullable=False)
    freq = Column(String(100), nullable=False)
    persona_id = Column(Integer, ForeignKey("personas.id"), nullable=False)
    persona = relationship("Persona", back_populates="hobbies")
    # Add any additional fields or relationships as necessary
    

    def __repr__(self) -> str:
        return f"<Hobby(id={self.id}, type={self.type}, name={self.name}, freq={self.freq}, persona_id={self.persona_id})>"