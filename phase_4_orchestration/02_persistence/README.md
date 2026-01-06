# Phase 4, Day 16: Persistence (Memory)

**Goal:** Give the Agent "Long-Term Memory" so it can remember users and conversations across server restarts.

---

## 📖 The "Why" (The Amnesia Problem)

In Day 15, our Agent was "Stateless."
* **The Issue:** If the Python script stopped, the `messages` list in RAM disappeared.
* **The Consequence:** The user had to restart the conversation from scratch every time.
* **The Solution:** We implement a **Checkpointer**. This saves the state of the graph to a database after every single step (Node execution).

---

## 📂 The Files

### 1. `memory_agent.py` (Short-Term RAM)
* **Backing Store:** `MemorySaver()`
* **Behavior:** Saves state to a Python dictionary in RAM.
* **Use Case:** Unit testing, quick debugging.
* **Limitation:** If you kill the script, the memory is lost.

### 2. `sqlite_agent.py` (Long-Term Disk)
* **Backing Store:** `SqliteSaver()`
* **Behavior:** Saves state to a local file (`checkpoints.sqlite`).
* **Use Case:** Local development, production (single server).
* **Advantage:** You can kill the script, restart your computer, and the Agent still remembers "Thread ID 1".

---

## 🧠 Deep Dive: How Persistence Works

LangGraph uses a system called **"Thread-Level Persistence."**

### 1. The Thread ID
Every time you run the agent, you pass a configuration dictionary. This ID acts as the "Primary Key" in the database.

    config = {"configurable": {"thread_id": "user_123"}}

### 2. The Checkpoint Cycle
* **Load:** Before the Agent runs, it queries the DB: `SELECT state FROM checkpoints WHERE thread_id="user_123"`.
* **Hydrate:** It populates the graph's `messages` list with that history.
* **Execute:** The Agent runs, calls tools, generates text.
* **Save:** After the node finishes, it writes the *new* state back to the DB.

### 3. Understanding the SQLite Files
When you run `sqlite_agent.py`, you will see three files appear. This is normal for SQLite in **WAL (Write-Ahead Log)** mode:

* **`checkpoints.sqlite`**: The main database file.
* **`checkpoints.sqlite-wal`**: A temporary "journal" where new writes go first for speed.
* **`checkpoints.sqlite-shm`**: A shared memory index for the WAL file.

> **⚠️ Security Warning:** Never commit these files to GitHub. They contain your private chat history. Add `*.sqlite` to your `.gitignore`.

---

## 🏃‍♂️ Usage Guide

### 1. Installation
The SQLite checkpointing logic is in a separate package:

    pip install langgraph-checkpoint-sqlite

### 2. Running the Persistent Agent

    python3 sqlite_agent.py

### 3. Testing Memory (The "Amneisa Check")
To prove persistence works, follow this protocol:

* **Run 1:** Start the script. Enter Thread ID `1`. Tell the bot: "My code is 1234." Quit the script.
* **Run 2:** Start the script. Enter Thread ID `2`. Ask: "What is my code?" (Result: "I don't know" -> Proves isolation). Quit.
* **Run 3:** Start the script. Enter Thread ID `1`. Ask: "What is my code?" (Result: "1234" -> Proves memory).

---

## 🔮 What's Next?
Now that the Agent has a **Brain** (Logic) and **Memory** (Persistence), we need to give it **Management Skills**.
In **Day 17**, we will build the **Supervisor Pattern**: A manager agent that orchestrates multiple worker agents (Researcher, Coder, Reviewer).