"""SQLalchemy Model for hobby."""

from src.digital_twin.schemas.hobby import HobbyFrequency, HobbyType
from sqlalchemy import Column, Integer, String, DeclaritiveBase, ForeignKey, relationship

class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""
    pass

class Hobby(Base):
    """SQLAlchemy model representing a hobby."""

    __tablename__ = "hobbies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    type: Mapped[str] = mapped_column(String(100), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    freq: Mapped[str] = mapped_column(String(100), nullable=False)
    persona_id: Mapped[int] = mapped_column(Integer, ForeignKey("personas.id"), nullable=False)
    persona: Mapped["Persona"] = relationship("Persona", back_populates="hobbies")
    # Add any additional fields or relationships as necessary
    

    def __repr__(self) -> str:
        return f"<Hobby(id={self.id}, type={self.type}, name={self.name}, freq={self.freq}, persona_id={self.persona_id})>"