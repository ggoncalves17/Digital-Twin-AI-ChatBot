from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import date
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, String

if TYPE_CHECKING:
    from digital_twin.models import Base, Persona

class Education(Base):
    __tablename__ = 'educations'

    id: Mapped[int] = mapped_column(primary_key=True)
    level: Mapped[str] = mapped_column(nullable=False)
    course: Mapped[str] = mapped_column(String(100), nullable=False)
    school: Mapped[str] = mapped_column(String(100), nullable=False)
    date_started: Mapped[date] = mapped_column(nullable=False)
    date_finished: Mapped[date] = mapped_column()
    is_graduated: Mapped[bool] = mapped_column(nullable=False)
    grade: Mapped[float] = mapped_column()

    persona_id: Mapped[int] = mapped_column(ForeignKey("personas.id"))

    persona: Mapped["Persona"] = relationship(back_populates="educations")

    def __repr__(self):
        return f"<Education(id={self.id}, level='{self.level}', course='{self.course}, school={self.school}')>"