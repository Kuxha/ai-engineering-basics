import asyncio
import os
import sys
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv
load_dotenv()  # This loads the .env file from your root directory

import logfire
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# 1. OBSERVABILITY (The X-Ray)
# Configure Logfire to track all agent activities
logfire.configure(send_to_logfire=True)
logfire.instrument_pydantic()

# 2. THE CONTRACT (Structured Output)
# The agent MUST return this structure. It cannot just "chat".
class TriageResult(BaseModel):
    summary: str = Field(description="A brief medical summary of the action taken.")
    booking_success: bool = Field(description="True if an appointment was confirmed.")
    doctor_name: Optional[str] = Field(description="Name of the assigned doctor.")
    slot_time: Optional[str] = Field(description="Time of the appointment.")

# 3. DEPENDENCIES
# This holds the connection to our MCP Server
@dataclass
class HospitalDeps:
    mcp_session: ClientSession

# 4. THE AGENT
# We use GPT-4o for high reasoning capability
# 4. THE AGENT
# We use GPT-4o for high reasoning capability
agent = Agent(
    'openai:gpt-4o',
    deps_type=HospitalDeps,
    # ---------------------------------------------------------
    # FIX: Renamed from 'result_type' to 'output_type' in v0.0.18+
    output_type=TriageResult, 
    # ---------------------------------------------------------
    system_prompt=(
        "You are Nurse Sarah, a Senior Hospital Operations Manager. "
        "Your goal is to triage patients and book appointments strictly based on the database. "
        "\n\n"
        "PROTOCOL: "
        "1. Identify the patient. Search for them by name. If not found, abort. "
        "2. Analyze their condition. Decide which specialty is needed (Cardiology, Surgery, Diagnostic, General). "
        "3. Search for available slots for that specialty. "
        "4. Book the EARLIEST available slot. "
        "5. Return a structured TriageResult. "
        "\n\n"
        "CRITICAL RULES: "
        "- NEVER invent a doctor or slot. You must use the Tools. "
        "- If no slots are available, return booking_success=False."
    )
)


# 5. TOOL DEFINITIONS
# We dynamically attach the MCP tools to the Pydantic AI Agent
@agent.tool
async def get_patient_details(ctx: RunContext[HospitalDeps], name: str) -> str:
    """Retrieve patient details by name."""
    result = await ctx.deps.mcp_session.call_tool("get_patient_details", arguments={"name": name})
    return result.content[0].text

@agent.tool
async def list_available_slots(ctx: RunContext[HospitalDeps], specialty: str = None) -> str:
    """List open appointment slots, optionally filtered by specialty."""
    result = await ctx.deps.mcp_session.call_tool("list_available_slots", arguments={"specialty": specialty})
    return result.content[0].text

@agent.tool
async def book_appointment(ctx: RunContext[HospitalDeps], slot_id: int, patient_id: int) -> str:
    """Book a specific slot for a patient."""
    result = await ctx.deps.mcp_session.call_tool("book_appointment", arguments={"slot_id": slot_id, "patient_id": patient_id})
    return result.content[0].text

# 6. EXECUTION RUNTIME
async def main():
    # Define the server we want to talk to
    server_params = StdioServerParameters(
        command="python",
        args=["phase_5_protocol/05_capstone/hospital_server.py"],
        env=os.environ.copy()
    )

    # Establish the MCP connection via Stdio
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            
            # The User Query
            query = "I am John Doe and I have a terrible migraine. I need to see a doctor immediately."
            print(f"User: {query}\n")
            print("Nurse Sarah is thinking... (Check Logfire for live trace)")

            # Run the Agent
            deps = HospitalDeps(mcp_session=session)
            result = await agent.run(query, deps=deps)

            # --- THE FIX: Use result.output instead of result.data ---
            output = result.output 
            
            print("\n--- TRIAGE REPORT ---")
            print(f"Summary: {output.summary}")
            print(f"Success: {output.booking_success}")
            if output.booking_success:
                print(f"Doctor:  {output.doctor_name}")
                print(f"Time:    {output.slot_time}")

if __name__ == "__main__":
    asyncio.run(main())