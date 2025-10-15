from datetime import date
from enum import StrEnum
from typing import Annotated, ClassVar

from pydantic import AfterValidator, BaseModel, ConfigDict, Field

from digital_twin.schemas import Education, Hobby, Occupation


class GenderEnum(StrEnum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"


def validate_birthdate(v: date) -> date:
    if date.today() < v:
        raise ValueError("Birthdate cannot be in the future.")
    return v


class PersonaBase(BaseModel):
    """Base Persona schema."""

    name: str = Field(min_length=1, max_length=100, description="Persona's name")
    birthdate: Annotated[date, AfterValidator(validate_birthdate)] = Field(
        description="Persona's birthdate"
    )
    gender: GenderEnum = Field(description="Persona's gender")
    nationality: str = Field(description="Persona's nationality")


class PersonaCreate(PersonaBase):
    """Persona creation schema."""

    pass


class PersonaUpdate(BaseModel):
    """Persona update schema."""

    name: str | None = Field(
        None, min_length=1, max_length=100, description="Persona name"
    )
    birthdate: Annotated[date | None, AfterValidator(validate_birthdate)] = Field(None)
    gender: GenderEnum | None = Field(None)
    nationality: str | None = Field(None)
    education: list[Education] | None = Field(None)
    occupations: list[Occupation] | None = Field(None)
    hobbies: list[Hobby] | None = Field(None)


class Persona(PersonaBase):
    """Persona response schema."""

    id: Annotated[int, Field(description="Unique Persona ID")]
    educations: list[Education] = Field(description="Persona's academic career")
    occupations: list[Occupation] = Field(description="Persona's work experience")
    hobbies: list[Hobby] = Field(description="Persona's hobbies")

    model_config: ClassVar[ConfigDict] = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "John Doe",
                "birthdate": "2000-01-31",
                "gender": "Male",
                "nationality": "Portuguese",
                "education": [],
                "occupations": [],
                "hobbies": [],
            }
        },
    )
