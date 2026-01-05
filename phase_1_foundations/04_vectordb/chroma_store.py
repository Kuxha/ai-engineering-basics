import chromadb

client = chromadb.PersistentClient(path="./chroma_db_data")
collection = client.get_or_create_collection(name="engineering_docs")


collection.upsert(
    documents=[
        "Python is a language for AI and Data Science.",
        "Pydantic enforces type hints at runtime.",
        "JavaScript is mainly used for frontend development."
    ],
    ids=["doc1", "doc2", "doc3"] # Unique IDs are required
)


results = collection.query(
    query_texts=["How do I validate my data schema?"],
    n_results=1
)

print(f"Top Match: {results['documents'][0][0]}")