import os
import chromadb
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)
client = OpenAI()

# --- SETUP: DATABASE WITH METADATA ---
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="company_policies")

def ingest_documents():
    if not os.path.exists("knowledge.txt"):
        print("Error: knowledge.txt not found!")
        return
    with open("knowledge.txt", "r") as f:
        chunks = f.read().split("\n\n")
    
    # NEW: We are giving each chunk a meaningful "Source ID"
    # In a real app, this would be filenames like "Remote_Policy_v2.pdf"
    ids = ["Policy #1 - Remote Work", "Policy #2 - Expenses", "Policy #3 - PTO"]
    
    # Safety check if knowledge.txt changes size
    if len(chunks) != len(ids):
        ids = [f"Section {i+1}" for i in range(len(chunks))]

    collection.add(documents=chunks, ids=ids)
    print("   [SYSTEM] Knowledge Base Loaded with Source IDs.")

def search_knowledge_base(query):
    print(f"   [RAG] Searching for: '{query}'...")
    
    # We fetch Text (documents) AND Names (ids)
    results = collection.query(query_texts=[query], n_results=3)
    
    if not results["documents"]:
        return "No info found."

    # NEW: Format the output so the AI knows where each text came from
    # Output format:
    # [Source: Policy #2] ...text...
    # [Source: Policy #1] ...text...
    
    context_pieces = []
    found_docs = results["documents"][0]
    found_ids = results["ids"][0]
    
    for doc, source_id in zip(found_docs, found_ids):
        context_pieces.append(f"[Source: {source_id}]\n{doc}")
        
    return "\n\n".join(context_pieces)

# --- THE AGENT ---

tools = [
    {
        "type": "function",
        "function": {
            "name": "search_knowledge_base",
            "description": "Look up company policies. Returns text and source names.",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"]
            }
        }
    }
]

# NEW: Strict System Instructions for Citations
system_prompt = """
You are a helpful HR Assistant.
1. Use the knowledge base to answer questions.
2. ALWAYS cite your source using square brackets at the end of the sentence.
   Example: "You can work remotely on Tuesdays [Source: Policy #1 - Remote Work]."
3. If the source is not explicitly provided in the tool output, do not make one up.
"""

def run_agent():
    ingest_documents()
    print("--- Citation Agent (Ask a question) ---")
    messages = [{"role": "system", "content": system_prompt}]

    while True:
        user_input = input("\nUser: ")
        if user_input.lower() in ["exit", "quit"]:
            break
            
        messages.append({"role": "user", "content": user_input})
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        
        msg = response.choices[0].message
        messages.append(msg)
        
        if msg.tool_calls:
            for tool_call in msg.tool_calls:
                args = eval(tool_call.function.arguments)
                result = search_knowledge_base(args["query"])
                
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })
            
            final_res = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )
            print(f"Agent: {final_res.choices[0].message.content}")
        else:
            print(f"Agent: {msg.content}")

if __name__ == "__main__":
    run_agent()