import os
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import StrOutputParser
from sqlalchemy.orm import Session
from digital_twin.schemas.question_answer import QACreate
from digital_twin.services.persona import PersonaService

load_dotenv()

api_key = os.getenv("GOOGLE_KEY")

def get_model():
    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key
    )
    return model

template = ChatPromptTemplate.from_messages([
    ("system", """You are a person named {name}, you are {nationality}, born in {birthdate}, of the {gender} gender.
    You have these hobbies: {hobbies}. This {occupations}. And this {educations}."""),

    ("human", """{input}

    Requirements:
    - Be happy and smooth
    - Don't be too long in your answer
    """)
])

def format_education(educations):
    if educations:
        formatted_educations = "; ".join([
            f"{e.level} in {e.course} at {e.school} {e.date_started} - {e.date_finished} (Graduated: {e.is_graduated} - Grade: {e.grade})"
            for e in educations
        ])

        return formatted_educations
    else:
        return "no listed educations"

def format_occupations(occupations):
    if occupations:
        formatted_occupations = "; ".join([
            f"{e.position} at {e.workplace} {e.date_started} - {e.date_finished}"
            for e in occupations
        ])

        return formatted_occupations
    else:
        return "no listed occupations"

def format_hobbies(hobbies):
    if hobbies:
        formatted_hobbies = "; ".join([
            f"{e.type} named {e.name} {e.freq}"
            for e in hobbies
        ])

        return formatted_hobbies
    else:
        return "no listed hobbies"

class QAService:

    """Question abstraction layer between ORM and API endpoints."""

    @staticmethod
    def generate_response(db: Session, question: QACreate) -> QACreate | None:

        persona_id = question.persona_id

        persona = PersonaService.get_persona(db, persona_id)

        if not persona:
            return None
        
        persona_data = {
            "name": persona.name,
            "nationality": persona.nationality or "Not specified",
            "birthdate": persona.birthdate.strftime("%Y-%m-%d") if persona.birthdate else "Unknown",
            "gender": persona.gender or "Not specified",
            "hobbies": format_hobbies(persona.hobbies),
            "occupations": format_occupations(persona.occupations),
            "educations": format_education(persona.educations),
            "input": question.question
        }
        
        model = get_model()

        content_chain = template | model | StrOutputParser()

        result = content_chain.invoke(persona_data)

        return result
