# Phase 6: Multi-Model Intelligence (The Architect Track)

**Goal:** Break vendor lock-in. Build a "Model Agnostic" system that routes tasks to the best AI provider (OpenAI, Google, Anthropic) based on cost and complexity.
**Stack:** Python 3.12, Pydantic AI, Google Vertex AI (Gemini), OpenAI (GPT-4o).

---

## 1. The Architecture

We moved from a "Single Model" dependency to a **Router-Worker** architecture.



### The Components

* **The Factory (model_factory.py):** A centralized dependency injector. It standardizes the connection to different providers, ensuring the rest of the app doesn't care which model is running.
* **The Router (router_agent.py):** The "Supervisor." It uses a fast, cheap model (Gemini 2.5 Flash) to classify user intent.
* **The Worker:** A transient agent spawned at runtime. It receives the MCP tools and executes the actual business logic.

---

## 2. The Routing Logic

We implemented **Semantic Routing** to optimize for Cost vs. Intelligence:

| User Intent | Selected Provider | Why? |
| :--- | :--- | :--- |
| **Medical Triage / Booking** | **OpenAI (GPT-4o)** | Requires high reasoning and strict tool reliability. |
| **Summarization / General Info** | **Google (Gemini)** | Requires massive context window and speed; lower cost. |

---

## 3. How to Run

**1. Setup Credentials**
Ensure your .env contains keys for both providers:

    OPENAI_API_KEY=sk-...
    GCP_PROJECT_ID=your-project
    GOOGLE_APPLICATION_CREDENTIALS=/abs/path/to/key.json

**2. Run the Router**

    python phase_6_intelligence/01_routing/router_agent.py

**3. Verify Behavior**
* **Input:** "I have chest pain."
* **Result:** Router selects OPENAI.
* **Input:** "Summarize this list."
* **Result:** Router selects GOOGLE.

---

## 4. Key Engineering Learnings

* **Vendor Agnosticism:** By wrapping models in a factory, we can switch providers in 1 line of code.
* **Dependency Injection:** The Agent class in Pydantic AI is stateless; we inject the Model and Tools at runtime.
* **Error Handling:** We learned to handle 429 Throttling (AWS) and 404 Model Not Found (Google) by strictly defining region-specific model aliases.
* **Secret Management:** We learned that relative paths in .env files are dangerous. Always use absolute paths for service account keys.