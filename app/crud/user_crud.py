from datetime import date, datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.users import User, UserRegistration
from app.database import User as DBUser
import bcrypt
import getpass

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def input_date(prompt: str) -> date:
    while True:
        try:
            d = input(prompt)
            return datetime.strptime(d, "%Y-%m-%d").date()
        except ValueError:
            print("Formato inválido. Usa YYYY-MM-DD.")

def create_user_from_data(db: Session, user: UserRegistration) -> DBUser:
    existing_user = db.query(DBUser).filter(DBUser.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email já registado")

    hashed_password = hash_password(user.password)

    new_user = DBUser(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=hashed_password,
        date_of_birth=user.date_of_birth,
        total_messages=user.total_messages or 0
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

