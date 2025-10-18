"""
User SQLAlchemy model.
"""

from datetime import date
from typing import TYPE_CHECKING, List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from digital_twin.models import Base

if TYPE_CHECKING:
    from digital_twin.models import Chat


class User(Base):
    """SQLAlchemy model for the User entity."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    birthdate: Mapped[date] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    chats: Mapped[List["Chat"]] = relationship(back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', birthdate='{self.birthdate}, email={self.email}')>"
