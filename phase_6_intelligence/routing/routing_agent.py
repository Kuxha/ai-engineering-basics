import asyncio
import os
import sys
from typing import Literal, Optional
from dataclasses import dataclass
from dotenv import load_dotenv

# FIX: Only go up 2 levels (../..) to reach project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import logfire
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from phase_6_intelligence.abstraction.model_factory import get_model

load_dotenv()

# Observability
logfire.configure(send_to_logfire=True)
logfire.instrument_pydantic()

# --- SCHEMAS ---
class RouterDecision(BaseModel):
    provider: Literal['openai', 'google'] = Field(description="The best AI provider for the task.")
    reasoning: str = Field(description="Why this provider was chosen.")

class TriageResult(BaseModel):
    summary: str
    booking_success: bool
    doctor_name: Optional[str]
    slot_time: Optional[str]

@dataclass
class HospitalDeps:
    mcp_session: ClientSession

# --- AGENTS ---
# The Supervisor (Gemini 2.5 Flash)
router_agent = Agent(
    get_model("google"), 
    output_type=RouterDecision,
    system_prompt=(
        "You are a Senior AI Dispatcher. Route based on complexity:\n"
        "1. 'openai' for complex logic, medical triage, or booking.\n"
        "2. 'google' for summaries or simple lookups."
    )
)

# The Worker Factory
def create_worker_agent(provider_name: str) -> Agent:
    print(f"👷 Spawning Worker Agent using: {provider_name.upper()}")
    return Agent(
        get_model(provider_name),
        output_type=TriageResult,
        deps_type=HospitalDeps,
        system_prompt="You are Nurse Sarah. Triage patients and book appointments via MCP tools."
    )

# --- EXECUTION ---
async def main():
    query = "I am John Doe. I have severe chest pain and dizziness. I need a heart doctor."
    print(f"User: {query}\n")

    # 1. Routing
    print("🚦 Router is analyzing intent...")
    try:
        route_result = await router_agent.run(query)
        decision = route_result.output
        print(f"👉 Decision: {decision.provider.upper()} ({decision.reasoning})\n")
    except Exception as e:
        print(f"❌ Routing Failed: {e}")
        return

    # 2. Worker Execution
    worker = create_worker_agent(decision.provider)
    
    # Connect to the Phase 5 Server
    # Update path to use dynamic resolution based on sys.path
    # This path construction is safer
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    server_path = os.path.join(root_dir, "phase_5_protocol/05_capstone/hospital_server.py")
    
    server_params = StdioServerParameters(
        command="python",
        args=[server_path],
        env=os.environ.copy()
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Dynamically attach tools
            @worker.tool
            async def get_patient_details(ctx: RunContext[HospitalDeps], name: str) -> str:
                res = await ctx.deps.mcp_session.call_tool("get_patient_details", arguments={"name": name})
                return res.content[0].text

            @worker.tool
            async def list_available_slots(ctx: RunContext[HospitalDeps], specialty: str = None) -> str:
                res = await ctx.deps.mcp_session.call_tool("list_available_slots", arguments={"specialty": specialty})
                return res.content[0].text

            @worker.tool
            async def book_appointment(ctx: RunContext[HospitalDeps], slot_id: int, patient_id: int) -> str:
                res = await ctx.deps.mcp_session.call_tool("book_appointment", arguments={"slot_id": slot_id, "patient_id": patient_id})
                return res.content[0].text

            # Run Worker
            print("🏥 Nurse Sarah is acting...")
            result = await worker.run(query, deps=HospitalDeps(mcp_session=session))
            print(f"\n--- RESULT ---\n{result.output.summary}")

if __name__ == "__main__":
    asyncio.run(main())