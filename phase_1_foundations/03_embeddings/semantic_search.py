# Module 3: Text Embeddings (Semantic Search)

**Phase 1 Status:** 📐 The Math Upgrade (3/5)

## 📖 The Story So Far
In Module 2, we gave the AI access to secret data, but our search logic was dumb. We were using `if "keyword" in string`. This meant that if a user asked for "Feline" but our document said "Cat," the system failed. Human language is too complex for simple keyword matching.

## 🚧 The Problem
**Keywords miss the Meaning.**
We need a way for the computer to understand that "Password", "Secret", and "Code" are all talking about the same thing, even if the letters are completely different.

## 🛠️ The Solution: Embeddings (Vectors)
We stopped comparing strings and started comparing **Concepts**.
An "Embedding" turns text into a list of numbers (a Vector). Ideally, the numbers for "Cat" and "Feline" will be mathematically close to each other.

**In this code (`semantic_search.py`):**
1.  We convert sentences into Vectors using OpenAI.
2.  We use **Cosine Similarity** to calculate the angle between them.
3.  We prove that "A feline is resting" is a 90% match for "The cat is on the mat," solving the synonym problem completely.