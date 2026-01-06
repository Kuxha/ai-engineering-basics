import sqlite3
import operator
from dotenv import load_dotenv
from typing import TypedDict, Annotated, List
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, BaseMessage
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver

load_dotenv()

# --- 1. SETUP STATE ---
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]

# --- 2. SETUP NODE ---
def call_model(state: AgentState):
    messages = state['messages']
    model = ChatOpenAI(model="gpt-4o-mini")
    response = model.invoke(messages)
    return {"messages": [response]}

# --- 3. BUILD GRAPH ---
workflow = StateGraph(AgentState)
workflow.add_node("agent", call_model)
workflow.set_entry_point("agent")
workflow.add_edge("agent", END)

# --- 4. THE PERSISTENCE LAYER ---
def run_interactive_session():
    # Connect to SQLite database (creates file if missing)
    with sqlite3.connect("checkpoints.sqlite", check_same_thread=False) as conn:
        
        # Create the saver
        memory = SqliteSaver(conn)
        
        # Compile graph with memory
        app = workflow.compile(checkpointer=memory)

        print("--- Persistent Chat Bot (Type 'q' to quit) ---")
        thread_id = input("Enter a Thread ID (e.g., 'user_1'): ")
        config = {"configurable": {"thread_id": thread_id}}
        
        while True:
            user_input = input("\nYou: ")
            if user_input.lower() in ["q", "quit"]:
                break
                
            # Stream output
            events = app.stream(
                {"messages": [HumanMessage(content=user_input)]}, 
                config=config
            )
            
            for event in events:
                if "agent" in event:
                    print(f"Agent: {event['agent']['messages'][0].content}")

if __name__ == "__main__":
    run_interactive_session()