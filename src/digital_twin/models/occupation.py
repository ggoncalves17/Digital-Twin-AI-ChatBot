"""
Occupation SQLAlchemy model.
"""

from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import date
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, String, Integer, Date


if TYPE_CHECKING:
    from digital_twin.models import Base, Persona

class Occupation(Base):
    """SQLAlchemy model for the Occupation entity."""

    __tablename__ = "occupations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    position: Mapped[str] = mapped_column(String(100), nullable=False)
    workplace: Mapped[str] = mapped_column(String(100), nullable=False)
    date_started: Mapped[date] = mapped_column(Date, nullable=False)
    date_finished: Mapped[date | None] = mapped_column(Date, nullable=True)

    persona_id: Mapped[int] = mapped_column(ForeignKey("personas.id"))

    persona: Mapped["Persona"] = relationship(back_populates="occupations")

    def __repr__(self) -> str:
        return (
            f"<Occupation(id={self.id}, position='{self.position}', "
            f"workplace='{self.workplace}', "
            f"date_started={self.date_started}, date_finished={self.date_finished})>"
        )
