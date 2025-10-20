from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from digital_twin.database import get_db
from digital_twin.schemas.question_answer import QACreate
from digital_twin.services.questions_answers import QAService

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/")
def questions_answers(
    question: QACreate,
    db: Annotated[Session, Depends(get_db)],
):
    result = QAService.generate_response(db, question)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Persona id not found"
        )    
    return result
