from typing import Any
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from sqlalchemy.orm import Session

from digital_twin.config import settings
from digital_twin.schemas.question_answer import QACreate
from digital_twin.services.persona import PersonaService
from digital_twin.utils.toolkit import search_tool, travel_recommendation, weather_tool

agent_tools = [search_tool, weather_tool, travel_recommendation]


def get_model():
    if not settings.GOOGLE_API_KEY:
        raise ValueError("API key cannot be empty!")
    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", google_api_key=settings.GOOGLE_API_KEY
    )
    return model


template = PromptTemplate.from_template("""
You are a person named {name}, you are {nationality}, born in {birthdate}, of the {gender} gender.
You have these hobbies: {hobbies}. This {occupations}. And this {educations}.

You have access to the following tools:
{tools}

When deciding what to do, the available tool names you can use in actions are:
[{tool_names}]

Use the following format:

Question: {input}
Thought: your reasoning
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (repeat if needed)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!
Question: {input}
Thought: {agent_scratchpad}
""")


def format_education(educations):
    if educations:
        formatted_educations = "; ".join(
            [
                f"{e.level} in {e.course} at {e.school} {e.date_started} - {e.date_finished} (Graduated: {e.is_graduated} - Grade: {e.grade})"
                for e in educations
            ]
        )

        return formatted_educations
    else:
        return "no listed educations"


def format_occupations(occupations):
    if occupations:
        formatted_occupations = "; ".join(
            [
                f"{e.position} at {e.workplace} {e.date_started} - {e.date_finished}"
                for e in occupations
            ]
        )

        return formatted_occupations
    else:
        return "no listed occupations"


def format_hobbies(hobbies):
    if hobbies:
        formatted_hobbies = "; ".join(
            [f"{e.type} named {e.name} {e.freq}" for e in hobbies]
        )

        return formatted_hobbies
    else:
        return "no listed hobbies"


def get_agent_executor() -> AgentExecutor:
    llm = get_model()  # your ChatGoogleGenerativeAI instance

    agent = create_react_agent(llm=llm, tools=agent_tools, prompt=template)

    return AgentExecutor(
        agent=agent,
        tools=agent_tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=10,
        early_stopping_method="generate",
    )


class QAService:
    """Question abstraction layer between ORM and API endpoints."""

    @staticmethod
    def generate_response(db: Session, question: QACreate) -> dict[str, Any] | None:
        persona_id = question.persona_id

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
            "input": question.question,
        }

        executor = get_agent_executor()

        result = executor.invoke(persona_data)

        return result
    
    @staticmethod
    def generate_chat_response(question: str, persona_id: int, db: Session) -> dict[str, Any] | None:

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
