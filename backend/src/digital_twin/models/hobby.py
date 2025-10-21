"""SQLalchemy Model for hobby."""

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from digital_twin.models import Base

if TYPE_CHECKING:
    from digital_twin.models import Persona


class Hobby(Base):
    """SQLAlchemy model representing a hobby."""

    __tablename__ = "hobbies"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(100), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    freq: Mapped[str] = mapped_column(String(100), nullable=False)

    persona_id: Mapped[int] = mapped_column(ForeignKey("personas.id"))

    persona: Mapped["Persona"] = relationship(back_populates="hobbies")

    def __repr__(self) -> str:
        return f"<Hobby(id={self.id}, type={self.type}, name={self.name}, freq={self.freq}, persona_id={self.persona_id})>"
