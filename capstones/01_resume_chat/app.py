import os
import chromadb
from chromadb.utils import embedding_functions
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Setup Clients
client = OpenAI()
chroma_client = chromadb.PersistentClient(path="./chroma_db")
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.getenv("OPENAI_API_KEY"),
    model_name="text-embedding-3-small"
)
collection = chroma_client.get_collection(name="resume_data", embedding_function=openai_ef)

def query_bot(user_query):
    # 1. RETRIEVE 
    results = collection.query(query_texts=[user_query], n_results=2)
    context_text = "\n\n".join(results['documents'][0])
    
    # 2. AUGMENT 
    system_prompt = """
    You are a helpful assistant answering questions about a candidate.
    Use ONLY the provided Context. If you don't know, say "I don't know".
    """
    
    prompt = f"""
    Context:
    {context_text}
    
    Question: 
    {user_query}
    """
    
    # 3. GENERATE
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content, context_text

if __name__ == "__main__":
    print("🤖 Resume Bot Live. Type 'exit' to quit.\n")
    while True:
        q = input("Recruiter: ")
        if q.lower() == "exit": break
        
        answer, source = query_bot(q)
        print(f"\nBot: {answer}")
        print(f"\n[Source Check]: {source[:100]}...\n") # Verification!