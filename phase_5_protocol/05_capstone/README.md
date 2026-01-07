# Phase 5 Capstone: Health Ops System (MCP & Agents)

**Goal:** Build a "System of Action" that autonomously manages hospital operations.
**Stack:** Python 3.12, Pydantic AI, FastMCP, SQLite, Logfire.

---

## 1. The Architecture

We moved beyond simple chatbots. This is a **Microservices Architecture** simulated locally. The system follows a strict request-response lifecycle where the LLM serves as the orchestrator, not just a text generator.



### The Components

* **The Database (hospital.db):** The single source of truth. It contains patients, doctors, and appointment slots.
* **The Server (hospital_server.py):** The "Backend." It exposes deterministic tools (get_patient, book_slot) via the Model Context Protocol (MCP). It enforces data integrity at the database level.
* **The Agent (hospital_agent.py):** The "Frontend." It uses an LLM to reason about the user's intent, calls the server tools to fetch data, and enforces the "Medical Triage Protocol."
* **Observability (Logfire):** The "X-Ray." It traces every thought, tool call, and validation step.

---

## 2. Setup & Installation

**Step 1: Dependencies**
Ensure you are in the project root and your virtual environment is active.

    pip install -r phase_5_protocol/05_capstone/requirements.txt

**Step 2: Database Initialization**
We wipe and re-seed the database to ensure reproducible tests and clean state.

    python phase_5_protocol/05_capstone/database.py

**Step 3: Logfire Authentication**
Associate your machine with your Pydantic Logfire project.

    logfire auth

---

## 3. How to Run

**Execute the Agent:**

    python phase_5_protocol/05_capstone/hospital_agent.py

### The "Happy Path" (John Doe)
* **Query:** "I am John Doe... I have a migraine."
* **Behavior:**
    1. Agent searches for "John Doe" using the MCP tool -> Found.
    2. Agent identifies "Migraine" -> Logic determines a need for "Diagnostic".
    3. Agent lists slots for "Diagnostic" specialty -> Finds Dr. House at 09:00.
    4. Agent executes the booking tool -> Success.
    5. **Database State Change:** The slot is now marked 'booked' in the SQLite file.

### The "Unhappy Path" (Unknown Patient)
* **Query:** "I am Laba Deka... broken arm."
* **Behavior:**
    1. Agent searches for "Laba Deka" -> Server returns "Not Found".
    2. Agent follows Protocol Rule #1: **Abort**.
    3. Returns `booking_success=False` without attempting to book a doctor.

---

## 4. Technical Deep Dive

### A. The Server (FastMCP)
We use `FastMCP` to wrap Python functions. The key innovation here is **Statelessness**. We open and close the DB connection inside every function call to avoid threading issues and deadlocks in asynchronous contexts.

    @mcp.tool()
    def book_appointment(slot_id: int, patient_id: int) -> str:
        # 1. Opens connection to hospital.db
        # 2. Checks if slot is 'open' and patient exists
        # 3. Commits SQL UPDATE transaction
        # 4. Returns deterministic result string

### B. The Agent (Pydantic AI)
We enforce a **Strict Contract**. The Agent is not allowed to return free-form text. It must return a `TriageResult` object.

    class TriageResult(BaseModel):
        summary: str
        booking_success: bool
        doctor_name: Optional[str]
        slot_time: Optional[str]

This guarantees that any downstream system or UI can reliably parse the output without the fragility of Regex or string matching.

### C. The Protocol (MCP)
We do not use traditional HTTP or REST APIs. We utilize **Stdio (Standard Input/Output)**.
* The Agent (Host) spawns the Server as a child subprocess.
* Communication occurs via JSON-RPC messages over the terminal pipes.
* **Benefit:** Zero network latency, local security, and perfect isolation of the data layer.

---

## 5. Troubleshooting & Lessons Learned

### Issue: AttributeError: 'AgentRunResult' object has no attribute 'data'
* **Context:** Pydantic AI is in active development (v0.0.18+).
* **The Fix:** The library renamed `.data` to **`.output`**.
* **Senior Insight:** Always use `dir(object)` to inspect attributes when working with bleeding-edge libraries.

### Issue: Missing API Key Errors
* **Context:** OpenAIError on script startup.
* **The Fix:** Explicitly loading environment variables using `python-dotenv` at the very top of the script.

    from dotenv import load_dotenv
    load_dotenv() # Injects keys before Agent initialization