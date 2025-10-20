from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from digital_twin.database import get_db
from digital_twin.schemas.question_answer import QACreate
from digital_twin.services.questions_answers import QAService
from digital_twin.utils.lakehouse_export import export_data

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/")
def questions_answers(
    question: QACreate,
    db: Annotated[Session, Depends(get_db)],
):
    result = QAService.generate_response(db, question)

    if result is None:
        export_data(
            "chat",
            {
                "event": "question_asked",
                "status": "error",
                "description": f"Persona with ID {question.persona_id} does not exist",
            }
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Persona id not found"
        )

    # TODO log tokens used in LLM invocation
    export_data(
        "chat",
        {
            "event": "question_asked",
            "status": "success",
            "persona_id": question.persona_id,
            "question": question.question,
            # "input_tokens": result.usage_metadata["input_tokens"],
            # "output_tokens": result.usage_metadata["output_tokens"],
            # "total_tokens": result.usage_metadata["total_tokens"]
        }
    )
    return result
