"""
Occupation SQLAlchemy model.
"""

from datetime import date
from sqlalchemy import Integer, String, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""
    pass


class Occupation(Base):
    """SQLAlchemy model for the Occupation entity."""

    __tablename__ = "occupations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    position: Mapped[str] = mapped_column(String(100), nullable=False)
    workplace: Mapped[str] = mapped_column(String(100), nullable=False)
    date_started: Mapped[date] = mapped_column(Date, nullable=False)
    date_finished: Mapped[date | None] = mapped_column(Date, nullable=True)

    def __repr__(self) -> str:
        return (
            f"<Occupation(id={self.id}, position='{self.position}', "
            f"workplace='{self.workplace}', "
            f"date_started={self.date_started}, date_finished={self.date_finished})>"
        )
