# Pattern: Few-Shot Prompting & Delimiters

**Tech Stack:** Python, OpenAI SDK

## The Problem
LLMs are non-deterministic by default. When asked to "rewrite text professionally" without guidance, the model often hallucinates the tone—sometimes sounding robotic, other times overly flowery. In a production pipeline, this inconsistency breaks downstream applications.

## The Solution
Implemented **In-Context Learning (Few-Shot Prompting)** to constrain the model's output space.

1.  **System Prompt:** Defines the strict persona ("Corporate Assistant").
2.  **Delimiters:** Used `####` to clearly separate system instructions from user data (preventing prompt injection).
3.  **Few-Shot Examples:** Provided 3 paired examples of [Dirty Input] -> [Clean Output] inside the message history.

## How to Run
```bash
# 1. Install dependencies
pip install openai python-dotenv

# 2. Set up environment
# Create a .env file with OPENAI_API_KEY=sk-...

# 3. Run the sanitizer
python few_shot_sanitizer.py