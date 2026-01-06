import os
import chromadb
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)
client = OpenAI()

# --- STEP 1: SETUP THE VECTOR DB ---
# We use a temporary in-memory database for this demo
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="company_policies")

def ingest_documents():
    """Reads the text file and saves it to the Vector DB."""
    if not os.path.exists("knowledge.txt"):
        print("Error: knowledge.txt not found!")
        return

    with open("knowledge.txt", "r") as f:
        text = f.read()

    # We split by double newline to get paragraphs
    chunks = text.split("\n\n")
    
    # Add to ChromaDB
    print(f"--- Ingesting {len(chunks)} chunks into Memory ---")
    collection.add(
        documents=chunks,
        ids=[f"id_{i}" for i in range(len(chunks))]
    )

# --- STEP 2: DEFINE THE TOOL ---
# This is the function the AI will "call"
def search_knowledge_base(query):
    """Searches the company policy for relevant info."""
    print(f"   [RAG TOOL] Searching for: '{query}'...")
    
    results = collection.query(
        query_texts=[query],
        n_results=1
    )
    
    # Extract the text from the result
    if results["documents"]:
        found_text = results["documents"][0][0]
        return found_text
    return "No relevant policy found."

# --- STEP 3: THE AGENT LOOP ---
tools = [
    {
        "type": "function",
        "function": {
            "name": "search_knowledge_base",
            "description": "Look up company policies (remote work, expenses, PTO).",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The search keywords."}
                },
                "required": ["query"]
            }
        }
    }
]

def run_agent():
    # 1. Load the data first!
    ingest_documents()
    
    print("\n--- Company Policy Agent (Ask about PTO, Expenses, Remote Work) ---")
    
    messages = [
        {"role": "system", "content": "You are an HR Assistant. Use the 'search_knowledge_base' tool to answer questions. Do not guess."}
    ]

    while True:
        user_input = input("\nUser: ")
        if user_input.lower() in ["exit", "quit"]:
            break
            
        messages.append({"role": "user", "content": user_input})
        
        # 2. The Decision (Router)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        
        msg = response.choices[0].message
        messages.append(msg)
        
        # 3. Execution Logic
        if msg.tool_calls:
            for tool_call in msg.tool_calls:
                # A. Parse the argument
                args = eval(tool_call.function.arguments) # simple parsing
                query = args["query"]
                
                # B. Run the RAG search
                result = search_knowledge_base(query)
                
                # C. Feed back to AI
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })
            
            # 4. Final Answer
            final_res = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )
            print(f"Agent: {final_res.choices[0].message.content}")
        else:
            # If no tool needed (e.g. "Hi")
            print(f"Agent: {msg.content}")

if __name__ == "__main__":
    run_agent()