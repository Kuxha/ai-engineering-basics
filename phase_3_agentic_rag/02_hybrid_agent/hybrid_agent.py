import os
import json
import chromadb
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)
client = OpenAI()

# --------------------------------------------------------------------------------
# DISCLAIMER: CONTEXT WINDOW & SCALE
# --------------------------------------------------------------------------------
# Why use RAG (Vector Search) for such a small file?
# 
# 1. FOR SMALL DATA (like this 1KB file): 
#    In production, we would just read the whole file and paste it into the 
#    system_prompt. It's faster and 100% accurate.
#
# 2. FOR BIG DATA (100MB+ of PDFs):
#    You physically cannot fit 10,000 pages into the AI's "Memory" (Context Window).
#    You MUST use Vector Search to find only the relevant 3-5 chunks.
#
# We use RAG here solely to simulate the architecture needed for Big Data.
# --------------------------------------------------------------------------------

# --- TOOL 1: THE LIBRARIAN (RAG) ---
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="company_policies")

def ingest_documents():
    if not os.path.exists("knowledge.txt"):
        print("Error: knowledge.txt not found!")
        return
    with open("knowledge.txt", "r") as f:
        # Split by double newline to get distinct paragraphs
        chunks = f.read().split("\n\n")
    
    collection.add(documents=chunks, ids=[f"id_{i}" for i in range(len(chunks))])
    print("   [SYSTEM] Knowledge Base Loaded.")

def search_knowledge_base(query):
    """Searches the vector DB for policies."""
    print(f"   [TOOL: RAG] Searching for: '{query}'...")
    
    # FIX: Retrieve top 3 results, not just 1.
    # This ensures we get related context (e.g. Remote Work AND Expenses).
    results = collection.query(query_texts=[query], n_results=3)
    
    if results["documents"]:
        # Join all 3 found chunks into one string for the AI to read
        combined_context = "\n\n".join(results["documents"][0])
        return combined_context
    return "No info found."

# --- TOOL 2: THE MATHEMATICIAN ---
def calculate_tool(expression):
    """Evaluates a mathematical expression safely."""
    print(f"   [TOOL: MATH] Calculating: '{expression}'...")
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"

# --- THE DEFINITION ---
tools = [
    {
        "type": "function",
        "function": {
            "name": "search_knowledge_base",
            "description": "Look up company policies (remote work, PTO, expenses).",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_tool",
            "description": "Perform mathematical calculations.",
            "parameters": {
                "type": "object",
                "properties": {"expression": {"type": "string"}},
                "required": ["expression"]
            }
        }
    }
]

def run_hybrid_agent():
    ingest_documents()
    print("--- Hybrid Agent (Ask about Policy OR Math) ---")
    
    messages = [
        {"role": "system", "content": "You are a helpful assistant. Use tools when needed."}
    ]

    while True:
        user_input = input("\nUser: ")
        if user_input.lower() in ["exit", "quit"]:
            break
            
        messages.append({"role": "user", "content": user_input})
        
        # 1. The Decision
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools,
            tool_choice="auto" 
        )
        
        msg = response.choices[0].message
        messages.append(msg)
        
        # 2. The Execution
        if msg.tool_calls:
            for tool_call in msg.tool_calls:
                func_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                
                result = "Error: Unknown Tool"
                
                # ROUTER SWITCH
                if func_name == "search_knowledge_base":
                    result = search_knowledge_base(args["query"])
                elif func_name == "calculate_tool":
                    result = calculate_tool(args["expression"])
                
                # Feed back result
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })
            
            # 3. Final Answer
            final_res = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )
            print(f"Agent: {final_res.choices[0].message.content}")
            
        else:
            print(f"Agent: {msg.content}")

if __name__ == "__main__":
    run_hybrid_agent()