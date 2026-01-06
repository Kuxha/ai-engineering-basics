# Phase 4, Day 15: Introduction to Graphs

**Goal:** We will transition from linear "Fire-and-Forget" scripts to **Stateful, Cyclic Agents** (State Machines) that can loop, retry, and pause.

---

## 📖 The "Why" (The Paradigm Shift)

To understand LangGraph, you must understand the limitation of what we built in Phase 3.

### The Problem: The "Domino" Mindset (Linear Chains)
In Phase 3, our code was a straight line:
`Input -> Search -> Answer -> Output`

Think of this like a row of **Dominoes**.
* **The Setup:** You line everything up perfectly.
* **The Action:** You flick the first domino.
* **The Failure:** If the "Search" domino falls slightly to the left (returns 0 results), it misses the next domino. The chain stops. The process is dead. You have to manually intervene to reset it.
* **Result:** Fragile.

### The Solution: The "Roomba" Mindset (Cyclic Graphs)
In Phase 4, we build **Graphs**.
Think of this like a **Roomba**.
* **The Goal:** "Clean the room" (Answer the question).
* **The Action:** It drives forward.
* **The Failure:** It bumps into a chair (Search returns 0 results).
* **The Reaction:** It doesn't power down. It has a sensor (Logic). It backs up, turns 30 degrees, and tries a new path. It keeps looping until the room is clean or it runs out of battery.
* **Result:** Resilient.

---

## 📂 The Files

### 1. `basic_graph.py` (The Hello World)
A simple "Straight Line" graph.
* **Structure:** `Start -> Agent -> End`
* **Purpose:** To teach you the syntax of `StateGraph` without the complexity of tools. It proves that a Graph can mimic a standard Chatbot.

### 2. `simple_agent.py` (The Loop)
A true "Cyclic" graph.
* **Structure:** `Start -> Agent <-> Tools`
* **Purpose:** To demonstrate the **Loop**.
* **The Magic:** We explicitly draw an edge from `Tools` *back* to `Agent`. This means the Agent can call a tool, see the result, and *then* decide what to do next (answer the user OR call another tool).

---

## 🧠 Key Concepts Explained

### 1. The State (`TypedDict`)
In a normal Python script, variables are scattered everywhere (`msg`, `response`, `tool_output`).
In a Graph, we have **One Shared Memory** called the State.

    class AgentState(TypedDict):
        messages: Annotated[List[BaseMessage], operator.add]

* **The Board Game Analogy:** Think of `State` as the game board. Every "Node" (Player) looks at the board, makes a move (adds a message), and passes the turn to the next player.
* **`operator.add`:** This tells the graph: "When a node returns data, do not DELETE the old history. ADD to it."

### 2. The Conditional Edge (The Router)
This is the "Brain" of the graph. It is a function that runs *between* nodes to decide the path.

    def should_continue(state):
        if state['messages'][-1].tool_calls:
            return "tools"  # The Loop (Go to Tool Node)
        return END          # The Exit (Finish)

### 3. The Cycle (The Edge)
This is the single most important line of code in Phase 4:

    workflow.add_edge("tools", "agent")

This line creates the **Roomba effect**. It says: "After you finish using a tool, **DO NOT STOP**. Go back to the Agent and report the result." This enables the agent to "think" about the tool's output.

---

## 🏃‍♂️ Usage

### Run the Linear Graph
(Behaves like a normal chatbot)
    python basic_graph.py

### Run the Cyclic Agent
(Can handle math problems by looping)
    python simple_agent.py

---

## 🔮 What's Next?
Now that we have a brain that can loop, we need to give it **Long-Term Memory**.
Currently, if you restart the script, the bot forgets everything. Next we will add **Persistence (SQLite)** so the Roomba remembers where it has already cleaned.