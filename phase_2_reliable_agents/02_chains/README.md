# Phase 2, Day 7: Chains (Multi-Step Reasoning)

**Goal:** Build a loop that allows the AI to call multiple tools in a sequence to solve complex problems.

## The Engineering Concept
In Day 6, we built a "One-Shot" agent: Question -> Tool -> Answer.
But most real-world questions require multiple steps.

**The Chain Pattern:**
1.  **Loop:** We wrap the model interaction in a `while True` loop.
2.  **History:** We append every tool output back to the `messages` list.
3.  **Termination:** The loop breaks only when the AI decides it has enough information to generate a text response (i.e., `tool_calls` is empty).

## Code Overview
In `chain_simulation.py`, we simulate a classic dependency problem:
* **Goal:** Find order status.
* **Problem:** We only have an email (`alice@example.com`), but the order database requires a User ID (`USR-100`).
* **Solution:** The AI autonomously figures out it must call `get_user_details` first, get the ID, and *then* call `get_recent_order`.

## Usage

### 1. Run the Chain
python chain_simulation.py

### 2. Trace the Flow
Watch the terminal. You will see the AI "thinking" in steps.

Step 1: AI realizes it needs the User ID.
> AI Decision: Call get_user_details with {'email': 'alice@example.com'}

Step 2: AI gets "USR-100" and realizes it can now check the order.
> AI Decision: Call get_recent_order with {'user_id': 'USR-100'}

Step 3: AI gets the order status and answers the user.
> Agent: The latest order for Alice is a Laptop, and it has been Shipped.