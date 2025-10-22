from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from digital_twin.schemas.chat_message import ChatMessageCreate
from digital_twin.models.chat_message import ChatMessage
from digital_twin.models.chat import Chat
from digital_twin.models.user import User
from digital_twin.schemas.user import UserCreate, UserLogin
from digital_twin.models.chat import Chat

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
    
    @staticmethod
    def get_user_persona_chats(id: int , persona_id: int, db: Session) -> Chat | None:
        return db.query(Chat).filter(Chat.user_id == id, Chat.persona_id == persona_id, Chat.is_active == True).first()

    @staticmethod
    def get_user_persona_chat_history(chat_id: int, db: Session) -> list[ChatMessage]:
        return db.query(ChatMessage).filter(ChatMessage.chat_id == chat_id).all()
    
    @staticmethod
    def create_chat_persona(id: int , persona_id: int, db: Session) -> Chat | None:

        new_chat = Chat(user_id=id, persona_id=persona_id)

        try:
            db.add(new_chat)
        except IntegrityError:
            return None
        db.commit()
        db.refresh(new_chat)
        
        return new_chat
    
    @staticmethod
    def add_chat_persona_message(chat_id: int, message: ChatMessageCreate, db: Session) -> ChatMessage | None:

        new_message = ChatMessage(**message.model_dump(), chat_id=chat_id)

        try:
            db.add(new_message)
        except IntegrityError:
            return None
        db.commit()
        db.refresh(new_message)
        
        return new_message
    
