import time
import os
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
import shutil

load_dotenv()

# --- 0. CLEAN SLATE (Reset DB for accurate test) ---
if os.path.exists("./cache_db"):
    shutil.rmtree("./cache_db")

# --- 1. SETUP THE CACHE LAYER ---
print("⚙️  Initializing Vector DB...")
chroma_client = chromadb.PersistentClient(path="./cache_db")

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.getenv("OPENAI_API_KEY"),
    model_name="text-embedding-3-small"
)

collection = chroma_client.get_or_create_collection(
    name="semantic_cache",
    embedding_function=openai_ef,
    metadata={"hnsw:space": "cosine"}
)

# --- 2. THE EXPENSIVE CALL ---
def expensive_llm_call(prompt: str) -> str:
    print(f"   💸 CALLING LLM (Simulated 2s latency)... processing '{prompt}'")
    time.sleep(2.0) 
    return f"Dr. House (Cardiology) - processed for '{prompt}'"

# --- 3. THE SMART QUERY ---
def smart_query(user_query: str, threshold: float = 0.2):
    print(f"\n❓ User asks: '{user_query}'")
    
    # Query using the QUESTION
    results = collection.query(
        query_texts=[user_query],
        n_results=1
    )
    
    # Check for Hit
    if results['documents'] and results['documents'][0]:
        dist = results['distances'][0][0]
        cached_question = results['documents'][0][0]
        
        # Retrieve the ANSWER from metadata
        cached_answer = results['metadatas'][0][0]['answer']
        
        print(f"   🔍 Found similar question: '{cached_question}' (Dist: {dist:.4f})")

        # Logic: If questions are similar, return the stored answer
        if dist < threshold:
            print(f"   ⚡ CACHE HIT! Returning answer from metadata.")
            return cached_answer
    
    # Cache Miss
    print("   ❌ Cache Miss. Routing to API.")
    answer = expensive_llm_call(user_query)
    
    # FIX: Store QUESTION in 'documents' (to embed it), ANSWER in 'metadatas'
    print("   💾 Saving result to cache...")
    collection.add(
        documents=[user_query], # <--- Embed the QUESTION
        metadatas=[{"answer": answer}], # <--- Store ANSWER in payload
        ids=[str(time.time())]
    )
    return answer

# --- 4. EXECUTION ---
if __name__ == "__main__":
    # 1. First Ask (Miss)
    smart_query("Who is the heart doctor?")
    
    # 2. Second Ask (Should be EXACT Hit -> Dist 0.0)
    smart_query("Who is the heart doctor?")
    
    # 3. Third Ask (Should be SEMANTIC Hit -> Dist < 0.2)
    smart_query("Who is the cardiologist?")
    
    # 4. Fourth Ask (Miss)
    smart_query("What are the symptoms of flu?")