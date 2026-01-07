import asyncio
import os
import logfire  # 🚀 IMPORT LOGFIRE
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from pydantic_ai import Agent
from dotenv import load_dotenv

load_dotenv()

# 🚀 CONFIGURE OBSERVABILITY
# This tells Logfire to auto-trace all Pydantic AI Agents
logfire.configure(send_to_logfire=True)
logfire.instrument_pydantic()

# --- PATH CONFIGURATION ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# Note: We go up TWO levels now (../..) because we are in 03_observability
SERVER_SCRIPT = os.path.abspath(os.path.join(CURRENT_DIR, "..", "01_mcp_server", "nurse_server.py"))

async def run_client():
    if not os.path.exists(SERVER_SCRIPT):
        print(f"❌ Error: Server script not found at: {SERVER_SCRIPT}")
        return

    server_params = StdioServerParameters(
        command="python",
        args=[SERVER_SCRIPT],
        env=dict(os.environ)
    )

    print(f"--- 🔭 Observability Enabled. Connecting to MCP Server... ---")

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Create Agent
            agent = Agent(
                'openai:gpt-4o-mini',
                system_prompt="You are a Head Nurse. Verify active status before answering."
            )

            # --- Tools ---
            @agent.tool
            async def get_nurse_details(ctx, nurse_id: str) -> str:
                # 🚀 MANUALLY LOG THE MCP CALL
                with logfire.span("mcp_call", tool="get_nurse_details", id=nurse_id):
                    result = await session.call_tool("get_nurse_details", arguments={"nurse_id": nurse_id})
                    return result.content[0].text

            @agent.tool
            async def list_nurses(ctx, role: str = None) -> str:
                # 🚀 MANUALLY LOG THE MCP CALL
                with logfire.span("mcp_call", tool="list_available_nurses", role=role):
                    result = await session.call_tool("list_available_nurses", arguments={"role": role})
                    if not result.content:
                        return "No nurses found."
                    return result.content[0].text

            # --- RUN ---
            print("\nUser: 'Who is nurse N101?'")
            # Logfire automatically tracks this .run() call
            result = await agent.run("Who is nurse N101 and are they active?")
            print(f"Agent: {result}")

if __name__ == "__main__":
    asyncio.run(run_client())