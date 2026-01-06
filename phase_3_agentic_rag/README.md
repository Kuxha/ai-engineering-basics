# Phase 3: Agentic RAG (The Application)

**Goal:** We will transform a passive "Chatbot" into an active "Researcher" that can decide *when* to search, *how* to cite sources, and *if* its answers are correct.

---

## 📖 The "Why" (Context & Evolution)

To understand why we are building this, we must look at where we came from.

**Phase 1 (The Brain): Passive RAG**
In Phase 1, we learned **Context Injection**. The user asked a question, we blindly searched the database, and shoved the text into the prompt.
* *The Limitation:* It was inefficient. If the user said "Hello" or "What is 2+2?", we wasted money searching the database for policy documents. The AI had no choice.

**Phase 2 (The Hands): Deterministic Tools**
In Phase 2, we learned **Tool Use**. We gave the LLM a calculator and an API client. We taught it to trigger Python functions to perform actions.
* *The Limitation:* The AI could "do" things, but its "knowledge" was still frozen in 2023 (training data).

**Phase 3 (The Synthesis): Agentic RAG**
Now, we combine them. We treat **"Knowledge Retrieval"** not as a hard-coded step, but as a **Tool**.
We give the AI a "Search Tool" alongside its "Math Tool." We force it to make a decision:
* *User:* "What is the refund policy?" -> *AI:* "I need to use the Search Tool."
* *User:* "Calculate the refund." -> *AI:* "I need to use the Math Tool."



This is the foundation of modern AI Product Engineering: **Routing & Dynamic Retrieval.**

---

## 🗺️ The Progression

We will build this system in four distinct logical steps.

### [Day 11: The RAG Tool](./01_rag_tool)
**Concept:** "Search as a Function"
We will wrap our vector database code into a portable Python function (`search_knowledge_base`) and define it as a Tool schema.
* **Engineering Goal:** We will decouple the "Database" from the "Chat Loop." The AI will no longer be connected to the DB; it will merely know a function *exists* that it can call.

### [Day 12: The Hybrid Agent](./02_hybrid_agent)
**Concept:** "The Router"
We will introduce a second tool (a Calculator) to force the Agent into a decision-making role.
* **Engineering Goal:** We will implement the **Dispatcher Pattern**. We will watch the AI analyze the user's intent and dynamically route the request to the correct subsystem (Math vs. Reading).

### [Day 13: Citations & Evidence](./03_citations)
**Concept:** "Grounding"
We will solve the "Trust Me Bro" problem. We will modify our search tool to mechanically inject source names (`[Source: Policy #1]`) directly into the text stream.
* **Engineering Goal:** Hallucination prevention. By forcing the model to repeat the source tag in its final answer, we ensure the output is grounded in retrieved text, not the model's imagination.

### [Day 14: Automated Evals](./04_auto_evals)
**Concept:** "LLM-as-a-Judge"
We will recognize that manual testing does not scale. We will build a testing harness that uses a second, cheaper LLM to grade the Agent's accuracy.
* **Engineering Goal:** We will move from "Vibe Checking" to **Semantic Unit Testing**. We will write tests that check for *meaning* rather than *string equality*.

---

## 📂 Architecture Overview

This folder contains the complete evolution of the system:

    phase_3_agentic_rag/
    ├── 01_rag_tool/       # Basic: "Here is a search tool."
    ├── 02_hybrid_agent/   # Logic: "Choose between Math or Search."
    ├── 03_citations/      # Trust: "Prove your answer."
    └── 04_auto_evals/     # Quality: "Did I get it right?"

---

## 🧠 Key Engineering Patterns We Will Master

| Pattern | Description |
| :--- | :--- |
| **Dynamic Retrieval** | Giving the AI permission to search only when necessary, saving cost/latency compared to "Always-On RAG." |
| **The Keyhole Problem** | Solving the retrieval issue where `n_results=1` hides crucial context. We will optimize our chunking strategy to `n=3`. |
| **Context Injection** | Manually adding metadata (Source IDs) into the prompt string so the AI can "read" them as part of the document. |
| **Semantic Testing** | Using a cheap LLM (GPT-4o-mini) to unit-test a smart LLM's outputs, enabling CI/CD for AI. |

---

## ⏭️ What Comes Next?

By the end of this phase, we will have mastered the **Components** of a thinking system.
However, our code is still "Linear." It runs from A to B. If the Search fails, the Agent gives up.

In **Phase 4: Orchestration**, we will introduce **LangGraph**.
We will stop writing linear Python scripts (`if msg.tool_calls...`) and start building **State Machines** (Graphs). We will give our agent the ability to:
1.  **Loop:** Search again if the first search fails.
2.  **Persist:** Remember the conversation even if the server restarts.
3.  **Pause:** Wait for human approval before taking action.