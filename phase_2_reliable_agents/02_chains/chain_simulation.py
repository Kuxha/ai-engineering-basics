import json
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)
client = OpenAI()

# --- PART 1: THE TOOLS (The "Menu") ---
# We have TWO tools now. The AI must figure out it needs to call them in sequence.

def get_user_details(email):
    """Finds a user's ID based on their email."""
    print(f"   [TOOL] Looking up user: {email}...")
    mock_users = {
        "alice@example.com": {"id": "USR-100", "name": "Alice"},
        "bob@example.com": {"id": "USR-101", "name": "Bob"}
    }
    return json.dumps(mock_users.get(email, {"error": "User not found"}))

def get_recent_order(user_id):
    """Finds the most recent order for a specific user ID."""
    print(f"   [TOOL] Looking up orders for: {user_id}...")
    mock_orders = {
        "USR-100": {"order_id": "ORD-999", "product": "Laptop", "status": "Shipped"},
        "USR-101": {"order_id": "ORD-777", "product": "Coffee", "status": "Delivered"}
    }
    return json.dumps(mock_orders.get(user_id, {"error": "No orders found"}))

# The Schema defines both tools
tools_schema = [
    {
        "type": "function",
        "function": {
            "name": "get_user_details",
            "description": "Look up a user's ID and name by their email address.",
            "parameters": {
                "type": "object",
                "properties": {"email": {"type": "string"}},
                "required": ["email"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_recent_order",
            "description": "Get the most recent order details (ID, status) for a user ID.",
            "parameters": {
                "type": "object",
                "properties": {"user_id": {"type": "string"}},
                "required": ["user_id"]
            }
        }
    }
]

# --- PART 2: THE CHAIN LOOP (The "Brain") ---

def run_chain():
    # A vague query that requires TWO steps to solve
    user_query = "What is the status of the last order for alice@example.com?"
    print(f"User: {user_query}")
    
    messages = [{"role": "user", "content": user_query}]

    # We use a loop because we don't know how many steps the AI needs.
    # It might need 1 tool, 2 tools, or 0 tools.
    while True:
        # 1. Ask the AI what to do next
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools_schema,
            tool_choice="auto"
        )
        msg = response.choices[0].message
        messages.append(msg) # Add the AI's thought to history

        # 2. Check: Did the AI ask for a tool?
        if msg.tool_calls:
            for tool_call in msg.tool_calls:
                func_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                
                print(f"🤖 AI Decision: Call {func_name} with {args}")

                # 3. Execute the right tool
                result = None
                if func_name == "get_user_details":
                    result = get_user_details(args["email"])
                elif func_name == "get_recent_order":
                    result = get_recent_order(args["user_id"])
                
                # 4. Feed the result back to the AI
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })
        else:
            # 5. If NO tool was asked for, the AI is done!
            print(f"Agent: {msg.content}")
            break

if __name__ == "__main__":
    run_chain()