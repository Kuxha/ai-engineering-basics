# Phase 1: AI Engineering Foundations (The Brain)

**Goal:** Build a system that can Read, Understand, and Remember.

## The Journey So Far
In this phase, we moved from interacting with raw Large Language Models (LLMs) to building a grounded, knowledge-aware system. We solved three fundamental problems of generic AI: **Tone**, **Amnesia**, and **Scale**.

## Module Breakdown

### Module 1: Prompt Patterns (Control)
* **The Problem:** LLMs are non-deterministic and unpredictable.
* **The Solution:** We implemented **Few-Shot Prompting**. By providing examples of "Input -> Output" pairs in the prompt history, we constrained the model's behavior and tone, making it reliable for business tasks.
* **Key Concept:** In-Context Learning.

### Module 2: Naive RAG (Memory)
* **The Problem:** LLMs do not know private data (e.g., passwords, internal docs) and have a knowledge cutoff.
* **The Solution:** We built a **Context Injection** pipeline. We manually retrieved secret information and pasted it into the system prompt, allowing the AI to answer questions about data it was never trained on.
* **Limitation:** It relied on simple keyword matching ("if password in text"), which fails on synonyms.

### Module 3: Embeddings (Meaning)
* **The Problem:** Keyword search is brittle. "Feline" does not match "Cat" using standard string comparison.
* **The Solution:** We used **Vector Embeddings**. We converted text into mathematical vectors and used **Cosine Similarity** to measure the distance between concepts. This allowed the system to understand that "Feline" and "Cat" are semantically identical.
* **Key Concept:** Semantic Search.

### Module 4: Vector Database (Scale)
* **The Problem:** Calculating embeddings for every query is slow and expensive. We needed a way to save "long-term memory."
* **The Solution:** We implemented **ChromaDB**, a specialized database for vectors. This allowed us to persist our embeddings to disk and perform ultra-fast Approximate Nearest Neighbor (ANN) searches, scaling our RAG system to handle larger datasets.

### Module 5: Capstone (Integration)
* **The Result:** We combined all previous modules into a production-style architecture.
* **The Build:** A Resume RAG Chatbot with a decoupled **Ingestion Pipeline** (ETL) and **Inference Pipeline** (Chat). It proves we can build a system that reads your documents and answers truthfully with citations.

---

## What's Next? (Phase 2)
Phase 1 gave our AI a **Brain** (Knowledge).
Phase 2 will give our AI **Hands** (Action).

We will move from *Reading* static data to *Acting* on dynamic systems using **Tool Use** and **Agents**.