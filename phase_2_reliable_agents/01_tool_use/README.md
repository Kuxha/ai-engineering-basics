# Phase 2, Day 6: Manual Tool Use

**Goal:** Understand the fundamental mechanics of how Large Language Models (LLMs) interact with external code (Tools).

## The Engineering Concept
LLMs are isolated text-generation engines. They cannot directly access databases or APIs. To bridge this gap, we use **Tool Calling** (or Function Calling).

This involves a 3-step handshake:
1.  **Definition:** The developer provides a JSON schema describing available functions (Tools).
2.  **Selection:** The LLM analyzes the user prompt and, if necessary, outputs a structured request to call a specific function with specific arguments.
3.  **Execution:** The runtime (this script) intercepts the request, executes the actual Python code, and feeds the result back to the LLM for the final response.

## Code Overview
In `manual_tool_calling.py`, we implement this loop from scratch without using high-level frameworks (like LangChain or FastMCP).
* **The Tool:** `get_order_status` simulates a database lookup.
* **The Schema:** `tools_schema` defines the interface for the LLM.
* **The Loop:** We manually parse the `tool_calls` from the OpenAI response and execute the corresponding function.

This pattern is the foundational building block for all Agentic workflows.

## Usage

### 1. Run the Agent
Execute the script to see the tool calling process in the terminal logs.
```
    python manual_tool_calling.py
```
### 2. Expected Output
You will see the "Brain" request the tool, the "Hands" execute it, and the "Brain" formulate the final answer.
```
    User Query: Where is my order ORD-123?
    Model requested a tool call.
       Function: get_order_status
       Arguments: {'order_id': 'ORD-123'}
       Output: {"status": "shipped", "delivery_date": "2023-10-25"}
    Agent Response: Your order ORD-123 has been shipped and is expected to be delivered on October 25, 2023.

```

![alt text](screenshot.png)



---

## 🧠 Deep Dive: The "Handshake" Illusion

A common misconception is that the AI has access to your computer or runs the code itself. **It does not.**
The AI is just a text generator. It generates a *request* for you to run code.

### The 4-Step Choreography

#### Step 1: The Setup (You)
You send the user prompt AND a "Menu" of available tools.
* *Prompt:* "Where is order 123?"
* *Tools:* `[ { "name": "get_order", "parameters": ... } ]`

#### Step 2: The Decision (AI)
The AI analyzes the prompt. It realizes it cannot answer with its training data.
Instead of writing a chat response, it generates a special **Tool Call Object**:

    {
      "content": null,
      "tool_calls": [
        {
          "function": {
            "name": "get_order",
            "arguments": "{\"order_id\": \"123\"}"
          }
        }
      ]
    }

#### Step 3: The Execution (You)
Your Python script sees this object.
* It **pauses** the chat.
* It runs `get_order("123")` on your local machine.
* It gets the result: `{"status": "shipped"}`.

#### Step 4: The Synthesis (AI)
You give the result back to the AI.
* *Input:* "The tool returned: `{'status': 'shipped'}`"
* *Output:* "Your order has been shipped!"

**Key Takeaway:** You are the engine. The AI is just the steering wheel.




### ⚠️ The Danger Zone: Argument Mismatches
The AI "knows" your function signatures because you sent it a `tools` schema (JSON) at the start of the chat.

However, the AI is probabilistic. It might hallucinate an extra argument or forget a required one.
* **If AI sends:** `get_order(id="123")` (Wrong key name: `id` instead of `order_id`)
* **Python executes:** `get_order(id="123")`
* **Result:** `TypeError: get_order() got an unexpected keyword argument 'id'`

**The Fix:** In production systems (like Phase 2, 03 ), we use validation libraries (Pydantic) to catch these errors before they crash the program.