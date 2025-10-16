from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool
from langchain.prompts import PromptTemplate # For custom React prompt
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
# Initialize model with function calling support
def get_model():
    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0,  # Deterministic for reasoning
        verbose=True
    )
    return model
# print("✓ Model initialized")

# ============================================
# Tool 1: Web Search
# ============================================
from langchain.tools import DuckDuckGoSearchRun

search_tool = Tool(
    name="WebSearch",
    func=DuckDuckGoSearchRun().run,
    description="""Search the internet for current information.

    Input: Search query as string (e.g., "Tesla stock price 2024", "GDP growth USA")
    Returns: Recent search results and snippets

    Use this when you need:
    - Current/recent information not in your training
    - News or events
    - Statistics or data
    - Real-time facts

    Do NOT use for:
    - General knowledge from training data"""
)

# Collect all tools
agent_tools = [
    search_tool
]

# print(f"✓ Created {len(agent_tools)} tools for agent")

custom_react_prompt = PromptTemplate.from_template("""
Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought: {agent_scratchpad}
""")

# Create agent
agent = create_react_agent(
    llm=get_model(),
    tools=agent_tools,
    prompt=custom_react_prompt
)

# Create agent executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=agent_tools,
    verbose=True,  # Show reasoning process
    handle_parsing_errors=True,
    max_iterations=10,  # Prevent infinite loops
    early_stopping_method="generate"
)

# print("✓ Agent created and ready")