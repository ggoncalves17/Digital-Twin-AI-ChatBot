from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.logger import logger
from sqlalchemy.orm import Session

from digital_twin.schemas.chat_message import ChatMessage
from digital_twin.schemas.chat import Chat
from digital_twin.database import get_db
from digital_twin.schemas.user import Token, User, UserCreate, UserLogin
from digital_twin.services.user import UserService
from digital_twin.utils.security import create_access_token, get_current_user

router = APIRouter(prefix="/users", tags=["user"])


@router.post("/register", status_code=status.HTTP_204_NO_CONTENT)
def add_user(new_user: UserCreate, db: Annotated[Session, Depends(get_db)]):
    success = UserService.add_user(db, new_user)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Email already in use. Try another one."
        )

@router.post("/login", response_model=Token)
def authenticate_user(user: UserLogin, db: Annotated[Session, Depends(get_db)]):
    user = UserService.authenticate_user(db, user)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Credentials invalid. Try again."
        )
    
    access_token = create_access_token(data={"sub": user.email})

    return Token(access_token=access_token, token_type="bearer")

@router.get("/profile")
def get_profile(current_user: User = Depends(get_current_user)) -> User:
    return current_user

@router.get("/{id}/chats/{persona_id}")
def get_chats(id: int, persona_id: int, db: Annotated[Session, Depends(get_db)], current_user: User = Depends(get_current_user)) -> list[ChatMessage] | None:

    chat = UserService.get_user_persona_chats(id, persona_id, db)

    if chat is None:
        return None
    
    return UserService.get_user_persona_chat_history(chat.id, db)
