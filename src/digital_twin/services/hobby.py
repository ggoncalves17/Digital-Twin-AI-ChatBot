from sqlalchemy.orm import Session, joinedload

from digital_twin.models.hobby import Hobby
from digital_twin.schemas.hobby import HobbyCreate, HobbyUpdate


class HobbyService:
    @staticmethod
    def create_hobby(db: Session, hobby: HobbyCreate) -> Hobby:
        db_hobby = Hobby(**hobby.model_dump())
        db.add(db_hobby)
        db.commit()
        db.refresh(db_hobby)
        return db_hobby

    @staticmethod
    def get_hobby(db: Session, id: int) -> Hobby | None:
        return db.query(Hobby).options(joinedload(Hobby.persona)).filter(Hobby.id == id).first()

    @staticmethod
    def get_hobbies(db: Session) -> list[Hobby]:
        return db.query(Hobby).order_by(Hobby.id.asc()).all()

    @staticmethod
    def update_hobby(db: Session, id: int, hobby_update: HobbyUpdate) -> Hobby | None:
        hobby = db.query(Hobby).filter(Hobby.id == id).first()
        if not hobby:
            return None

        update_data = hobby_update.model_dump(exclude_unset=True)
        for k,v in update_data.items():
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
