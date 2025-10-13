"""
Education data models.
"""

from datetime import date
from enum import Enum
from typing import Annotated, Callable, ClassVar

from pydantic import (
    AfterValidator,
    BaseModel,
    ConfigDict,
    Field,
    model_validator,
)
from typing_extensions import Self


class EducationLevel(str, Enum):
    """Education levels enumeration."""

    HIGHSCHOOL = "Highschool"
    BACHELOR = "Bachelor"
    MASTER = "Master"
    PHD = "PhD"


def validate_non_empty(err: str) -> Callable[[str], str]:
    def _validator(v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError(err)
        return v

    return _validator


class EducationBase(BaseModel):
    """Base education model with common fields."""

    level: EducationLevel = Field(..., description="Education level")
    course: Annotated[
        str, AfterValidator(validate_non_empty("Course name cannot be empty."))
    ] = Field(..., min_length=1, max_length=100, description="Name of the course")
    school: Annotated[
        str, AfterValidator(validate_non_empty("School name cannot be empty."))
    ] = Field(..., min_length=1, max_length=100, description="Name of the school")
    date_started: date = Field(..., description="Date when the course started")
    date_finished: date | None = Field(
        None, description="Date when the course finished"
    )
    is_graduated: bool = Field(
        ..., description="Indicates whether the user has graduated"
    )
    grade: float | None = Field(None, ge=0, le=20, description="Grade of the course")

    @model_validator(mode="after")
    def validate_is_graduated(self) -> Self:
        if self.is_graduated is True and not self.date_finished:
            raise ValueError(
                "If the user is graduated, 'date_finished' must be specified."
            )
        return self

    @model_validator(mode="after")
    def check_dates(self) -> Self:
        if self.date_finished and self.date_finished < self.date_started:
            raise ValueError("'date_finished' must be after 'date_started'.")
        return self

    model_config: ClassVar[ConfigDict] = ConfigDict(validate_assignment=True)


class EducationCreate(EducationBase):
    """Model for creating a new education."""

    pass


class EducationUpdate(BaseModel):
    """Model for updating an existing education."""

    level: EducationLevel | None = Field(None, description="Education level")
    course: Annotated[
        str | None, AfterValidator(validate_non_empty("Course name cannot be empty."))
    ] = Field(None, min_length=1, max_length=100, description="Name of the course")
    school: Annotated[
        str | None, AfterValidator(validate_non_empty("School name cannot be empty."))
    ] = Field(None, min_length=1, max_length=100, description="Name of the school")
    date_started: date | None = Field(None, description="Date when the course started")
    date_finished: date | None = Field(
        None, description="Date when the course finished"
    )
    is_graduated: bool | None = Field(
        None, description="Indicates whether the user has graduated"
    )
    grade: float | None = Field(None, ge=0, le=20, description="Grade of the course")

    @model_validator(mode="after")
    def check_dates(self) -> Self:
        if (
            self.date_started is not None
            and self.date_finished is not None
            and self.date_finished < self.date_started
        ):
            raise ValueError("'date_finished' must be after 'date_started'.")
        return self


class Education(EducationBase):
    """Model for education responses."""

    id: int = Field(..., description="Unique education ID")

    model_config: ClassVar[ConfigDict] = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "level": "Bachelor",
                    "course": "Computer Science",
                    "school": "Harvard University",
                    "date_started": "2022-10-01",
                    "date_finished": "2025-07-01",
                    "is_graduated": True,
                    "grade": 17.2,
                    "id": 1,
                },
            ]
        },
    )
