import os
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv

load_dotenv()

client = chromadb.PersistentClient(path="./chroma_db")
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.getenv("OPENAI_API_KEY"),
    model_name="text-embedding-3-small"
)
collection = client.get_or_create_collection(name="resume_data", embedding_function=openai_ef)

def ingest_file(file_path):
    with open(file_path, 'r') as f:
        text = f.read()
    
    chunks = [p for p in text.split('\n\n') if p.strip()]
    
    print(f"Adding {len(chunks)} chunks to database...")
    
    collection.upsert(
        documents=chunks,
        ids=[f"chunk_{i}" for i in range(len(chunks))],
        metadatas=[{"source": "resume.txt"} for _ in range(len(chunks))]
    )
    print("✅ Ingestion Complete.")

if __name__ == "__main__":
  
    if not os.path.exists("data/resume.txt"):
        os.makedirs("data", exist_ok=True)
        with open("data/resume.txt", "w") as f:
            f.write("EXPERIENCE\n\nSoftware Engineer at TechCorp (2020-2024).\nFocused on Python backend and AWS.\n\nEDUCATION\n\nMasters in CS from NYU.")
    
    ingest_file("data/resume.txt")