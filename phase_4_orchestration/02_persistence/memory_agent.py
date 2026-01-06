import operator
from dotenv import load_dotenv
from typing import TypedDict, Annotated, List
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver # <--- NEW IMPORT

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

# --- 4. ADD PERSISTENCE (THE BRAIN) ---
# In a real app, this would be Postgres (PostgresSaver) or Sqlite (SqliteSaver).
# For dev, we use MemorySaver (keeps it in RAM for the session).
memory = MemorySaver()

# We compile with the checkpointer!
app = workflow.compile(checkpointer=memory)

# --- 5. RUN WITH THREAD ID ---
if __name__ == "__main__":
    # A "thread_id" is like a User Session ID.
    # As long as we use the same ID, the bot remembers.
    config = {"configurable": {"thread_id": "1"}}

    print("--- Conversation 1 (Thread ID: 1) ---")
    input1 = {"messages": [HumanMessage(content="Hi! My name is Kuxha.")]}
    
    # Run the graph
    app.invoke(input1, config=config)
    print("User: Hi! My name is Kuxha.")
    print("Agent: (Saved to memory...)")

    print("\n--- Conversation 2 (Same Thread, New Turn) ---")
    input2 = {"messages": [HumanMessage(content="What is my name?")]}
    
    # Run again with SAME config
    result = app.invoke(input2, config=config)
    
    print(f"User: What is my name?")
    print(f"Agent: {result['messages'][-1].content}")
    
    print("\n--- Conversation 3 (Different Thread) ---")
    # New user, new ID
    config_new = {"configurable": {"thread_id": "2"}}
    input3 = {"messages": [HumanMessage(content="What is my name?")]}
    result_new = app.invoke(input3, config=config_new)
    
    print(f"User (Thread 2): What is my name?")
    print(f"Agent: {result_new['messages'][-1].content}")