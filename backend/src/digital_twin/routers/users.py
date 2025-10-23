from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from digital_twin.database import get_db
from digital_twin.schemas.chat_message import ChatMessage, ChatMessageCreate
from digital_twin.schemas.user import Token, User, UserCreate, UserLogin
from digital_twin.services.chat import ChatService
from digital_twin.services.user import UserService
from digital_twin.utils.lakehouse_export import export_data
from digital_twin.utils.security import create_access_token, get_current_user

router = APIRouter(prefix="/users", tags=["user"])


@router.post("/register", status_code=status.HTTP_204_NO_CONTENT)
def add_user(new_user: UserCreate, db: Annotated[Session, Depends(get_db)]):
    success = UserService.add_user(db, new_user)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email already in use. Try another one.",
        )


@router.post("/login", response_model=Token)
def authenticate_user(user: UserLogin, db: Annotated[Session, Depends(get_db)]):
    user = UserService.authenticate_user(db, user)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Credentials invalid. Try again.",
        )

    access_token = create_access_token(data={"sub": user.email})

    return Token(access_token=access_token, token_type="bearer")


@router.get("/profile")
def get_profile(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    return current_user


@router.get("/{id}/chats/{persona_id}")
def get_chats(
    id: int,
    persona_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> list[ChatMessage] | None:
    chat = ChatService.get_user_persona_chats(id, persona_id, db)

    if chat is None:
        return None

    return ChatService.get_user_persona_chat_history(chat.id, db)


@router.post("/{id}/chats/{persona_id}")
def add_chat_message(
    id: int,
    persona_id: int,
    message: ChatMessageCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    chat = ChatService.get_user_persona_chats(id, persona_id, db)

    if chat is None:
        chat = ChatService.create_chat_persona(id, persona_id, db)
        if not chat:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create a new chat with the specified persona.",
            )

    new_message = ChatService.add_chat_persona_message(chat.id, message, db)
    if not new_message:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add the user's message to the chat.",
        )

    result = ChatService.generate_chat_response(new_message.content, persona_id, db)
    if not result:
        export_data(
            "chat",
            {
                "event": "question_asked",
                "status": "error",
                "description": f"Persona with ID {persona_id} does not exist",
            }
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate a response from the persona.",
        )

    # TODO log tokens used in LLM invocation
    export_data(
        "chat",
        {
            "event": "question_asked",
            "status": "success",
            "persona_id": persona_id,
            "user_id": id,
            "question": message.content,
            # "input_tokens": result.usage_metadata["input_tokens"],
            # "output_tokens": result.usage_metadata["output_tokens"],
            # "total_tokens": result.usage_metadata["total_tokens"]
        }
    )

    assistant_message = ChatMessageCreate(role="Assistant", content=result["output"])
    new_response = ChatService.add_chat_persona_message(chat.id, assistant_message, db)

    if not new_response:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to store the assistant's response in the chat.",
        )

    return new_response
