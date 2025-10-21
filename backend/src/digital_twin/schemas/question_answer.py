"""
Question data models
"""

from enum import Enum
from pydantic import BaseModel, ConfigDict, Field, field_validator


class QABase(BaseModel):
    """Data model representing a question"""

    question : str = Field(..., min_length=1, max_length=250, description="Question text")
    

    @field_validator('question')
    @classmethod
    def validate_question(cls, v: str) -> str:
        if v is not None and not v.strip():
            raise ValueError("Question cannot be empty.")
        return v.strip() if v else v
    

class QACreate(QABase):
    """Data model for questioning llm"""

    persona_id: int = Field(gt=0)