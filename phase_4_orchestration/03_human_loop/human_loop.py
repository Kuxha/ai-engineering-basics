import operator
from typing import Annotated, List, TypedDict, Literal
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, ToolMessage
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver 
from langchain_core.tools import tool

load_dotenv()

# --- 1. TOOLS ---
@tool
def check_balance():
    """Checks the user's bank balance."""
    return "Balance is $10,000"

@tool
def transfer_money(amount: int):
    """Transfers money to an external account. DANGEROUS."""
    return f"SUCCESS: Transferred ${amount}."

tools = [check_balance, transfer_money]
tool_map = {t.name: t for t in tools}

# --- 2. STATE ---
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]

# --- 3. NODES ---
def agent_node(state: AgentState):
    messages = state['messages']
    model = ChatOpenAI(model="gpt-4o-mini").bind_tools(tools)
    response = model.invoke(messages)
    return {"messages": [response]}

def tool_node(state: AgentState):
    last_message = state['messages'][-1]
    tool_calls = last_message.tool_calls
    
    results = []
    for call in tool_calls:
        print(f"  [System] Executing Tool: {call['name']}...")
        tool_func = tool_map[call['name']]
        output = tool_func.invoke(call['args'])
        results.append(ToolMessage(tool_call_id=call['id'], content=str(output)))
        
    return {"messages": results}

# --- 4. GRAPH ---
workflow = StateGraph(AgentState)
workflow.add_node("Agent", agent_node)
workflow.add_node("Tools", tool_node)

workflow.set_entry_point("Agent")

# Conditional Edge (Router)
def router(state: AgentState):
    last_message = state['messages'][-1]
    if last_message.tool_calls:
        return "Tools"
    return END

workflow.add_conditional_edges("Agent", router)
workflow.add_edge("Tools", "Agent")

# --- 5. THE MAGIC (Interrupt) ---
# We tell the graph: "Stop BEFORE you run the 'Tools' node."
memory = MemorySaver()
app = workflow.compile(
    checkpointer=memory, 
    interrupt_before=["Tools"] # <--- THIS IS THE KEY
)

# --- 6. RUNNER ---
if __name__ == "__main__":
    thread_id = "user_wallet_1"
    config = {"configurable": {"thread_id": thread_id}}
    
    print("--- Step 1: User requests transfer ---")
    app.invoke(
        {"messages": [HumanMessage(content="Transfer $500.")]}, 
        config=config
    )
    
    # At this point, the Graph has PAUSED.
    # It decided to call 'transfer_money', but it hasn't executed it yet.
    
    # We inspect the state
    snapshot = app.get_state(config)
    next_action = snapshot.next
    print(f"\n[Status] Graph Paused. Next node: {next_action}")
    
    # Human Review
    approval = input("Do you approve this action? (yes/no): ")
    
    if approval.lower() == "yes":
        print("\n--- Step 2: Resuming Graph ---")
        # Passing None means "Just continue where you left off"
        result = app.invoke(None, config=config)
        print(f"Agent: {result['messages'][-1].content}")
    else:
        print("\n[Status] Action Cancelled.")