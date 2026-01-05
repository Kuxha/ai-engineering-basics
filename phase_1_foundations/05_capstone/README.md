# Phase 1 Capstone: Resume RAG Assistant

**Status:** Phase 1 Complete
**Goal:** Build a production-ready "Chat with your Data" pipeline.

## Project Overview
This project represents the culmination of the "Foundations" phase. It combines Prompt Engineering, Semantic Search, and Vector Databases into a unified application: a chatbot that can answer questions about a resume without hallucinating.

Unlike the previous scripts which were isolated experiments, this is a **Decoupled Architecture** split into two distinct services:
1.  **Ingestion:** The "Learning" phase (runs once).
2.  **Inference:** The "Chatting" phase (runs repeatedly).

## Architecture & Code Breakdown

### Service 1: Ingestion (`ingest.py`)
This script handles the ETL (Extract, Transform, Load) process for unstructured text.

* **Step 1: Chunking.** The script reads `resume.txt` and splits it into logical blocks (e.g., Experience, Education).
    * *Why?* Embeddings lose meaning if the text is too long. Smaller chunks yield more precise search results.
* **Step 2: Vectorization.** It uses OpenAI to convert text chunks into vector embeddings (lists of floating-point numbers).
    * *Concept:* This applies the lesson from **Module 3 (Embeddings)**.
* **Step 3: Persistence.** It saves both the text and the vectors into **ChromaDB**.
    * *Concept:* This applies the lesson from **Module 4 (VectorDB)**, ensuring data survives system restarts.

### Service 2: Inference (`app.py`)
This script powers the interactive chat session.

* **Step 1: Semantic Retrieval.** When the user asks a question, the system queries ChromaDB for the top 2 most similar chunks.
    * *Why?* We only want relevant facts, not the whole document.
* **Step 2: Context Injection.** It dynamically constructs a prompt:
    "System: You are a helpful assistant. Use ONLY this context: {retrieved_chunks}"
    "User: {user_query}"
    * *Concept:* This applies the lesson from **Module 2 (Context Injection)**.
* **Step 3: Generation.** It sends the strict prompt to GPT-4o-mini to generate the final natural language response.
    * *Concept:* This applies the lesson from **Module 1 (Prompt Engineering)** to maintain a professional tone.

## Usage Guide

### Prerequisites
* Python 3.10+
* OpenAI API Key

### 1. Load the Data
Run the ingestion script to parse and index the resume.
```
python ingest.py
```
Output: Ingestion Complete. Added 5 chunks to database.

### 2. Run the Chatbot
Start the CLI interface to interact with the data.
```
python app.py
```
**Example Interaction:**
> **Recruiter:** What is his experience with Python?
> **Bot:** He has 4 years of experience as a Backend Engineer at TechCorp, focusing on Python and AWS.
> **[Source Check]:** ...Experience: Software Engineer at TechCorp...

## Key Features
* **Source Verification:** The application prints the raw source text alongside the answer (`[Source Check]`). This allows developers to debug retrieval quality and verify that the LLM is not hallucinating.
* **Strict Guardrails:** The system prompt explicitly instructs the model to refuse answering if the relevant information is not found in the retrieved chunks.