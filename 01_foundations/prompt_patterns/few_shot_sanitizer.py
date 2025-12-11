import os
import openai
from dotenv import load_dotenv

# Here we load env vars from .env file
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def sanitize_update(raw_input):
    """
    Takes a raw string and returns a polite professional summary.
    """
    system_instruction = """
    You are a professional corporate assistant. 
    Rewrite the user's technical input into a calm, executive-level summary.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",  
        messages=[
            {"role": "system", "content": system_instruction},
            
            # FEW-SHOT EXAMPLE 1
            {"role": "user", "content": "Input: #### db died, redis is full ####"},
            {"role": "assistant", "content": "Output: The database is experiencing a service interruption due to capacity limits in the caching layer."},
            
            # FEW-SHOT EXAMPLE 2
            {"role": "user", "content": "Input: #### api is slow as hell, checking logs ####"},
            {"role": "assistant", "content": "Output: API latency is currently elevated; the team is investigating logs to identify the root cause."},

            # FEW-SHOT EXAMPLE 3 
            {"role": "user", "content": "Input: #### third party api down. need to contact  ####"},
            {"role": "assistant", "content": "Output: A third-party API is currently unavailable; we are reaching out to their support team for assistance."},

            # THE ACTUAL TASK
            {"role": "user", "content": f"Input: #### {raw_input} ####"}
        ]
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    # Test loop
    while True:
        user_input = input("\nEnter rough update (or 'exit'): ")
        if user_input.lower() == 'exit': break
        print(f"\n> {sanitize_update(user_input)}")