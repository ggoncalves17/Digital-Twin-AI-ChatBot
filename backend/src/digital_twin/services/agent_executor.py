from langchain.agents import AgentExecutor, create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from digital_twin.prompts.persona_prompt import persona_template
from digital_twin.config import settings
from digital_twin.utils.toolkit import search_tool, travel_recommendation, weather_tool

agent_tools = [search_tool, weather_tool, travel_recommendation]

def get_model():
    if not settings.GOOGLE_API_KEY:
        raise ValueError("API key cannot be empty!")
    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", google_api_key=settings.GOOGLE_API_KEY
    )
    return model


def get_agent_executor() -> AgentExecutor:
    llm = get_model()  # your ChatGoogleGenerativeAI instance

    agent = create_react_agent(llm=llm, tools=agent_tools, prompt=persona_template)

    return AgentExecutor(
        agent=agent,
        tools=agent_tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=10,
        early_stopping_method="generate",
    )