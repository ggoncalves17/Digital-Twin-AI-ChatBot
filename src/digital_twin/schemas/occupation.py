"""
Occupation data models.
"""

from datetime import date
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional
from typing_extensions import Self

class OccupationBase(BaseModel):

    """Base Occupation model with common fields."""

    position : str = Field(..., min_length=1, max_length=100, description="Title of the position")
    workplace : str = Field(..., min_length=1, max_length=100, description="Name of the company")
    date_started : date = Field(..., description="Date when the job started")
    date_finished : Optional[date] = Field(None, description="Date when stopped working")

    @field_validator('position')
    def validate_position(cls, v : str) -> str:
        if not v.strip():
            raise ValueError("Position name cannot be empty.")
        return v.strip()

    @field_validator('workplace')
    def validate_workplace(cls, v : str) -> str:
        if not v.strip():
            raise ValueError("Workplace name cannot be empty.")
        return v.strip()
    
    @model_validator(mode='after')
    def check_dates(self) -> Self:
        if self.date_finished and self.date_finished < self.date_started:
            raise ValueError("date_finished must be after date_started.")
        return self
    
class OccupationCreate(OccupationBase):
    """Model for creating a new Occupation."""
    pass

class OccupationUpdate(BaseModel):
    """Model for updating an existing Occupation."""

    position : Optional[str] = Field(None, min_length=1, max_length=100, description="Title of the position")
    workplace : Optional[str] = Field(None, min_length=1, max_length=100, description="Name of the company")
    date_started : Optional[date] = Field(None, description="Date when the job started")
    date_finished : Optional[date] = Field(None, description="Date when stopped working")
    
    @field_validator('position')
    def validate_position(cls, v : str) -> str:
        if v is not None and not v.strip():
            raise ValueError("Position name cannot be empty.")
        return v.strip()

    @field_validator('workplace')
    def validate_workplace(cls, v : str) -> str:
        if v is not None and not v.strip():
            raise ValueError("Workplace name cannot be empty.")
        return v.strip()
    @model_validator(mode='after')
    def check_dates(self) -> Self:
        if self.date_started and self.date_finished and self.date_finished < self.date_started:
            raise ValueError("date_finished must be after date_started.")
        return self
    

class Occupation(OccupationBase):
    """Model for occupation responses."""

    id: int = Field(..., description="Occupation ID")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "position": "Junior Dev",
                    "workplace": "Loop Co.",
                    "date_started": "2019-09-09",
                    "date_finished": "2025-10-01"
                },
            ]
        }
    }