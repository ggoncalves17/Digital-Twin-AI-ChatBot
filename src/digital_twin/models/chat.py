"""
Chat SQLAlchemy model.
"""

from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, String
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from digital_twin.models import Base

if TYPE_CHECKING:
    from digital_twin.models import User, Persona, ChatMessage


class Chat(Base):
    """SQLAlchemy model for the Chat entity."""

    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(primary_key=True)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    persona_id: Mapped[int] = mapped_column(ForeignKey("personas.id"))

    user: Mapped["User"] = relationship(back_populates="chats")
    persona: Mapped["Persona"] = relationship(back_populates="chats")
    messages: Mapped[List["ChatMessage"]] = relationship(back_populates="chat")

    def __repr__(self):
        return f"<Chat(id={self.id}, name='{self.name}', is_active='{self.is_active}, created_at={self.created_at}')>"
