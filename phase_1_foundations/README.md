# Phase 1: AI Engineering Foundations (The Brain)

**Goal:** Build a system that can Read, Understand, and Remember.

## 🗺️ Phase Overview
In this phase, we move from interacting with raw Large Language Models (LLMs) to building a grounded, knowledge-aware system.

We follow a specific engineering progression:
1.  **Control:** First, we must learn to tame the LLM's unpredictable nature.
2.  **Memory:** Next, we give it access to private data it wasn't trained on.
3.  **Meaning:** Then, we upgrade that memory from simple "keywords" to "concepts."
4.  **Scale:** Finally, we build a dedicated database to hold that memory permanently.

---

## 📂 Module Breakdown

### Module 1: Prompt Patterns (Control)
* **The Problem:** LLMs are non-deterministic. If we ask the same question twice, we might get different answers or tones.
* **The Build:** We will implement **Few-Shot Prompting**.
* **The Lesson:** By providing examples of "Input -> Output" pairs in the prompt history, we constrain the model's behavior and tone without expensive fine-tuning.

### Module 2: Naive RAG (Memory)
* **The Problem:** LLMs have a "Knowledge Cutoff" and don't know our private data (passwords, internal docs).
* **The Build:** We will build a **Context Injection** pipeline. We will manually retrieve secret information and paste it into the system prompt.
* **The Limitation:** This module intentionally uses simple `if "keyword" in text` logic. We will see exactly why this fails when users use synonyms (e.g., searching for "cat" misses "feline").

### Module 3: Embeddings (Meaning)
* **The Problem:** Keyword search is brittle. It fails to capture intent.
* **The Build:** We will replace keyword matching with **Vector Embeddings**. We will convert text into mathematical vectors and use **Cosine Similarity** to measure the distance between concepts.
* **The Lesson:** This teaches the system that "Feline" and "Cat" are semantically identical, solving the limitation from Module 2.

### Module 4: Vector Database (Scale)
* **The Problem:** Calculating embeddings for every single query is slow and expensive. We cannot re-read our entire dataset every time a user asks a question.
* **The Build:** We will implement **ChromaDB**, a specialized database for vectors.
* **The Lesson:** This allows us to persist our embeddings to disk and perform ultra-fast Approximate Nearest Neighbor (ANN) searches, enabling our system to handle thousands of documents.

### Module 5: Capstone (Integration)
* **The Result:** We will combine all previous modules into a production-style architecture.
* **The Build:** A **Resume RAG Chatbot**.
    * **Ingestion Pipeline:** Reads a resume, chunks it, embeds it, and saves it to ChromaDB.
    * **Inference Pipeline:** Retrieves relevant chunks based on user questions and generates cited answers.

---

## ⏭️ Next phase 
Once we have completed the Capstone, we are ready for **Phase 2**, where we give the AI "Hands" to take action on the real world.