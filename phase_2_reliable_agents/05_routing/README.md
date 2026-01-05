# Phase 2, Day 10: The Router Agent

**Goal:** Build an agent that autonomously decides between "Chatting" and "Working."

## The Engineering Concept
A **Router** is the core of any advanced agent system. It prevents the AI from being a "one-trick pony."

* **Scenario A (Chat):** User says "Hi." -> Router sees no need for tools -> Returns text.
* **Scenario B (Work):** User says "Check TKT-123." -> Router sees a matching tool -> Triggers function.

This is achieved using `tool_choice="auto"`. We give the AI the *option* to use tools, but we don't *force* it. The AI uses its internal reasoning to decide if the tool is necessary for the current prompt.

## Usage

### 1. Run the Agent
    python router_agent.py

### 2. Test the Routing
Try these distinct inputs to see the "Switch" flip:

* **Input:** "Hello, who are you?"
    * **Result:** [ROUTER] Decision: General Chat.
    * **Agent:** "I am the Gatekeeper..."
* **Input:** "Check status of TKT-456"
    * **Result:** [ROUTER] Decision: Database Lookup Needed.
    * **Agent:** "Ticket TKT-456 is currently Closed - Resolved."
* **Input:** "Tell me a joke."
    * **Result:** [ROUTER] Decision: General Chat.

## Deep Dive: The "Auto" Parameter
When we set `tool_choice="auto"`, OpenAI calculates a probability score.
* If `Probability(Need Tool) > Threshold`, it generates a `tool_call`.
* Otherwise, it generates `content` (text).
    
This creates the illusion of "intelligence"—the agent appears to "know" when to work and when to talk.

---

## 🧠 Deep Dive: Why do we need "Routing" logic?

You might ask: *"Can't I just send the tools and let the AI figure it out?"*

If you attach tools but don't write the Python `if/else` block to handle them, you get **The Silent Fail**.

### The Scenario
**User:** "Check ticket TKT-123."
**AI:** Accurately decides to use the tool.

**The Response Object:**
The AI returns a specific packet structure:
* `content`: `null` (It has nothing to say *yet*)
* `tool_calls`: `[{ name: "get_ticket", ... }]`

### The Crash
If your Python code looks like a standard chatbot:
```python
print(response.choices[0].message.content)