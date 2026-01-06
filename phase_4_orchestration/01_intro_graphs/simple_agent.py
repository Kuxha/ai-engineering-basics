import operator
from dotenv import load_dotenv
from typing import TypedDict, Annotated, List
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

load_dotenv()

# --- 1. THE TOOLS ---
@tool
def multiply(a: int, b: int) -> int:
    """Multiplies two numbers."""
    return a * b

tools = [multiply]

# --- 2. THE STATE ---
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]

# --- 3. THE NODES ---
def call_model(state: AgentState):
    messages = state['messages']
    # We "bind" the tools to the model so it knows they exist
    model = ChatOpenAI(model="gpt-4o-mini").bind_tools(tools)
    response = model.invoke(messages)
    return {"messages": [response]}

# LangGraph has a pre-built node that runs tools for us!
tool_node = ToolNode(tools)

# --- 4. THE CONDITIONAL LOGIC (The Router) ---
def should_continue(state: AgentState):
    last_message = state['messages'][-1]
    
    # If the LLM asking to call a tool?
    if last_message.tool_calls:
        return "tools" # Go to the "tools" node
    
    # Otherwise, stop.
    return END

# --- 5. THE GRAPH ---
workflow = StateGraph(AgentState)

workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

workflow.set_entry_point("agent")

# THE MAGIC: Conditional Edge
# "After 'agent' runs, look at 'should_continue' to decide where to go."
workflow.add_conditional_edges(
    "agent",
    should_continue,
    ["tools", END]
)

# THE LOOP: After the tool runs, go back to the agent to read the result
workflow.add_edge("tools", "agent")

app = workflow.compile()

# --- 6. RUN IT ---
if __name__ == "__main__":
    print("--- Testing Math (Should Loop) ---")
    final_state = app.invoke(
        {"messages": [HumanMessage(content="What is 50 times 8?")]}
    )
    print(final_state['messages'][-1].content)

    print("\n--- Testing Chat (Should NOT Loop) ---")
    final_state = app.invoke(
        {"messages": [HumanMessage(content="Hello!")]}
    )
    print(final_state['messages'][-1].content)