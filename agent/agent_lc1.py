from langchain.agents import initialize_agent, AgentType, Tool
from langchain_groq import ChatGroq 
from dotenv import load_dotenv
import os
import sys

# Setup root dir
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import tools
from tools.check_stock import check_stock
from tools.generate_reorder_plan import generate_reorder_plan
from tools.get_last_transaction import get_last_transaction
from tools.get_customer_detail import get_customer_detail
from tools.create_customer import create_customer
from tools.take_order import take_order

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

def generate_reorder_tool(_: str) -> str:
    """
    Wrapper so it always accepts a string input.
    """
    df = generate_reorder_plan()
    if df is None or df.empty:
        return "❌ Could not generate reorder plan."
    return df.to_string(index=False)

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
    ),
    Tool(
        name="GetLastTransactionTool",
        func=get_last_transaction,
        description="Use this to find the most recent sales order details for a customer. Input should be a customer name (string) or customer ID (number). Example: 'PT. Steelworks' or 101"
    ),
    Tool(
        name="CheckCustomerByNameAndLocationTool",
        func=lambda input_str: get_customer_detail(*input_str.split(",")),
        description=("Use this to check if a customer exists by partial name, district, and city. "
                 "Input should be comma separated: 'customer name,district,city'. "
                 "Example: 'Toko Langgar Tani,Tajurhalang,Kab Bogor'")
    ),
    Tool(
        name="RegisterNewCustomerTool",
        func=create_customer,
        description=("Use this to register a new customer. "
                 "Input should be comma separated: 'customer_name,customer_address,customer_district,customer_city'. "
                 "Example: 'Toko Langgar Tani,Jl. Kebun Raya No.10,Tajurhalang,Kab Bogor'")
    ),
    Tool(
        name="TakeOrderTool",
        func=take_order,
        description=(
            "Use this to take an order from a customer and calculate subtotals and total value. "
            "Input format: 'customer name, order: product1 - qty, product2 - qty'. "
            "Example: 'Toko Tani Berkah, order: Benih Jagung Nogorojo - 10, Emasol 30E - 8'")
    )
]

# Initialize agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
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
        user_input = input("\nWhat do you want to ask the Supply Chain Agent?\n> ")
        if user_input.lower() in ('exit', 'quit'):
            break

        result = run_agent(user_input)
        print("\n✅ Agent Response:")
        print(result)
