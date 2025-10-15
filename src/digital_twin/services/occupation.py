from datetime import date, datetime

from sqlalchemy.orm import Session

from digital_twin.models.occupation import Occupation
from digital_twin.schemas.occupation import OccupationCreate, OccupationUpdate
from digital_twin.services.persona import PersonaService


def input_date(prompt: str) -> date:
    while True:
        try:
            d = input(prompt)
            return datetime.strptime(d, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid format. Use YYYY-MM-DD.")


class OccupationService:
    """Occupation abstraction layer between ORM and API endpoints."""

    @staticmethod
    def create_occupation(db: Session, occupation: OccupationCreate) -> Occupation:
        new_occupation = Occupation(**occupation.model_dump())
        db.add(new_occupation)
        db.commit()
        db.refresh(new_occupation)
        return new_occupation

    @staticmethod
    def get_occupation(db: Session, id: int) -> Occupation | None:
        return db.query(Occupation).filter(Occupation.id == id).first()

    @staticmethod
    def get_occupations_by_persona(db: Session, persona_id: int) -> list[Occupation] | None:
        if not PersonaService.get_persona(db, persona_id):
            return None
        return (
            db.query(Occupation)
            .filter(Occupation.persona_id == persona_id)
            .order_by(Occupation.date_started)
            .all()
        )

    @staticmethod
    def update_occupation(
        db: Session, id: int, update: OccupationUpdate
    ) -> Occupation | None:
        occupation = db.query(Occupation).filter(Occupation.id == id).first()
        if occupation:
            for k, v in update.model_dump(exclude_unset=True).items():
                setattr(occupation, k, v)
            db.commit()
            db.refresh(occupation)

        return occupation

    @staticmethod
    def delete_occupation(db: Session, id: int) -> bool:
        occupation = db.query(Occupation).filter(Occupation.id == id).first()
        if not occupation:
            return False

        db.delete(occupation)
        db.commit()
        return True
