"""
 Naive RAG (Keyword Retrieval) - Hello World of RAG

Purpose: Demonstrates the 'Context Injection' pattern. 
Limitation: Uses hardcoded keyword matching ('if code in input'). 
Future: Will replace keyword matching with Vector Embeddings for semantic retrieval.
"""

import os
import openai
from dotenv import load_dotenv

# Here we load env vars from .env file
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

knowledge_base = "Secret: The code is 1234"

def take_user_input(user_input):
  print(user_input)

def generate_response(user_input):
    """
    Generates a response using retrieval-augmented generation (RAG) approach.
    """
    # Simple retrieval step
    if "code" in user_input.lower():
        retrieved_info = knowledge_base
    else:
        retrieved_info = "I don't have information on that."

    # Generation step
    prompt = f"User asked: {user_input}\nRetrieved info: {retrieved_info}\nProvide a helpful response based on the retrieved information."
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an assistant that provides information based on retrieved knowledge."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ("quit", "exit"):
            break
        
        take_user_input(user_input)
        response = generate_response(user_input)
        print("Assistant:", response)

# Naive Retrieval-Augmented Generation (RAG) Example
# This example demonstrates a simple RAG system that retrieves information from a static knowledge base.
    