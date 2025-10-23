from typing import Any

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from digital_twin.services.agent_executor import get_agent_executor
from digital_twin.utils.persona_format import (
    format_education,
    format_hobbies,
    format_occupations,
)
from digital_twin.models.chat import Chat
from digital_twin.models.chat_message import ChatMessage
from digital_twin.schemas.chat_message import ChatMessageCreate
from digital_twin.services.persona import PersonaService
from digital_twin.services.multi_agent_supervisor_pattern import create_supervisor_workflow


class ChatService:
    """Chat abstraction layer between ORM and API endpoints."""

    @staticmethod
    def get_user_persona_chats(id: int, persona_id: int, db: Session) -> Chat | None:
        return (
            db.query(Chat)
            .filter(Chat.user_id == id, Chat.persona_id == persona_id, Chat.is_active)
            .first()
        )

    @staticmethod
    def get_user_persona_chat_history(chat_id: int, db: Session) -> list[ChatMessage]:
        return db.query(ChatMessage).filter(ChatMessage.chat_id == chat_id).all()

    @staticmethod
    def create_chat_persona(id: int, persona_id: int, db: Session) -> Chat | None:
        new_chat = Chat(user_id=id, persona_id=persona_id)

        try:
            db.add(new_chat)
        except IntegrityError:
            return None
        db.commit()
        db.refresh(new_chat)

        return new_chat

    @staticmethod
    def add_chat_persona_message(
        chat_id: int, message: ChatMessageCreate, db: Session
    ) -> ChatMessage | None:
        new_message = ChatMessage(**message.model_dump(), chat_id=chat_id)

        try:
            db.add(new_message)
        except IntegrityError:
            return None
        db.commit()
        db.refresh(new_message)

        return new_message

    @staticmethod
    def generate_chat_response(
        question: str, persona_id: int, db: Session
    ) -> dict[str, Any] | None:
        persona = PersonaService.get_persona(db, persona_id)

        if not persona:
            return None

        persona_data = {
            "name": persona.name,
            "nationality": persona.nationality or "Not specified",
            "birthdate": persona.birthdate.strftime("%Y-%m-%d")
            if persona.birthdate
            else "Unknown",
            "gender": persona.gender or "Not specified",
            "hobbies": format_hobbies(persona.hobbies),
            "occupations": format_occupations(persona.occupations),
            "educations": format_education(persona.educations),
            "input": question,
        }

        executor = get_agent_executor()

        result = executor.invoke(persona_data)

        return result
    
    @staticmethod
    def generate_chat_response_supervisor(
        question: str, db: Session
    ) -> dict[str, Any] | None:
        """
        Uses the multi-agent supervisor pattern to generate a collective response.
        """
        from digital_twin.services.multi_agent_supervisor_pattern import create_supervisor_workflow

        workflow = create_supervisor_workflow(db)

        state = {
            "user_question": question,
            "chosen_persona": "",
            "completed_personas": [],
            "persona_reports": {},
            "final_answer": "",
            "confidence_score": 0.0,
        }

        try:
            result = workflow.invoke(state)
        except Exception as e:
            print(f"[Supervisor Error] {e}")
            return None

        return {
            "output": result.get("final_answer", ""),
            "confidence": result.get("confidence_score", 0.0),
            "persona": result.get("chosen_persona",""),
            "persona_id": result.get("chosen_persona_id","")
        }

