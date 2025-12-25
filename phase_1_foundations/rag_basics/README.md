# Pattern: Naive RAG (Keyword Retrieval)



## The Problem
Large Language Models (LLMs) have two major limitations:
1.  **Knowledge Cutoff:** They don't know events that happened after their training data.
2.  **Privacy:** They don't know your internal company data (e.g., passwords, private docs).

## The Solution
Implemented a **Naive Retrieval-Augmented Generation (RAG)** system.
Instead of fine-tuning the model (expensive), we "inject" the relevant data into the prompt at runtime.

### Architecture Flow
```mermaid
graph LR
    A[User Query] --> B{Contains Keyword?}
    B -- Yes --> C[Retrieve Secret]
    B -- No --> D[Retrieve Nothing]
    C --> E[Inject into System Prompt]
    E --> F[LLM Generates Answer]