
import time
import gradio as gr
import sys
import os

# define project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.agent_lc1 import run_agent

# call AI agent
def salesforce_ai(message, history):
    """
    Gradio ChatInterface expects a function:
    - message: new user input (string)
    - history: list of previous messages (ignored here)
    """
    response = run_agent(message)
    return response


with gr.Blocks(title="SalesForce Copilot") as demo:
    gr.Markdown("## 🤖 Supply Chain AI Copilot")
    gr.Markdown("Ask me things like 'Check stock for product 1' or 'Generate reorder plan'.")
    gr.ChatInterface(
        salesforce_ai,
        type="messages",
        flagging_mode="manual",
        save_history=True
    )

if __name__ == "__main__":
    demo.launch()


