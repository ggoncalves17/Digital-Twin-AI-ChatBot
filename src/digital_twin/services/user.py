from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from digital_twin.models.user import User
from digital_twin.schemas.user import UserCreate, UserLogin

from digital_twin.utils.security import hash_password, verify_password

class UserService:
    """User abstraction layer between ORM and API endpoints."""

    @staticmethod
    def add_user(db: Session, user: UserCreate) -> User | None:

        user.password = hash_password(user.password)

        new_user = User(**user.model_dump())

        if UserService.get_user_email(db, new_user.email):
            return None
        else:
            try:
                db.add(new_user)
            except IntegrityError:
                return None
            db.commit()
            db.refresh(new_user)
            return new_user
    
    @staticmethod
    def authenticate_user(db: Session, user: UserLogin) -> User | bool:
        new_user = UserService.get_user_email(db, user.email)

        if not new_user or not verify_password(user.password, new_user.password):
            return False
        
        return new_user

    @staticmethod
    def get_user_email(db: Session, email: str) -> User | None:
        return (
            db.query(User)
            .options(
                joinedload(User.chats),
            )
            .filter(User.email == email)
            .first()
        )
    
    @staticmethod
    def get_user(db: Session, id: int) -> User | None:
        return (
            db.query(User)
            .options(
                joinedload(User.chats),
            )
            .filter(User.id == id)
            .first()
        )

    @staticmethod
    def get_users(db: Session) -> list[User]:
        return db.query(User).order_by(User.id).all()
