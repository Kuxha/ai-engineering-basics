import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)
client = OpenAI()

# --- THE MEMORY BANK ---
# This list IS the memory. If this list is lost (e.g., script crashes), memory is gone.
conversation_history = [
    {
        "role": "system", 
        "content": "You are a helpful assistant named Jarvis. You are sarcastic but helpful."
    }
]

def run_chat():
    print("--- Starting Chat (Type 'exit' to stop) ---")
    
    while True:
        # 1. Get input from the user
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]:
            break
            
        # 2. Add USER message to history
        conversation_history.append({"role": "user", "content": user_input})
        
        # 3. Send the ENTIRE history to the model
        # The model reads the System Prompt + User Msg 1 + AI Reply 1 + User Msg 2...
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=conversation_history
        )
        
        assistant_message = response.choices[0].message.content
        
        # 4. Add ASSISTANT message to history
        # If we skip this, the AI will forget what it just said in the next turn.
        conversation_history.append({"role": "assistant", "content": assistant_message})
        
        print(f"Jarvis: {assistant_message}")

        # Debug: Uncomment this to see the list grow!
        # print(f"\n[DEBUG] History Length: {len(conversation_history)}")

if __name__ == "__main__":
    run_chat()