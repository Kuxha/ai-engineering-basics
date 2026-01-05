# Phase 2, Day 8: Structure (Pydantic)

**Goal:** Stop parsing unstable JSON manually. Use Pydantic to force the AI to return strict, type-safe Python objects.

## The Engineering Concept
One of the biggest risks in AI Engineering is **Parser Errors**.
* You ask for JSON.
* The AI returns `JSON` + some chatty text: *"Here is your JSON: {...}"*
* Your `json.loads()` crashes.

**The Solution: Structured Outputs**
OpenAI's `client.beta.chat.completions.parse` method allows us to pass a **Pydantic Model** directly to the API.
1.  The API guarantees the output will match your class schema.
2.  The Python SDK automatically converts the JSON response into a valid Python Object.

## Code Overview
In `structured_extraction.py`, we define a `SupportTicket` class.
* **`Literal[...]`**: This is a powerful feature. It forces the AI to choose from a pre-defined list (Enums). If the user says "My computer is broken," the AI maps it to `"hardware"`, not `"broken_computer"`.
* **`Field(description=...)`**: These are the "hints" the AI reads to understand what the field means.

## Usage

### 1. Install Pydantic
(It is likely installed, but just in case)
pip install pydantic

### 2. Run the Extractor
python structured_extraction.py

### 3. Expected Output
Notice how it perfectly categorizes "fire" as "hardware" and "high" priority without us writing any if/else logic.

Analyzing Email: 'My server is literally on fire...'

--- Extracted Data ---
User:     Alice
Category: hardware
Priority: HIGH
Summary:  Server hardware overheating/fire emergency.




---

## 🧠 Deep Dive: The "Hidden" Translation Layer

When you write `class SupportTicket(BaseModel)`, it feels like Python magic.
But OpenAI does not speak Python. It speaks **JSON Schema**.

Here is what actually happens when you press "Run":

### 1. The Translation
Before the request leaves your laptop, the SDK inspects your Pydantic class and converts it into a strict JSON Schema definition.

**Your Python Code:**

    class SupportTicket(BaseModel):
        summary: str = Field(description="A concise summary.")
        priority: Literal["high", "low"]

**What OpenAI Actually Receives:**

    {
      "type": "json_schema",
      "json_schema": {
        "name": "SupportTicket",
        "schema": {
          "type": "object",
          "properties": {
            "summary": { "type": "string", "description": "A concise summary." },
            "priority": { "type": "string", "enum": ["high", "low"] }
          },
          "required": ["summary", "priority"],
          "additionalProperties": false
        },
        "strict": true
      }
    }

### 2. The Constraint (Prompt Engineering via Schema)
Notice that your `description="..."` field is passed to the model.
* **This is why descriptions matter.** The model reads them as instructions.
* **The "Enum" constraint:** Because `priority` is defined as `["high", "low"]`, the model is mathematically incapable of generating the word "medium." It must pick a token from the allowed list.

### 3. The Validation
When the JSON comes back, Pydantic runs it against your class.
* If the AI returns `{"priority": "HIGH"}` (uppercase), Pydantic fixes it or raises an error depending on your settings.
* This protects your downstream code (e.g., database saves) from crashing due to dirty data.