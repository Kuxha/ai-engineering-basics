# The AI Engineering Handbook 🛠️

**Goal:** A ground-up implementation of the modern AI Engineering stack, moving from basic prompting to autonomous MCP agents.
**Focus:** Reliability, System Design, and building "Systems of Action" rather than just Chatbots.

> **Transparency Note:** This repository was built with the assistance of Google's Gemini, acting as a pair programmer and technical coach to structure the learning path and refine the code patterns.

---

## 📖 Why AI Engineering?
Most people stop at "Prompt Engineering"—typing text into ChatGPT.
**AI Engineering** is different. It is the discipline of treating Large Language Models (LLMs) not as magic boxes, but as **software components**.

This repository is a self-study guide designed to answer:
* How do we stop LLMs from hallucinating? (RAG)
* How do we connect them to our own database? (Tools)
* How do we build systems that can fix their own mistakes? (Agents)
* How do we deploy this to production reliably? (Evals & Ops)

---

## 🗺️ The Roadmap Philosophy
This curriculum follows a strict **"Crawl, Walk, Run"** progression. We do not jump straight to complex Agents because they are impossible to debug without strong foundations.

1.  **Phase 1 (The Brain):** We treat the LLM as a passive knowledge engine. We focus on controlling *what it knows* (RAG) and *how it speaks* (Prompting).
2.  **Phase 2 (The Hands):** We give the LLM the ability to *touch* the real world. We focus on **Determinism**—ensuring that when the AI tries to run code, it runs safely and predictably.
3.  **Phase 3 (The Logic):** We build the "Cortex." Simple scripts become **Graphs**. We handle loops, retries, and failures (e.g., "The API is down, what now?").
4.  **Phase 4 (The Protocol):** We standardize everything using **MCP (Model Context Protocol)**, the industry standard for connecting AI to systems.
5.  **Phase 5 (Production):** We treat it like real software. Testing, Caching, and Architecture.

---

## 🏗️ Phase 1: Foundations (The Brain)
*Goal: Control the LLM and give it access to knowledge.*

| Part | Topic | Engineering Pattern |
| :--- | :--- | :--- |
| **01** | **Prompting** | **In-Context Learning**: Constraining model tone/style without fine-tuning (Few-Shot). |
| **02** | **RAG Basics** | **Context Injection**: Grounding the model in static data to prevent hallucinations. |
| **03** | **Embeddings** | **Vector Math**: Matching queries by semantic meaning, not just keywords. |
| **04** | **Storage** | **Persistence**: Using ChromaDB (HNSW index) for scalable, long-term memory. |
| **05** | **Capstone 1** | **The Resume Bot**: An end-to-end RAG application with citation logic. |

---

## 🤖 Phase 2: Reliable Agents (The Hands)
*Goal: Transition from "Passive Chat" to "Active Work" using Tools and Pydantic.*

| Part | Topic | Engineering Pattern |
| :--- | :--- | :--- |
| **01** | **Tools** | **Deterministic Execution**: Letting LLMs trigger reliable Python functions (Math/API). |
| **02** | **Chains** | **Pipelines**: Breaking complex tasks into atomic, linear steps (A → B → C). |
| **03** | **Schemas** | **Pydantic**: Enforcing strict input/output validation. (No broken JSON). |
| **04** | **Memory** | **Context Buffers**: Managing conversation history in stateful applications. |
| **05** | **Routing** | **Intent Classification**: Using logic to route user queries to the correct tool. |

---

## 🕸️ Phase 3: Orchestration (The Logic)
*Goal: Building complex, self-correcting workflows that can recover from failure.*

| Part | Topic | Engineering Pattern |
| :--- | :--- | :--- |
| **01** | **LangGraph** | **Cyclic Graphs**: Enabling loops and retries (e.g., "Try again if error"). |
| **02** | **Persistence** | **Checkpointing**: Saving the agent's state to a database so it can resume later. |
| **03** | **Human-in-Loop** | **Approval Flows**: Pausing execution for human review before sensitive actions. |
| **04** | **Capstone 2** | **The Travel Agent**: A multi-step planner that searches, plans, and books. |

---

## 🔌 Phase 4: The MCP Protocol (Specialist Track)
*Goal: Mastering Anthropic's Model Context Protocol for standardizing AI connections.*

| Part | Topic | Engineering Pattern |
| :--- | :--- | :--- |
| **01** | **Architecture** | **Protocol Design**: Understanding Clients, Hosts, and Servers. |
| **02** | **FastMCP** | **Server Implementation**: Building robust Python servers with minimal boilerplate. |
| **03** | **Resources** | **Secure Data**: Exposing files and logs to the agent safely. |
| **04** | **Capstone 3** | **Health Ops Agent**: A production-grade Shift Assignment System (Pydantic + MCP). |

---

## 💎 Phase 5: Production Engineering (Scale)
*Goal: Testing, Optimization, and ensuring system reliability.*

| Part | Topic | Engineering Pattern |
| :--- | :--- | :--- |
| **01** | **Evals** | **Unit Testing**: Deterministic grading of non-deterministic AI outputs. |
| **02** | **Optimization** | **Caching**: Reducing latency and cost for repeated queries. |
| **03** | **System Design** | **Architecture**: Designing scalable agent systems for high-load environments. |

---

### 📚 Tech Stack
* **Languages:** Python (Strict Type Hinting)
* **Models:** GPT-4o-mini, text-embedding-3-small
* **Infrastructure:** ChromaDB, OpenAI SDK
* **Frameworks:** LangChain, LangGraph, Pydantic, FastMCP