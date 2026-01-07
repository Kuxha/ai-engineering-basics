import asyncio
import os
from typing import Literal
from dotenv import load_dotenv

# Load env vars first
load_dotenv()

import logfire
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Import our factory
from model_factory import get_model

# 1. OBSERVABILITY
logfire.configure(send_to_logfire=True)
logfire.instrument_pydantic()

# --- PART A: THE ROUTER AGENT ---

# The Schema for the Routing Decision
class RouterDecision(BaseModel):
    provider: Literal['openai', 'google'] = Field(description="The best AI provider for the task.")
    reasoning: str = Field(description="Why this provider was chosen.")

# The Router uses Google Gemini 2.5 Flash (Fast & Cheap)
router_model = get_model("google")

router_agent = Agent(
    router_model,
    output_type=RouterDecision,
    system_prompt=(
        "You are a Senior AI Dispatcher. Analyze the user's query and route it to the best model.\n"
        "RULES:\n"
        "1. Route to 'openai' if the task involves complex medical reasoning, logic, or strict tool usage (Booking, Triage).\n"
        "2. Route to 'google' if the task is a general summary, simple lookup, or involves processing large amounts of text.\n"
        "3. Default to 'openai' for safety if unsure."
    )
)

# --- PART B: THE HOSPITAL AGENT (The Worker) ---

# We define the dependencies and result types (Same as before)
from dataclasses import dataclass
from typing import Optional

class TriageResult(BaseModel):
    summary: str
    booking_success: bool
    doctor_name: Optional[str]
    slot_time: Optional[str]

@dataclass
class HospitalDeps:
    mcp_session: ClientSession

# Function to spawn a specific worker based on the Router's decision
def create_worker_agent(provider_name: str) -> Agent:
    print(f"👷 Spawning Worker Agent using: {provider_name.upper()}")
    model = get_model(provider_name)
    
    return Agent(
        model,
        output_type=TriageResult,
        deps_type=HospitalDeps,
        system_prompt=(
            "You are Nurse Sarah. Triage patients and book appointments via MCP tools. "
            "Protocol: Identify -> Analyze -> Book Earliest Slot -> Return TriageResult."
        )
    )

# --- PART C: EXECUTION ---

async def main():
    # 1. The User Query
    query = "I am John Doe. I have severe chest pain and dizziness. I need a heart doctor."
    print(f"User: {query}\n")

    # 2. THE ROUTING STEP
    print("🚦 Router is analyzing intent...")
    routing_result = await router_agent.run(query)
    decision = routing_result.output
    
    print(f"👉 Route Decision: {decision.provider.upper()}")
    print(f"📝 Reasoning: {decision.reasoning}\n")

    # 3. THE WORKER EXECUTION
    worker = create_worker_agent(decision.provider)
    
    # Connect to MCP Server (Reuse logic from Phase 5)
    server_params = StdioServerParameters(
        command="python",
        args=["phase_5_protocol/05_capstone/hospital_server.py"],
        env=os.environ.copy()
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Run the selected worker
            deps = HospitalDeps(mcp_session=session)
            
            # Dynamically attach tools to the worker instance
            # (Note: In a full app, we'd structure this better, but this works for the demo)
            @worker.tool
            async def get_patient_details(ctx: RunContext[HospitalDeps], name: str) -> str:
                result = await ctx.deps.mcp_session.call_tool("get_patient_details", arguments={"name": name})
                return result.content[0].text

            @worker.tool
            async def list_available_slots(ctx: RunContext[HospitalDeps], specialty: str = None) -> str:
                result = await ctx.deps.mcp_session.call_tool("list_available_slots", arguments={"specialty": specialty})
                return result.content[0].text

            @worker.tool
            async def book_appointment(ctx: RunContext[HospitalDeps], slot_id: int, patient_id: int) -> str:
                result = await ctx.deps.mcp_session.call_tool("book_appointment", arguments={"slot_id": slot_id, "patient_id": patient_id})
                return result.content[0].text

            print("🏥 Nurse Sarah is acting...")
            result = await worker.run(query, deps=deps)
            output = result.output

            print("\n--- FINAL RESULT ---")
            print(f"Summary: {output.summary}")
            print(f"Doctor:  {output.doctor_name}")

if __name__ == "__main__":
    asyncio.run(main())