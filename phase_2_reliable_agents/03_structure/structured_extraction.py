import os
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Literal

load_dotenv(override=True)
client = OpenAI()

# --- PART 1: DEFINE THE RULES (The "Shape") ---
# We use Pydantic to define exactly what we want.
# The AI must fill in this form. It cannot invent new fields.

class SupportTicket(BaseModel):
    user_name: str = Field(description="The name of the user mentioned in the text.")
    
    # Literal enforces a "Multiple Choice" question. 
    # The AI CANNOT say "Laptop" or "Screen". It MUST pick "hardware", "software", or "billing".
    category: Literal["hardware", "software", "billing"] = Field(
        description="The category of the issue."
    )
    
    priority: Literal["low", "medium", "high"] = Field(
        description="Assess the urgency. 'high' if the user is angry or blocked."
    )
    
    summary: str = Field(description="A concise 5-word summary of the problem.")

# --- PART 2: THE EXTRACTION (The "Enforcer") ---

def analyze_email(email_text):
    print(f"\nAnalyzing Email:\n'{email_text}'\n")

    # We use the new '.parse' method from OpenAI.
    # We pass our Pydantic class to 'response_format'.
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Extract the support ticket details."},
            {"role": "user", "content": email_text},
        ],
        response_format=SupportTicket, # <--- The Magic Line
    )

    # The result is NOT a dictionary. It is a real Python Object.
    ticket = completion.choices[0].message.parsed
    
    # We can access fields with dot notation (ticket.priority), not brackets (ticket['priority'])
    # This means your IDE can autocomplete these fields!
    print("--- Extracted Data ---")
    print(f"User:     {ticket.user_name}")
    print(f"Category: {ticket.category}")
    print(f"Priority: {ticket.priority.upper()}")
    print(f"Summary:  {ticket.summary}")

if __name__ == "__main__":
    # Test 1: A software issue
    email_1 = "Hi, I'm John Doe. My login isn't working and I need to submit a report by 5pm!"
    analyze_email(email_1)

    # Test 2: A hardware issue (Note: It infers category 'hardware' from 'smoke')
    email_2 = "This is Alice. My server is literally on fire and smoking. Help!"
    analyze_email(email_2)