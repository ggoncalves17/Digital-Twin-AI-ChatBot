"""
Persona SQLAlchemy model.
"""

from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import date
from typing import TYPE_CHECKING, List
from sqlalchemy import String
from digital_twin.models import Base

if TYPE_CHECKING:
    from digital_twin.models import Education, Occupation, Hobby


class Persona(Base):
    """SQLAlchemy model for the Persona entity."""

    __tablename__ = "personas"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    birthdate: Mapped[date] = mapped_column(nullable=False)
    gender: Mapped[str] = mapped_column(String(100), nullable=False)
    nationality: Mapped[str] = mapped_column(String(100), nullable=False)

    educations: Mapped[List["Education"]] = relationship(back_populates="persona")
    occupations: Mapped[List["Occupation"]] = relationship(back_populates="persona")
    hobbies: Mapped[List["Hobby"]] = relationship(back_populates="persona")

    def __repr__(self):
        return f"<Persona(id={self.id}, name='{self.name}', birthdate='{self.birthdate}, nationality={self.nationality}')>"
