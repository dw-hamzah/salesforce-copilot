# This file is using initialize_agent 
from langchain.agents import initialize_agent, AgentType, Tool
from langchain_groq import ChatGroq 
from dotenv import load_dotenv
import json
import os
import sys

# Setup root dir
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import your tools
from tools.check_stock import check_stock
from tools.generate_reorder_plan import generate_reorder_plan

# Get your Groq API key from environment
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq LLM
try:
    llm = ChatGroq(
        temperature=0,
        # model_name="compound-beta" --> parsing error
        # model_name="llama-3.1-8b-instant", --> response stump
        # model_name="mixtral-8x7b",  --> model not found
        # model_name="llama2-70b-4096", -> model not foundcheck
        model_name="qwen/qwen3-32b", # --> running well
        groq_api_key=os.getenv("GROQ_API_KEY")
    )
except Exception as e:
    raise RuntimeError(f"Failed to initialize Groq LLM: {str(e)}")

# Define tools
tools = [
    Tool(
        name="CheckStockTool",
        func=check_stock,
        description="Use this to check current stock levels. Input should be a product name (string) or product ID (number). Example inputs: 'Cardboard Box Large' or 12345"
    ),
    Tool(
        name="GenerateReorderPlanTool",
        func=lambda x: generate_reorder_plan().to_string(index=False),
        description="Use this to generate a complete reorder plan based on recent average sales. No input needed - just call this tool when asked for reorder recommendations."
    )
]

# Initialize agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False,
)

def run_agent(user_input):
    try:
        response = agent.invoke(
            f"Please respond clearly. If you need to check stock, use CheckStockTool. "
            f"If you need to generate a reorder plan, use GenerateReorderPlanTool. "
            f"Question: {user_input}"
        )
        return response.get('output', str(response))
    except Exception as e:
        return f"Error processing request: {str(e)}"

if __name__ == "__main__":
    # Simple CLI for quick test
    while True:
        user_input = input("\nWhat do you want to ask the Salesforce Copilot?\n> ")
        if user_input.lower() in ('exit', 'quit'):
            break

        result = run_agent(user_input)
        print("\n✅ Agent Response:")
        print(result)
