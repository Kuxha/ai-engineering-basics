# Phase 7: Production Engineering (The Scale Track)

**Goal:** Move from "it works on my machine" to "it works everywhere." We focus on Reliability (Evals), Cost Efficiency (Caching), and Portability (Docker).
**Stack:** RAGAS, ChromaDB, Docker.

---

## 1. Advanced Evaluations (RAGAS)

We stopped judging agents by "vibes" and started judging them by math. Using **RAGAS** (Retrieval Augmented Generation Assessment), we implemented an automated unit test suite.

* **Faithfulness:** Measures if the answer is grounded in the retrieved documents (Anti-Hallucination).
* **Answer Relevancy:** Measures if the answer actually addresses the user's question.

**Key File:** `01_advanced_evals/ragas_eval.py`
**The Win:** We caught a "Silent Failure" where the bot was faithful but incomplete (missing Patient ID), scoring a `0.0`.

---

## 2. Semantic Caching

We implemented a **Vector Cache** to reduce API costs and latency. Instead of paying for every query, we check if a similar question has been asked before.

* **Logic:**
    1.  Embed User Query.
    2.  Check ChromaDB for questions with Cosine Similarity > 0.8.
    3.  **Hit:** Return cached answer instantly (0s latency, $0 cost).
    4.  **Miss:** Call expensive LLM, then save the result.

**Key File:** `02_caching/semantic_cache.py`
**The Win:** We proved that "Who is the heart doctor?" and "Who is the cardiologist?" trigger a cache hit, saving 50% of compute on repeat intent.

---

## 3. Containerization (Docker)

We packaged the entire Multi-Model / MCP ecosystem into a single Docker image.

**Dockerfile Strategy:**
1.  **Base:** `python:3.12-slim` for minimal footprint.
2.  **Context:** Built from Root to allow cross-phase imports.
3.  **Security:** Secrets are **not** baked in; they are injected via `-e` flags at runtime.

**How to Run:**
```bash
# Build
docker build -t hospital-agent:v1 .

# Run (Injecting Secrets)
docker run -it \
  -e OPENAI_API_KEY=sk-... \
  -e GCP_PROJECT_ID=... \
  -e GOOGLE_APPLICATION_CREDENTIALS=... \
  hospital-agent:v1
```