import json
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)
client = OpenAI()

# --- PART 1: THE TOOLS ---
# We have a specific tool for database lookups.

def get_ticket_status(ticket_id):
    """Query the database for a support ticket status."""
    print(f"   [DATABASE] Querying ticket {ticket_id}...")
    # Mock Database
    mock_db = {
        "TKT-123": "Open",
        "TKT-456": "Closed - Resolved",
        "TKT-789": "Pending User Reply"
    }
    status = mock_db.get(ticket_id, "Not Found")
    return json.dumps({"ticket_id": ticket_id, "status": status})

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_ticket_status",
            "description": "Get the status of a support ticket by its ID (e.g., TKT-123).",
            "parameters": {
                "type": "object",
                "properties": {"ticket_id": {"type": "string"}},
                "required": ["ticket_id"]
            }
        }
    }
]

# --- PART 2: THE ROUTER AGENT ---

system_prompt = """
You are the 'Gatekeeper' for a Customer Support system.
Your job is to helpful, but efficient.

RULES:
1. If the user asks about a specific ticket (e.g., 'status of TKT-123'), USE THE TOOL.
2. If the user is just saying 'hi' or asking general questions, just chat normally.
3. Be concise.
"""

def run_agent():
    print("--- Support Gatekeeper (Type 'exit' to quit) ---")
    messages = [{"role": "system", "content": system_prompt}]

    while True:
        user_input = input("\nUser: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        messages.append({"role": "user", "content": user_input})

        # The Decision Point: The AI decides "Text" or "Tool"?
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools,
            tool_choice="auto" # "auto" lets the AI act as the Router
        )
        
        msg = response.choices[0].message
        messages.append(msg) # Keep history (Memory)

        # ROUTING LOGIC
        if msg.tool_calls:
            print("   [ROUTER] Decision: Database Lookup Needed.")
            
            for tool_call in msg.tool_calls:
                # 1. Execute Tool
                args = json.loads(tool_call.function.arguments)
                result = get_ticket_status(args["ticket_id"])
                
                # 2. Feed result back
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })
            
            # 3. Get final answer after tool use
            final_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )
            print(f"Agent: {final_response.choices[0].message.content}")
            
        else:
            print("   [ROUTER] Decision: General Chat.")
            print(f"Agent: {msg.content}")

if __name__ == "__main__":
    run_agent()