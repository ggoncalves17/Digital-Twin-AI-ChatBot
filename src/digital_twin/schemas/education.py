"""
Education data models.
"""

from datetime import date
from pydantic import BaseModel, Field, field_validator, model_validator
from enum import Enum
from typing import Optional
from typing_extensions import Self

class EducationLevel(str, Enum):

    """Education levels enumeration."""

    HIGHSCHOOL = "Highschool"
    BACHELOR = "Bachelor"
    MASTER = "Master"
    PHD = "PhD"

class Education(BaseModel):

    """Education information model."""

    level : EducationLevel = Field(..., description="Education level")
    course : str = Field(..., min_length=1, max_length=100, description="Name of the course")
    school : str = Field(..., min_length=1, max_length=100, description="Name of the school")
    date_started : date = Field(..., description="Date when the course started")
    date_finished : Optional[date] = Field(None, description="Date when the course finished")
    is_graduated: bool = Field(..., description="Indicates whether the user has graduated")

    @field_validator('course')
    def validate_course(cls, v : str) -> str:
        if len(v.strip()) == 0:
            raise ValueError("Course name cannot be empty.")
        return v

    @field_validator('school')
    def validate_school(cls, v : str) -> str:
        if len(v.strip()) == 0:
            raise ValueError("School name cannot be empty.")
        return v

    @model_validator(mode='after')
    def validate_is_graduated(self) -> Self:
        if self.is_graduated is True and not self.date_finished:
            raise ValueError("If the user is graduated, 'date_finished' must be specified.")
        return self
    
    @model_validator(mode='after')
    def check_dates(self) -> Self:
        if self.date_finished and self.date_finished < self.date_started:
            raise ValueError("'date_finished' must be after 'date_started'.")
        return self
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "level": "Bachelor",
                    "course": "Computer Science",
                    "school": "Harvard University",
                    "date_started": "2022-10-01",
                    "date_finished": "2025-07-01",
                    "is_graduated": True
                },
                {
                    "level": "Master",
                    "course": "Data Science",
                    "school": "MIT",
                    "date_started": "2023-09-01",
                    "is_graduated": False
                }
            ]
        }
    }
