import os
from dotenv import load_dotenv
from typing import TypedDict, Annotated, List
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage
import operator

load_dotenv()

# --- 1. THE STATE (The Board) ---
# This dictionary holds the conversation history.
# 'operator.add' means: "When a node returns a new message, ADD it to the list, don't overwrite it."
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]

# --- 2. THE NODES (The Players) ---
def call_model(state: AgentState):
    """
    The main chatbot node. It reads the history and generates a response.
    """
    messages = state['messages']
    model = ChatOpenAI(model="gpt-4o-mini")
    response = model.invoke(messages)
    
    # We return ONLY the new piece of state (the new message).
    # The Graph handles merging it into the main list.
    return {"messages": [response]}

# --- 3. THE GRAPH (The Rules) ---
workflow = StateGraph(AgentState)

# Add the node
workflow.add_node("agent", call_model)

# Set the entry point (Where do we start?)
workflow.set_entry_point("agent")

# Add the edge (Where do we go next?)
# "END" is a special node that stops the graph.
workflow.add_edge("agent", END)

# Compile the graph (Turn it into a runnable app)
app = workflow.compile()

# --- 4. RUN IT ---
if __name__ == "__main__":
    print("--- Starting Graph ---")
    
    # Initialize with a user message
    initial_state = {
        "messages": [
            SystemMessage(content="You are a helpful assistant."),
            HumanMessage(content="Hello! What is your name?")
        ]
    }
    
    # Run the graph
    result = app.invoke(initial_state)
    
    # Print the last message
    print("Agent:", result['messages'][-1].content)