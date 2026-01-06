import os
import chromadb
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)
client = OpenAI()

# --- SETUP ---
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="eval_policies")

def ingest_documents():
    if not os.path.exists("knowledge.txt"):
        return
    with open("knowledge.txt", "r") as f:
        # Split and remove empty whitespace chunks
        raw_chunks = f.read().split("\n\n")
        chunks = [c.strip() for c in raw_chunks if c.strip()]
    
    
    
    ids = ["Policy #1 - Remote Work", "Policy #2 - Expenses", "Policy #3 - PTO"]
    
    if len(chunks) != len(ids):
        print(f"   [WARNING] Chunk count mismatch! Expected {len(ids)}, got {len(chunks)}. Reverting to generic IDs.")
        ids = [f"Section {i+1}" for i in range(len(chunks))]
        
    collection.add(documents=chunks, ids=ids)

def search_knowledge_base(query):
    results = collection.query(query_texts=[query], n_results=3)
    if not results["documents"]:
        return "No info found."
    
    context_pieces = []
    for doc, source_id in zip(results["documents"][0], results["ids"][0]):
        context_pieces.append(f"[Source: {source_id}]\n{doc}")
    return "\n\n".join(context_pieces)

tools = [{
    "type": "function",
    "function": {
        "name": "search_knowledge_base",
        "description": "Look up policies.",
        "parameters": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"]
        }
    }
}]

# --- THE FUNCTION WE WILL TEST ---
def get_agent_response(user_query):
    # Re-init ingest on every run for safety in this demo
    try:
        ingest_documents()
    except:
        pass # Ignore if already exists

    messages = [
        {"role": "system", "content": "You are a helpful HR Assistant. ALWAYS cite your source using square brackets. Example: [Source: Policy #1]."},
        {"role": "user", "content": user_query}
    ]
    
    # 1. First Call
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools
    )
    msg = response.choices[0].message
    messages.append(msg)
    
    # 2. Tool Execution
    if msg.tool_calls:
        for tool_call in msg.tool_calls:
            args = eval(tool_call.function.arguments)
            result = search_knowledge_base(args["query"])
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
        return final_res.choices[0].message.content
    
    return msg.content