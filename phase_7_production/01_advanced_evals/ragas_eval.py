import os
import asyncio
from datasets import Dataset 
from ragas import evaluate
# FIX: Updated imports to silence DeprecationWarnings
from ragas.metrics import faithfulness, answer_relevancy
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from dotenv import load_dotenv
import pandas as pd

# Load env vars
load_dotenv()

# --- 1. THE DATASET (Ground Truth) ---
data_samples = {
    'question': [
        'What are the symptoms of a migraine?',
        'Who is the cardiologist on duty?',
        'How do I book an appointment?'
    ],
    'answer': [
        # 1. High Quality Answer
        'Symptoms include severe throbbing pain, usually on one side, sensitivity to light, and nausea.',
        # 2. Hallucination (Dr. House is correct, but the time 2 PM might be hallucinated if not in context?)
        # Let's see what the judge thinks.
        'Dr. House is the cardiologist available at 2 PM.',
        # 3. Vague Answer (Low Relevancy)
        'You can book using the book_appointment tool with a slot ID.'
    ],
    'contexts': [
        ['Migraines are characterized by pulsing headaches, nausea, and photosensitivity.'],
        ['Dr. House (Cardiology) has slots open at 14:00 and 15:00.'],
        ['To book, use the booking tool. Provide patient ID and slot ID.']
    ],
    'ground_truth': [
        'Severe throbbing pain, usually on one side, nausea, and light sensitivity.',
        'Dr. House.',
        'Use the booking tool with the slot ID and patient ID.'
    ]
}

def run_evaluation():
    print("⚖️  Starting RAGAS Evaluation (Judge: GPT-4o)...")
    
    # 1. Convert Dictionary to HuggingFace Dataset
    dataset = Dataset.from_dict(data_samples)

    # 2. Configure the "Judge" Models
    gpt4 = ChatOpenAI(model="gpt-4o")
    embeddings = OpenAIEmbeddings()

    # 3. Run the Evaluation
    results = evaluate(
        dataset,
        metrics=[
            faithfulness,
            answer_relevancy,
        ],
        llm=gpt4,
        embeddings=embeddings
    )

    print("\n--- 📊 RAGAS REPORT ---")
    print(results)
    
    # 4. Senior Engineer Analysis
    df = results.to_pandas()
    
    # FIX: Dynamically find the question column to avoid KeyError
    # Ragas sometimes renames 'question' to 'user_input'
    question_col = 'user_input' if 'user_input' in df.columns else 'question'
    
    print("\n--- DETAILED BREAKDOWN ---")
    # Set pandas display options to see the full text
    pd.set_option('display.max_colwidth', 50)
    
    if question_col in df.columns:
        print(df[[question_col, 'faithfulness', 'answer_relevancy']])
    else:
        # Fallback: Print all columns if we can't find the specific one
        print(df)

if __name__ == "__main__":
    run_evaluation()