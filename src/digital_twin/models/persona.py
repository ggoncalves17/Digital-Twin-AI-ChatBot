from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import date
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, String

if TYPE_CHECKING:
    from digital_twin.models import Base, Education, Occupation, Hobby

class Persona(Base):
    __tablename__ = 'personas'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    birthdate: Mapped[date] = mapped_column(nullable=False)
    gender: Mapped[str] = mapped_column(String(100), nullable=False)
    nationality: Mapped[str] = mapped_column(String(100), nullable=False)

    educations: Mapped["Education"] = relationship(back_populates="persona")
    occupations: Mapped["Occupation"] = relationship(back_populates="persona")
    hobbies: Mapped["Hobby"] = relationship(back_populates="persona")

    def __repr__(self):
        return f"<Persona(id={self.id}, name='{self.name}', birthdate='{self.birthdate}, nationality={self.nationality}')>"