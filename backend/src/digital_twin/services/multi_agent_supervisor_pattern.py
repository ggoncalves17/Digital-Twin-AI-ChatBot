import re
from typing import Annotated, Dict, List, TypedDict

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from pydantic import BaseModel
from sqlalchemy.orm import Session

from digital_twin.config import settings
from digital_twin.services.persona import PersonaService
from digital_twin.utils.toolkit import search_tool, travel_recommendation, weather_tool

agent_tools = [search_tool, weather_tool, travel_recommendation]


# ===============================
# Data Models
# ===============================
class PersonaReport(BaseModel):
    persona_name: str
    response: str
    confidence: float
    key_findings: List[str]


class SupervisorState(TypedDict):
    user_question: str
    chosen_persona: str
    chosen_persona_id: int
    completed_personas: Annotated[list[str], add_messages]
    persona_reports: Dict[str, PersonaReport]
    final_answer: str
    confidence_score: float


# ===============================
# LLM Setup
# ===============================
def create_llm():
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.7,
        google_api_key=settings.GOOGLE_API_KEY
    )
    return llm


# ===============================
# Persona Agent Factory
# ===============================
def create_persona_agent(persona: Dict, llm):
    def agent(state: Dict) -> Dict:
        question = state["user_question"]

        persona_context = f"""
        You are a person named {persona.get('name', 'Unknown')}.
        You are {persona.get('nationality', 'of unspecified nationality')}, born in {persona.get('birthdate', 'an unknown date')},
        of the {persona.get('gender', 'unspecified')} gender.

        Your hobbies include: {persona.get('hobbies', 'no hobbies listed')}.
        Your occupations are: {persona.get('occupations', 'not specified')}.
        Your education background is: {persona.get('educations', 'not specified')}.
        You have acess to the following tools: {agent_tools}

        Question: {question}
        Thought: describe your reasoning
        Final Answer: respond naturally as yourself, {persona.get('name', 'Unknown')}
        """

        response = llm.invoke([
            SystemMessage(content=persona_context.strip()),
            HumanMessage(content=f"User asks: {question}")
        ])

        report = PersonaReport(
            persona_name=persona["name"],
            response=response.content,
            confidence=0.9,
            key_findings=[
                f"Answered in {persona['name']}'s style.",
                f"Persona context: nationality={persona.get('nationality')}, hobbies={persona.get('hobbies', 'N/A')}"
            ]
        )

        return {
            "persona_reports": {
                **state.get("persona_reports", {}),
                persona["name"]: report
            },
            "completed_personas": state.get("completed_personas", []) + [persona["name"]],
            "chosen_persona": persona["name"],
            "chosen_persona_id": persona["id"]
        }

    return agent


# ===============================
# Supervisor Agent
# ===============================
def supervisor_agent_factory(agents: Dict[str, callable], persona_map: Dict[str, int], llm):
    """Supervisor que decide qual persona deve responder."""

    def supervisor_agent(state: SupervisorState) -> Dict:
        user_question = state["user_question"].lower()

        # Tenta encontrar uma persona mencionada diretamente
        for persona_name in agents.keys():
            if re.search(rf"\b{persona_name.lower()}\b", user_question):
                print(f"→ Supervisor detected direct mention: {persona_name}")
                next_persona = persona_name
                break
        else:
            # Caso não encontre menção direta, pede ao LLM para escolher a melhor persona
            persona_names = ", ".join(agents.keys())
            system_prompt = f"""
            You are a routing agent.
            Available personas: {persona_names}.
            Based on the user's question, decide which persona is most appropriate to answer.
            Respond ONLY with the persona name.
            """

            response = llm.invoke([
                SystemMessage(content=system_prompt.strip()),
                HumanMessage(content=f"User question: {user_question}")
            ])

            next_persona = response.content.strip()
            if next_persona not in agents:
                print(f"Persona '{next_persona}' not found, defaulting to first available.")
                next_persona = list(agents.keys())[0]

            print(f"→ Supervisor chose persona: {next_persona}")

        # Executa a persona selecionada
        persona_response = agents[next_persona](state)
        report = persona_response["persona_reports"][next_persona]

        return {
            "final_answer": report.response,
            "confidence_score": report.confidence,
            "persona_reports": persona_response["persona_reports"],
            "chosen_persona": next_persona,
            "chosen_persona_id": persona_map[next_persona]
        }

    return supervisor_agent


# ===============================
# Workflow Builder
# ===============================
def create_supervisor_workflow(db: Session):
    workflow = StateGraph(SupervisorState)

    personas_from_db = PersonaService.get_personas(db)

    persona_dicts = []
    persona_map = {}  # nome → id
    for p in personas_from_db:
        persona_dicts.append({
            "id": p.id,
            "name": p.name,
            "birthdate": p.birthdate.strftime("%Y-%m-%d") if p.birthdate else "Unknown",
            "gender": p.gender or "Not specified",
            "nationality": p.nationality or "Not specified",
            "educations": [e.degree for e in p.educations] if hasattr(p, "educations") else [],
            "occupations": [o.name for o in p.occupations] if hasattr(p, "occupations") else [],
            "hobbies": [h.name for h in p.hobbies] if hasattr(p, "hobbies") else [],
        })
        persona_map[p.name] = p.id

    llm = create_llm()
    agents = {p["name"]: create_persona_agent(p,llm) for p in persona_dicts}

    workflow.add_node("supervisor", supervisor_agent_factory(agents, persona_map,llm))
    workflow.add_edge(START, "supervisor")
    workflow.add_edge("supervisor", END)

    return workflow.compile()