"""
Chat data models
"""

from datetime import datetime
from typing import Annotated, ClassVar

from pydantic import BaseModel, ConfigDict, Field

from digital_twin.schemas import ChatMessage


class ChatBase(BaseModel):
    """Base Chat schema."""

    created_at: datetime = Field(default=datetime.now())
    is_active: bool = Field(default=True, description="Indicates if the chat is active")


class ChatCreate(ChatBase):
    """Chat creation schema."""

    user_id: int = Field(gt=0, description="User's ID")
    persona_id: int = Field(gt=0, description="Persona's ID")


class ChatUpdate(BaseModel):
    """Chat update schema."""

    is_active: bool | None = Field(None, description="Indicates if the chat is active")


class Chat(ChatBase):
    """Chat response schema."""

    id: Annotated[int, Field(description="Unique Chat ID")]
    messages: list[ChatMessage] = Field(description="Chat's message history")

    model_config: ClassVar[ConfigDict] = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example" : {
                "id": 1,
                "is_active": True,
                "messages": [],
            }
        },
    )
