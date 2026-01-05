import json
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load your API key from the .env file
load_dotenv(override=True)
client = OpenAI()

# --- PART 1: THE TOOL (The "Hands") ---
# This is a standard Python function. The AI cannot "see" this code.
# It can only see the *description* we provide in the schema below.
def get_order_status(order_id):
    """
    Simulates a database lookup. Returns JSON because LLMs understand JSON better than English.
    """
    print(f"   [SYSTEM] Searching database for {order_id}...") 
    
    mock_db = {
        "ORD-123": {"status": "shipped", "delivery_date": "2023-10-25"},
        "ORD-456": {"status": "processing", "delivery_date": "TBD"},
        "ORD-789": {"status": "delivered", "delivery_date": "2023-10-20"}
    }
    # .get() prevents the code from crashing if the ID doesn't exist
    result = mock_db.get(order_id, {"error": "Order ID not found."})
    return json.dumps(result)

# --- PART 2: THE SCHEMA (The "Menu") ---
# We must explicitly tell the AI what tools are available.
# This structure isn't random; it follows the OpenAI "Tool" standard.
tools_schema = [
    {
        "type": "function",
        "function": {
            "name": "get_order_status",
            "description": "Get the current status and delivery date of a customer order.",
            "parameters": {
                "type": "object",
                "properties": {
                    # We define 'order_id' so the AI knows exactly what argument to pass.
                    "order_id": {
                        "type": "string", 
                        "description": "The unique order ID (e.g., ORD-123)"
                    }
                },
                "required": ["order_id"] # The AI MUST provide this argument.
            }
        }
    }
]

def run_agent():
    user_query = "Where is my order ORD-123?"
    print(f"User: {user_query}")

    # --- PART 3: THE BRAIN (First Pass) ---
    # We ask the LLM: "Here is the user query. Here are your tools. What do you want to do?"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": user_query}],
        tools=tools_schema, # <--- Giving the AI 'Hands'
        tool_choice="auto"  # <--- Telling the AI "Use your hands if you need to"
    )
    
    # We grab the first (and usually only) response choice
    msg = response.choices[0].message

    # --- PART 4: THE DECISION POINT ---
    # The AI has two options:
    # Option A: It replies with text (msg.content is set, msg.tool_calls is None).
    # Option B: It asks to run a function (msg.tool_calls is set).
    
    if msg.tool_calls:
        print(" AI: I need to use a tool to answer this.")
        
        # The AI can technically ask for multiple tools at once. We just take the first one.
        tool_call = msg.tool_calls[0]
        
        # 4a. Parse the Request
        # The AI gives us the function name as a string (e.g., "get_order_status")
        function_name = tool_call.function.name
        
        # The AI gives us the arguments as a JSON string (e.g., '{"order_id": "ORD-123"}')
        # We must convert this string back into a Python dictionary.
        function_args = json.loads(tool_call.function.arguments)
        
        print(f"   [Check] Function Name: {function_name}")
        print(f"   [Check] Arguments: {function_args}")
        
        # 4b. Execute the Code (The "Hands" Move)
        # We manually check the name and run our Python function.
        if function_name == "get_order_status":
            tool_output = get_order_status(function_args["order_id"])
            print(f"   [Data] Database returned: {tool_output}")
            
            # --- PART 5: THE SYNTHESIS (Second Pass) ---
            # The AI has the tool output, but the USER hasn't seen it yet.
            # We must send the data BACK to the AI so it can translate "JSON" into "English".
            
            final_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user", "content": user_query}, # Original Question
                    msg,                                      # The AI's request to use the tool
                    {                                         # The Result of the tool
                        "role": "tool", 
                        "tool_call_id": tool_call.id, 
                        "content": tool_output
                    }
                ]
            )
            print(f"Agent: {final_response.choices[0].message.content}")
    else:
        # If the AI didn't use a tool, just print what it said.
        print(f"Agent: {msg.content}")

if __name__ == "__main__":
    run_agent()