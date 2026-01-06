import operator
from typing import Annotated, List, TypedDict
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, ToolMessage
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver 
# Import the specific tool we just built
from tools import find_available_nurse 

load_dotenv()

# --- 1. STATE ---
class ShiftState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]

# --- 2. NODES ---

def intake_node(state: ShiftState):
    """
    The Brain: Analyzes the user request.
    It decides IF it needs to call the tool to find a provider.
    """
    messages = state['messages']
    # We bind the 'find_available_nurse' tool to the model
    model = ChatOpenAI(model="gpt-4o-mini").bind_tools([find_available_nurse])
    
    response = model.invoke(messages)
    return {"messages": [response]}

def tool_node(state: ShiftState):
    """
    The Hands: Executes the deterministic logic from tools.py.
    """
    last_message = state['messages'][-1]
    tool_calls = last_message.tool_calls
    
    results = []
    
    for call in tool_calls:
        if call['name'] == 'find_available_nurse':
            print("  [System] Running Weighted Scoring Algorithm...")
            # This calls the function in tools.py
            output = find_available_nurse.invoke(call['args'])
            results.append(ToolMessage(tool_call_id=call['id'], content=str(output)))
    
    return {"messages": results}

def compliance_node(state: ShiftState):
    """
    The Gatekeeper: This node runs AFTER the tool but BEFORE the final response.
    It represents the 'Drafting' phase.
    """
    return {"messages": [HumanMessage(content="[SYSTEM] Provider identified. Drafting recruitment SMS...")]}

# --- 3. GRAPH ---
workflow = StateGraph(ShiftState)

workflow.add_node("Intake", intake_node)
workflow.add_node("Scheduler", tool_node)
workflow.add_node("Compliance", compliance_node)

workflow.set_entry_point("Intake")

# Logic: Did the Intake Agent ask to run a tool?
def route_intake(state: ShiftState):
    last_msg = state['messages'][-1]
    if last_msg.tool_calls:
        return "Scheduler"
    return END

workflow.add_conditional_edges("Intake", route_intake)

# After Scheduler runs, go to Compliance
workflow.add_edge("Scheduler", "Compliance")
# After Compliance, we are done
workflow.add_edge("Compliance", END)

# --- 4. COMPILE (With Safety Interrupt) ---
memory = MemorySaver()
app = workflow.compile(
    checkpointer=memory,
    # CRITICAL: We pause BEFORE the 'Compliance' node runs.
    # This allows the Human to review the Tool's output (The chosen provider).
    interrupt_before=["Compliance"]
)

# --- 5. RUNNER ---
if __name__ == "__main__":
    # Case ID mimics a patient file ID
    thread_id = "case_303"
    config = {"configurable": {"thread_id": thread_id}}
    
    print(f"--- Shift Orchestrator (Case {thread_id}) ---")
    user_input = input("Request: ") # Try: "Need an ICU nurse in Brooklyn."
    
    # 1. Run until the Pause
    app.invoke({"messages": [HumanMessage(content=user_input)]}, config=config)
    
    # 2. Inspect the Pause State
    state = app.get_state(config)
    if state.next:
        print("\n--- ⏸️  COMPLIANCE CHECK REQUIRED ⏸️  ---")
        
        # Look at the last message to see what the Tool returned
        last_msg = state.values['messages'][-1]
        print(f"Tool Output: {last_msg.content}")
        
        # 3. Human Decision
        approval = input("\nDo you approve this provider match? (yes/no): ")
        
        if approval.lower() == "yes":
            print("\n--- ✅ Approved. Sending SMS... ---")
            # Resume the graph by passing None
            result = app.invoke(None, config=config)
            print(f"Final Response: {result['messages'][-1].content}")
        else:
            print("\n--- ❌ Rejected. Cancellation logged. ---")