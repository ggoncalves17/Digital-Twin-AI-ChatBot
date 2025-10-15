from fastapi import HTTPException
from sqlalchemy.orm import Session

from digital_twin.models.hobby import Hobby
from digital_twin.schemas.hobby import HobbyCreate, HobbyUpdate
from digital_twin.services.persona import PersonaService


class HobbyService:
    """Hobby abstraction layer between ORM and API endpoints."""

    @staticmethod
    def create_hobby(db: Session, hobby: HobbyCreate) -> Hobby:
        new_hobby = Hobby(**hobby.model_dump())
        db.add(new_hobby)
        db.commit()
        db.refresh(new_hobby)
        return new_hobby

    @staticmethod
    def get_hobby(db: Session, hobby_id: int) -> Hobby | None:
        return db.query(Hobby).filter(Hobby.id == hobby_id).first()

    @staticmethod
    def get_hobbies_by_persona(db: Session, persona_id: int) -> list[Hobby] | None:
        if not PersonaService.get_persona(db, persona_id):
            return None
        return db.query(Hobby).filter(Hobby.persona_id == persona_id).order_by(Hobby.id).all()

    @staticmethod
    def update_hobby(db: Session, id: int, update: HobbyUpdate) -> Hobby | None:
        hobby = db.query(Hobby).filter(Hobby.id == id).first()
        if hobby:
            for k, v in update.model_dump(exclude_unset=True).items():
                setattr(hobby, k, v)
            db.commit()
            db.refresh(hobby)

        return hobby

    @staticmethod
    def delete_hobby(db: Session, id: int) -> bool:
        hobby = db.query(Hobby).filter(Hobby.id == id).first()
        if not hobby:
            return False

        db.delete(hobby)
        db.commit()
        return True

