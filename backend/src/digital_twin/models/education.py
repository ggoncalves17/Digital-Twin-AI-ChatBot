"""
Education SQLAlchemy model.
"""

from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from digital_twin.models import Base

if TYPE_CHECKING:
    from digital_twin.models import Persona


class Education(Base):
    """SQLAlchemy model for the Education entity."""

    __tablename__ = "educations"

    id: Mapped[int] = mapped_column(primary_key=True)
    level: Mapped[str] = mapped_column(nullable=False)
    course: Mapped[str] = mapped_column(String(100), nullable=False)
    school: Mapped[str] = mapped_column(String(100), nullable=False)
    date_started: Mapped[date] = mapped_column(Date, nullable=False)
    date_finished: Mapped[date] = mapped_column(nullable=True)
    is_graduated: Mapped[bool] = mapped_column(nullable=False)
    grade: Mapped[float] = mapped_column()

    persona_id: Mapped[int] = mapped_column(ForeignKey("personas.id"))

    persona: Mapped["Persona"] = relationship(back_populates="educations")

    def __repr__(self):
        return f"<Education(id={self.id}, level='{self.level}', course='{self.course}, school={self.school}')>"
