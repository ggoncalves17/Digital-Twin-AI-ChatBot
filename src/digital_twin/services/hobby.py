from fastapi import HTTPException
from sqlalchemy.orm import Session

from digital_twin.models.hobby import Hobby
from digital_twin.schemas.hobby import HobbyUpdate

# Mock database
DBHobby: list[Hobby] = list()

def get_hobby_by_id(db: Session, hobby_id: int) -> Hobby:
    hobby = db.query(DBHobby).filter(DBHobby.id == hobby_id).first()
    if not hobby:
        raise HTTPException(status_code=404, detail="Hobby not found")
    return hobby

def create_new_hobby(db: Session, hobby: Hobby) -> Hobby:
    existing_hobby = db.query(DBHobby).filter(DBHobby.name == hobby.name).first()
    if existing_hobby:
        raise HTTPException(status_code=400, detail="Hobby already registered")

    new_hobby = DBHobby(
        type=hobby.type,
        name=hobby.name,
        freq=hobby.freq,
        persona_id=hobby.persona_id,
    )
    db.add(new_hobby)
    db.commit()
    db.refresh(new_hobby)
    return new_hobby

def list_all_hobbys(db: Session) -> list[Hobby]:
    return db.query(DBHobby).all()

def update_hobby(db: Session, hobby_id: int, update: HobbyUpdate) -> Hobby:
    hobby = get_hobby_by_id(db, hobby_id)
    if not hobby:
        raise HTTPException(status_code=404, detail="Hobby not found")

    update_data = update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(hobby, field, value)

    db.commit()
    db.refresh(hobby)
    return hobby

def delete_hobby(db: Session, hobby_id: int) -> None:
    hobby = get_hobby_by_id(db, hobby_id)
    if not hobby:
        raise HTTPException(status_code=404, detail="Hobby not found")
    db.delete(hobby)
    db.commit()