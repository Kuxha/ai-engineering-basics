# The AI Engineering Handbook 🛠️

**Goal:** A ground-up implementation of the modern AI Engineering stack, moving from basic prompting to autonomous MCP agents.
**Focus:** Reliability, System Design, and "Systems of Action" (not just Chatbots).

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

## 💎 Phase 5: Production & Evals (Seniority)
*Goal: Testing, Optimization, and Documentation.*

| Part | Topic | Engineering Pattern |
| :--- | :--- | :--- |
| **01** | **Evals** | **Unit Testing**: Deterministic grading of non-deterministic AI outputs. |
| **02** | **Optimization** | **Caching**: Reducing latency and cost for repeated queries. |
| **03** | **Interview** | **System Design**: Mock interview simulation and architecture defense. |

---

### 📚 Tech Stack
* **Languages:** Python (Strict Type Hinting)
* **Models:** GPT-4o-mini, text-embedding-3-small
* **Infrastructure:** ChromaDB, OpenAI SDK
* **Frameworks:** LangChain, LangGraph, Pydantic, FastMCP