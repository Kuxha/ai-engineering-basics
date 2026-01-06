# Phase 4 Capstone: Shift Orchestrator (ShiftFinder)

**Goal:** Build a production-grade, semi-autonomous agent that solves the "Provider Scheduling Problem" using strict constraints, deterministic mathematics, and Human-in-the-Loop safety checks.

---

## 📖 Project Overview

This system allows a user to request healthcare staff using natural language (e.g., *"I need an ICU nurse in Brooklyn"*). Instead of relying on an LLM to "guess" the best candidate, this project implements a **Hybrid Architecture**:

1.  **The Brain (LLM):** Parses unstructured text into structured constraints (Location, Skills).
2.  **The Hands (Python):** Executes a deterministic **Weighted Scoring Algorithm** to rank candidates based on distance, rating, and preference.
3.  **The Gatekeeper (LangGraph):** Pauses the workflow for human verification before any external communication (SMS/Email) is drafted.

---

## 🏗️ Architecture

The system is built on the **Supervisor Pattern** using `LangGraph`.

**The Flow:**
1.  **User Request:** "Find a nurse..."
2.  **Intake Agent:** Extracts JSON constraints (Pydantic).
3.  **Scheduler Tool:** Calculates specific scores (Python).
4.  **Pause:** System halts for Compliance Review.
5.  **Drafter:** If approved, generates the SMS.

### The Components

| Component | Technology | Responsibility |
| :--- | :--- | :--- |
| **Intake Agent** | GPT-4o-mini + Pydantic | Extract strict constraints from vague user prompts. |
| **Scheduler Tool** | Python (Haversine/Math) | Calculate optimal matches using geospatial math and weighted scoring. |
| **Orchestrator** | LangGraph StateMachine | Manage state, handle routing, and enforce the "Compliance Pause." |

---

## 🧠 Technical Deep Dive

This project prioritizes **Reliability** over "generative creativity." Here are the core engineering decisions:

### 1. Geospatial Precision (Haversine vs. Euclidean)
* **The Problem:** Many basic routing apps use Euclidean distance (`sqrt((x2-x1)^2 + (y2-y1)^2)`). This assumes the Earth is flat, introducing significant errors over long distances.
* **The Solution:** We implemented the **Haversine Formula**.
    * It calculates the Great-Circle distance between two points on a sphere.
    * This ensures that "Distance" metrics are physically accurate for real-world travel estimation.

### 2. Multi-Objective Optimization (Weighted Scoring)
How do you compare a provider who is **2 miles away** (Good) but has a **3.0 Rating** (Average) against one **10 miles away** (Bad) with a **5.0 Rating** (Excellent)?

We cannot simply add `Distance + Rating` because the units differ. We solved this using **Min-Max Normalization**:

1.  **Normalization:** We scale all metrics to a `0.0 - 1.0` range.
    
        NormDistance = (Value - Min) / (Max - Min)

2.  **Inversion:** For distance, "Lower is Better." We invert the score:

        Score = 1.0 - NormDistance

3.  **Weighted Sum:** We apply configurable business logic weights:

        FinalScore = (DistanceScore * 0.50) + (RatingScore * 0.30) + (PreferenceScore * 0.20)

    * *Benefit:* This makes the ranking algorithm tunable via configuration files without code changes.

### 3. Framework-Level Safety (The "Interrupt")
Instead of asking the LLM to "please ask for permission," we enforce safety at the infrastructure level.

* **Mechanism:** workflow.compile(interrupt_before=["Compliance"])

* **Behavior:** When the Scheduler selects a candidate, the graph **physically terminates** execution and persists the state to a database.
* **Security:** It is impossible for the Agent to draft or send a message without an external API call to resume the thread. This protects against Prompt Injection attacks that might try to bypass approval.

---

## 📂 File Structure

    phase_4_orchestration/capstone/
    ├── main.py         # The LangGraph Orchestrator (Flow Logic)
    ├── tools.py        # The Deterministic Math & Database (Business Logic)
    └── README.md       # Documentation

---

## 🏃‍♂️ Usage Guide

### 1. Installation
Ensure you have the required dependencies:

    pip install langgraph langchain-openai python-dotenv

### 2. Running the Agent

    python3 phase_4_orchestration/capstone/main.py

### 3. Example Interaction

**User:** "I need an ICU nurse in Brooklyn."

**System Logs:**

    [Intake] Parsed Location: Brooklyn, Skill: ICU
    [System] Running Weighted Scoring Algorithm...
    [Tool] Searching DB...
       -> Found Sarah (Brooklyn): Dist 0.0mi, Rating 4.8
       -> Found Jessica (Queens): Dist 8.5mi, Rating 4.9
    [Math] Normalizing scores...
    [Math] Winner: Sarah (Score: 0.94) due to distance weight.

**System Pause:**

    --- ⏸️ COMPLIANCE CHECK REQUIRED ⏸️ ---
    Tool Output: Found Sarah Jones in Brooklyn (0.0 miles away).
    Do you approve this provider match? (yes/no): 

**User:** `yes`

**System:**

    --- ✅ Approved. Sending SMS... ---
    Final Response: [SYSTEM] Provider identified. Drafting recruitment SMS...