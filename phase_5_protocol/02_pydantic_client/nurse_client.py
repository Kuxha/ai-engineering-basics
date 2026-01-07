import asyncio
import os
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from pydantic_ai import Agent
from dotenv import load_dotenv

load_dotenv()

# --- PATH CONFIGURATION ---
# We need to find the server script in the sibling directory (01_mcp_server)
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SERVER_SCRIPT = os.path.abspath(os.path.join(CURRENT_DIR, "..", "01_mcp_server", "nurse_server.py"))

async def run_client():
    # 1. Validation: Ensure the server script actually exists
    if not os.path.exists(SERVER_SCRIPT):
        print(f"❌ Error: Server script not found at: {SERVER_SCRIPT}")
        print("Did you move the files into '01_mcp_server'?")
        return

    # 2. Define how to launch the server (Stdio Mode)
    server_params = StdioServerParameters(
        command="python",
        args=[SERVER_SCRIPT],
        env=dict(os.environ) # Pass current env vars (API keys) to the subprocess
    )

    print(f"--- 🔌 Connecting to MCP Server... ---")
    print(f"    Target: {SERVER_SCRIPT}")

    # 3. Connect to the Server
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            
            # Handshake
            await session.initialize()
            
            # Discovery: Ask the server what tools it has
            tools_list = await session.list_tools()
            tool_names = [t.name for t in tools_list.tools]
            print(f"--- ✅ Connected! Found tools: {tool_names} ---")

            # 4. Initialize the Pydantic AI Agent
            agent = Agent(
                'openai:gpt-4o-mini',
                system_prompt=(
                    "You are a Head Nurse. "
                    "Use the available tools to find information about nurses. "
                    "Always verify if a nurse is active."
                )
            )

            # 5. Dynamic Tool Binding (The "Glue")
            # We wrap the MCP calls so the Agent can use them as native tools.
            
            @agent.tool
            async def get_nurse_details(ctx, nurse_id: str) -> str:
                """Get details for a specific nurse by ID (e.g. N101)."""
                # The Agent calls this -> We forward it to MCP -> MCP returns result
                result = await session.call_tool("get_nurse_details", arguments={"nurse_id": nurse_id})
                return result.content[0].text

            @agent.tool
            async def list_nurses(ctx, role: str = None) -> str:
                """List all nurses, optionally filtered by role."""
                # Call the server
                result = await session.call_tool("list_available_nurses", arguments={"role": role})
                
                # FIX: Check if content is empty before accessing index [0]
                if not result.content:
                    return "No nurses found matching that criteria."
                
                return result.content[0].text

            # --- 6. RUN THE AGENT ---
            print("\nUser: 'Who is nurse N101?'")
            result = await agent.run("Who is nurse N101 and are they active?")
            print(f"Agent: {result}")
            
            print("\nUser: 'List all ER nurses'")
            result = await agent.run("List all nurses who work in ER.")
            print(f"Agent: {result}")

if __name__ == "__main__":
    asyncio.run(run_client())