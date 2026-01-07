# Phase 6: Multi-Model Intelligence (The Architect Track)

**Goal:** Achieve true Vendor Agnosticism. We will move beyond "OpenAI wrappers" to build a resilient, multi-model architecture that routes tasks between OpenAI, Google Vertex AI, and AWS Bedrock based on cost and complexity.
**Stack:** Python 3.12, Pydantic AI, Google Gemini 2.5 Flash, GPT-4o, AWS Bedrock (Claude).

---

## 1. How This Connects to the Journey

To understand the architecture, we must look at the evolution of our system:

* **Phase 1-4 (The Logic):** We built sophisticated reasoning chains, but they were "hard-coded" to a single provider. If OpenAI went down, our application died.
* **Phase 5 (The Protocol):** We standardized the **Tools** layer using MCP. The "Hands" became swappable.
* **Phase 6 (The Intelligence):** We now standardize the **Brain** layer. By implementing a **Model Factory** and **Semantic Router**, we decouple our business logic from the underlying intelligence provider.

**The Result:** A system where the "Body" (MCP) and the "Brain" (Model) are fully modular.

---

## 2. The Architecture: Router-Worker Pattern

We will implement a "Supervisor" architecture used by top AI labs.



### The Components

**01. The Model Factory (Abstraction Layer)**
We will build a dependency injection system that standardizes the interface for all models. Whether it is Claude, Gemini, or GPT, our agent sees a uniform `Model` object. This is the "USB-C" for our AI brains.

**02. The Semantic Router (The Supervisor)**
We will deploy **Google Gemini 2.5 Flash** as a high-speed, low-cost classifier. It analyzes user intent before any expensive compute is used:
* **High Complexity:** "Triage this patient based on symptoms." -> **Route to OpenAI (GPT-4o)**.
* **Low Complexity:** "Summarize this log file." -> **Route to Google (Gemini)**.

**03. The Worker (The Specialist)**
We will spawn transient agents at runtime. These workers receive the specific MCP tools they need to complete the task, execute it, and then terminate.

---

## 3. Module Breakdown

### Module 01: Abstraction
We implement the Factory Pattern to wrap `pydantic_ai.models`.
* **Key File:** `abstraction/model_factory.py`
* **Learning:** How to manage `AWS_DEFAULT_REGION` and `GOOGLE_APPLICATION_CREDENTIALS` in a unified configuration.

### Module 02: AWS Bedrock Integration
We implement the connection to Anthropic's Claude 3.5 Sonnet via AWS.
* **Key File:** `bedrock/claude_tester.py`
* **Status:** Technical implementation complete. (Note: Requires AWS Service Quota increase for production use).

### Module 03: Google Vertex AI Integration
We implement the connection to Gemini 2.5 Flash.
* **Key File:** `vertex/gemini_tester.py`
* **Learning:** Handling model versioning (`gemini-2.5-flash`) and region availability (`us-central1`).

### Module 04: Dynamic Routing
We build the autonomous dispatch system.
* **Key File:** `routing/routing_agent.py`
* **Logic:** The Router Agent evaluates the query complexity and dynamically instantiates the correct Worker Agent, injecting the Hospital MCP tools just-in-time.

---

## 4. How to Run

**1. validate Providers**
Before running the router, verify that your cloud credentials are active.

    # Test Google Vertex AI
    python phase_6_intelligence/vertex/gemini_tester.py

    # Test AWS Bedrock (If Quota Approved)
    python phase_6_intelligence/bedrock/claude_tester.py

**2. Run the Autonomous System**
This script will listen to your query, choose a model, and execute the hospital protocol.

    python phase_6_intelligence/routing/routing_agent.py

---

## 5. Key Engineering Learnings

1.  **Dependency Injection over Hardcoding:** By passing `model_name` as a variable, we reduced code duplication by 60%.
2.  **Latency vs. Intelligence:** We learned that for "Routing" tasks, speed matters more than reasoning depth. Gemini Flash (Sub-1s latency) allows the router to feel instant, while GPT-4o provides the deep reasoning needed for medical triage.
3.  **The "Version Churn" Reality:** Working with bleeding-edge libraries (`pydantic-ai`) requires checking attributes dynamically (e.g., handling `.data` vs `.output` changes).
4.  **Import Pathing:** We mastered Python's `sys.path` manipulation to allow deep modular imports without creating a packaged library.

---

**Next Step:**
With a robust, multi-model intelligence layer complete, we are ready for **Phase 7: Production Engineering**. We will package this entire ecosystem into **Docker containers** and deploy it to the cloud.