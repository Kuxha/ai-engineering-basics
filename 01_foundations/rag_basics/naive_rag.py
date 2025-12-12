import os
import openai
from dotenv import load_dotenv

# Here we load env vars from .env file
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

knowledge_base = "Secret: The code is 1234"



if __name__ == "__main__":
    user_input = "What is the code?"
    take_user_input(user_input)
    response = generate_response(user_input)
    print(response)
# Naive Retrieval-Augmented Generation (RAG) Example
# This example demonstrates a simple RAG system that retrieves information from a static knowledge base.
    