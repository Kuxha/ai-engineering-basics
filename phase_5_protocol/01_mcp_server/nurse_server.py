from typing import List, Dict
from fastmcp import FastMCP, Context
from pydantic import BaseModel

# 1. Initialize the Server
# This name "NurseDB" is what the client sees during the handshake.
mcp = FastMCP("NurseDB")

# --- MOCK DATABASE (In production, this would be SQLite/Postgres) ---
NURSE_DB = {
    "N101": {"name": "Sarah Jones", "role": "ICU", "active": True},
    "N102": {"name": "Mike Chen", "role": "ER", "active": False},
    "N103": {"name": "Emma Wilson", "role": "Pediatrics", "active": True},
}

SHIFT_LOGS = """
[2026-01-01] N101: Checked in 08:00 AM. Vitals stable.
[2026-01-01] N102: Called in sick. Replacement needed.
[2026-01-02] N103: Administered medication at 14:00.
"""

# --- 2. DEFINE TOOLS (The "Hands") ---
# The Agent can "Call" these functions.

@mcp.tool()
def get_nurse_details(nurse_id: str) -> Dict:
    """
    Look up a nurse's core details by their ID (e.g., N101).
    Returns name, role, and active status.
    """
    nurse = NURSE_DB.get(nurse_id)
    if not nurse:
        return {"error": "Nurse not found"}
    return nurse

@mcp.tool()
def list_available_nurses(role: str = None) -> List[str]:
    """
    List all ACTIVE nurses. Optionally filter by role (ICU, ER, etc).
    """
    results = []
    for nid, data in NURSE_DB.items():
        if data["active"]:
            if role and data["role"] != role:
                continue
            results.append(f"{data['name']} ({nid}) - {data['role']}")
    return results

# --- 3. DEFINE RESOURCES (The "Books") ---
# The Agent can "Read" these like files.

@mcp.resource("shift://logs")
def get_shift_logs() -> str:
    """
    Returns the raw text logs of the last 48 hours.
    Useful for context on past events.
    """
    return SHIFT_LOGS

# --- 4. RUNNER ---
if __name__ == "__main__":
    # This starts the server over Stdio (Standard Input/Output)
    # This is the default mode for connecting to local agents.
    mcp.run()