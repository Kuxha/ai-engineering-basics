# The AI Engineering Handbook

**Goal:** A ground-up implementation of the modern AI Engineering stack, moving from basic prompting to autonomous MCP agents.
**Focus:** Reliability, System Design, and building "Systems of Action" rather than just Chatbots.

> **Transparency Note:** This repository was built with the assistance of Google's Gemini, acting as a pair programmer and technical coach. It is a repository that helped me consolidate many of the ideas and things learnt during the process.

# Motivation

I have been learning and building this repository as a comprehensive reference point for AI Engineering. I have tried to make it as generic and accessible as possible so that anyone who wants to transition to AI Engineering can use this documentation and code as a solid foundation.

---

## Why AI Engineering?
Most people stop at "Prompt Engineering"—typing text into ChatGPT.
**AI Engineering** is different. It is the discipline of treating Large Language Models (LLMs) not as magic boxes, but as **software components**.

This repository is a self-study guide designed to answer:
* How do we stop LLMs from hallucinating? (RAG)
* How do we connect them to our own database? (Tools)
* How do we build systems that can fix their own mistakes? (Agents)
* How do we deploy this to production reliably? (Evals & Ops)

---

## Setup & Installation
Follow these steps to configure your environment for all phases.

**1. Clone and Configure Environment**

    # Create a virtual environment
    python3 -m venv .venv

    # Activate it (Mac/Linux)
    source .venv/bin/activate
    # Activate it (Windows)
    .venv\Scripts\activate

**2. Install Dependencies**

    pip install -r requirements.txt

**3. Set API Keys**
Create a file named `.env` in the root folder and add your keys:

    OPENAI_API_KEY=sk-proj-...
    TAVILY_API_KEY=tvly-...
    GCP_PROJECT_ID=...
    GOOGLE_APPLICATION_CREDENTIALS=/abs/path/to/key.json

---

## The Roadmap Philosophy
This curriculum follows a strict **"Crawl, Walk, Run"** progression. We do not jump straight to complex Agents because they are impossible to debug without strong foundations.

1.  **Phase 1 (The Brain):** Treats the LLM as a passive knowledge engine. Focuses on RAG and Prompting.
2.  **Phase 2 (The Hands):** Gives the LLM the ability to execute code. Focuses on Tool Use and Determinism.
3.  **Phase 3 (The Application):** Combines Brain and Hands into Agentic RAG with citations and self-correction.
4.  **Phase 4 (The Logic):** Introduces "Cortex" logic using Graphs (loops, retries, persistence).
5.  **Phase 5 (The Protocol):** Standardizes connections using MCP and Pydantic AI.
6.  **Phase 6 (The Intelligence):** Implements Vendor Agnosticism (Multi-Model Routing).
7.  **Phase 7 (Production):** Focuses on Scale, Evals, Caching, and Docker Deployment.

---

## Phase 1: Foundations (The Brain)
*Goal: Control the LLM and give it access to knowledge.*

| Part | Topic | Engineering Pattern |
| :--- | :--- | :--- |
| **01** | **Prompting** | **In-Context Learning**: Constraining model tone/style without fine-tuning (Few-Shot). |
| **02** | **RAG Basics** | **Context Injection**: Grounding the model in static data to prevent hallucinations. |
| **03** | **Embeddings** | **Vector Math**: Matching queries by semantic meaning, not just keywords. |
| **04** | **Storage** | **Persistence**: Using ChromaDB (HNSW index) for scalable, long-term memory. |
| **05** | **Capstone 1** | **The Resume Bot**: An end-to-end RAG application with citation logic. |

---

## Phase 2: Reliable Agents (The Hands)
*Goal: Transition from "Passive Chat" to "Active Work" using Tools and Pydantic.*

| Part | Topic | Engineering Pattern |
| :--- | :--- | :--- |
| **01** | **Tools** | **Deterministic Execution**: Letting LLMs trigger reliable Python functions (Math/API). |
| **02** | **Chains** | **Pipelines**: Breaking complex tasks into atomic, linear steps (A -> B -> C). |
| **03** | **Schemas** | **Pydantic**: Enforcing strict input/output validation. (No broken JSON). |
| **04** | **Memory** | **Context Buffers**: Managing conversation history in stateful applications. |
| **05** | **Routing** | **Intent Classification**: Using logic to route user queries to the correct tool. |

---

## Phase 3: Agentic RAG (The Application)
*Goal: Building systems that can research, reason, and cite evidence.*

| Part | Topic | Engineering Pattern |
| :--- | :--- | :--- |
| **01** | **RAG Tool** | **Dynamic Retrieval**: Wrapping Vector Search into a callable Tool so the Agent decides *when* to search. |
| **02** | **Hybrid Agents** | **Multi-Tool Routing**: An agent that can dynamically switch between Math (Calculator) and Search (RAG). |
| **03** | **Citations** | **Grounding**: Injecting source metadata into the context to force evidence-based answers. |
| **04** | **Auto-Evals** | **LLM-as-a-Judge**: Building automated unit tests to grade the agent's accuracy and citations. |

---

## Phase 4: Orchestration (The Logic)
*Goal: Building complex, self-correcting workflows that can recover from failure.*

| Part | Topic | Engineering Pattern |
| :--- | :--- | :--- |
| **01** | **LangGraph** | **Cyclic Graphs**: Enabling loops and retries (e.g., "Try again if error"). |
| **02** | **Persistence** | **Checkpointing**: Saving the agent's state to a SQLite database so it can resume later. |
| **03** | **Human-in-Loop** | **Approval Flows**: Pausing execution for human review before sensitive actions. |  
| **04** | **Capstone 2** | **The Shift Orchestrator**: A semi-autonomous agent that extracts strict constraints and routes tasks to deterministic solvers (Supervisor Pattern). |

---

## Phase 5: Protocols & Standards (Specialist Track)
*Goal: Standardizing connections and enforcing reliability with strict contracts.*

| Part | Topic | Engineering Pattern |
| :--- | :--- | :--- |
| **01** | **MCP Architecture** | **Protocol Design**: Understanding the Client-Host-Server relationship (The "USB-C" for AI). |
| **02** | **FastMCP Servers** | **Server Implementation**: Building robust Python servers to expose local data resources standardly. |
| **03** | **Strict Contracts** | **Pydantic AI**: Implementing Type-Safe Agents that enforce strict I/O validation at the framework level. |
| **04** | **Observability** | **Logfire**: Implementing "X-Ray" vision to visualize agent reasoning, validation errors, and latency. |
| **05** | **Capstone 3** | **Health Ops System**: A modular ecosystem where a Pydantic AI Client (Agent) connects to a secure MCP Server (Data) to manage hospital operations. |

---

## Phase 6: Multi-Model Intelligence (The Architect Track)
*Goal: Achieving vendor agnosticism by implementing Model Routing.*

| Part | Topic | Engineering Pattern |
| :--- | :--- | :--- |
| **abstraction** | **The Model Factory** | **Dependency Injection**: A factory pattern to swap providers (OpenAI, Google, Anthropic) instantly. |
| **integrations** | **Cloud Connectivity** | **Vendor SDKs**: Implements connections for Google Vertex AI (Gemini 2.5) and AWS Bedrock (Claude 3.5). |
| **routing** | **The Semantic Router** | **Supervisor Pattern**: A Router Agent that classifies intent and dispatches tasks to the most cost-effective model. |

---

## Phase 7: Production Engineering (Scale)
*Goal: Moving from "It works on my machine" to deployed software.*

| Part | Topic | Engineering Pattern |
| :--- | :--- | :--- |
| **01** | **Advanced Evals** | **RAGAS Integration**: Implements algorithmic scoring (Faithfulness, Relevancy) to mathematically prove agent reliability. |
| **02** | **Semantic Caching** | **Vector Caching**: Reduces API costs by 50% by caching "meaning" (Question A = Question B) rather than exact text. |
| **03** | **Deployment** | **Docker**: Production-ready containerization. (See `Dockerfile` in root). |

---

### Tech Stack
* **Languages:** Python 3.12 (Strict Type Hinting)
* **Models:** GPT-4o, Gemini 2.5 Flash, Claude 3.5 Sonnet
* **Infrastructure:** ChromaDB, SQLite, Docker, AWS Bedrock, Google Vertex AI
* **Frameworks:**
    * **LangChain / LangGraph:** For orchestration and RAG chains.
    * **Pydantic AI:** For type-safe agent definitions.
    * **Logfire:** For observability and tracing.
    * **FastMCP:** For building standardized Model Context Protocol servers.
    * **RAGAS:** For automated evaluation and testing.