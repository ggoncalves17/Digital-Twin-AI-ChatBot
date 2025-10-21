"""
ChatMessage SQLAlchemy model.
"""

from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, String
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from digital_twin.models import Base

if TYPE_CHECKING:
    from digital_twin.models import Chat


class ChatMessage(Base):
    """SQLAlchemy model for the ChatMessage entity."""

    __tablename__ = "chat_messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    role: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)

    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"))

    chat: Mapped["Chat"] = relationship(back_populates="messages")

    def __repr__(self):
        return f"<ChatMessage(id={self.id}, role='{self.role}', content='{self.content}, created_at={self.created_at}')>"
