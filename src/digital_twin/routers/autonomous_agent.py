from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from digital_twin.utils.autonomous_agent import get_agent_executor

router = APIRouter(prefix="/agent", tags=["agent"])

class AgentQuery(BaseModel):
    question: str

@router.post("/ask")
async def ask_agent(query: AgentQuery):
    """
    Envia uma questão para o agente autônomo e devolve a resposta.
    """
    try:
        response = await get_agent_executor().ainvoke({"input": query.question})
        return {"question": query.question, "answer": response["output"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
