"""
ChatMessage data models.
"""

from datetime import datetime
from enum import Enum
from typing import Annotated, Callable, ClassVar

from pydantic import (
    AfterValidator,
    BaseModel,
    ConfigDict,
    Field,
)


def validate_non_empty(err: str) -> Callable[[str], str]:
    def _validator(v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError(err)
        return v

    return _validator


class ChatMessageRole(str, Enum):
    """ChatMessage roles enumeration."""

    USER = "User"
    ASSISTANT = "Assistant"


class ChatMessageBase(BaseModel):
    """Base ChatMessage model with common fields."""

    role: ChatMessageRole = Field(..., description="Role of the chat message")
    content: Annotated[
        str, AfterValidator(validate_non_empty("Chat message content cannot be empty."))
    ] = Field(..., min_length=1, description="Content of the chat message")
    created_at: datetime = Field(default=datetime.now())

    model_config: ClassVar[ConfigDict] = ConfigDict(validate_assignment=True)


class ChatMessageCreate(ChatMessageBase):
    """Model for creating a new ChatMessage."""

    chat_id: int = Field(gt=0, description="ID of the chat this message belongs to")


class ChatMessageUpdate(BaseModel):
    """Model for updating an existing Chat Message."""

    pass


class ChatMessage(ChatMessageBase):
    """Model for ChatMessage responses."""

    id: int = Field(..., description="Unique chat message ID")

    model_config: ClassVar[ConfigDict] = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example" : {
                "role": "User",
                "content": "Hello, how are you?",
                "created_at": "2025-01-01T18:30:00",
                "id": 1,
            },   
        },
    )
