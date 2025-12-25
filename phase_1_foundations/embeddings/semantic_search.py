import os
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()
client = OpenAI()

def get_embedding(text):
    """Generates vector for a given text."""
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding

def main():
 
    documents = [
        "The cat sits on the mat",
        "A dog chases the ball",
        "The software engineer writes python",
        "I love eating pizza"
    ]
    

    query = "A feline is resting" 
    
    print(f"Query: '{query}'\n")

    # 3. Vectorize everything
    query_vec = get_embedding(query)
    doc_vecs = [get_embedding(doc) for doc in documents]

    similarities = cosine_similarity([query_vec], doc_vecs)[0]

    for i, doc in enumerate(documents):
        print(f"Doc: '{doc}' | Similarity: {similarities[i]:.4f}")

if __name__ == "__main__":
    main()