from datetime import date, datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from digital_twin.models.occupation import Occupation
from digital_twin.schemas.occupation import OccupationCreate, OccupationUpdate


def input_date(prompt: str) -> date:
    while True:
        try:
            d = input(prompt)
            return datetime.strptime(d, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid format. Use YYYY-MM-DD.")

def get_occupation_by_id(db: Session, occupation_id: int) -> Occupation:
    occupation = db.query(Occupation).filter(Occupation.id == occupation_id).first()
    if not occupation:
        raise HTTPException(status_code=404, detail="Occupation not found")
    return occupation

def create_new_occupation(db: Session, occupation: OccupationCreate) -> Occupation:
    existing_occupation = db.query(Occupation).filter(Occupation.name == occupation.name).first()
    if existing_occupation:
        raise HTTPException(status_code=400, detail="Occupation already registered")

    new_occupation = Occupation(
        position=occupation.position,
        workplace=occupation.workplace,
        date_started=occupation.date_started,
        date_finished=occupation.date_finished,
        persona_id=occupation.persona_id
    )
    db.add(new_occupation)
    db.commit()
    db.refresh(new_occupation)
    return new_occupation

def list_all_occupations(db: Session) -> list[Occupation]:
    return db.query(Occupation).all()

def update_occupation(db: Session, occupation_id: int, update: OccupationUpdate) -> Occupation:
    occupation = get_occupation_by_id(db, occupation_id)
    if not occupation:
        raise HTTPException(status_code=404, detail="Occupation not found")

    update_data = update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(occupation, field, value)

    db.commit()
    db.refresh(occupation)
    return occupation

def delete_occupation(db: Session, occupation_id: int) -> None:
    occupation = get_occupation_by_id(db, occupation_id)
    if not occupation:
        raise HTTPException(status_code=404, detail="Occupation not found")
    db.delete(occupation)
    db.commit()