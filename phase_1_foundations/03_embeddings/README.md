# Module 3: Text Embeddings (Semantic Search)

**Phase 1 Status:** 📐 The Math Upgrade (3/5)

## 📖 The Story So Far
In Module 2, we gave the AI secrets, but we used "Keyword Matching." If the user asked for "Feline" but the doc said "Cat," the system failed. We realized that simple string matching (`if "feline" in text`) is too dumb for human language.

## 🚧 The Problem: The "Synonym Gap"
Computers treat text as raw characters. To a computer, "Cat" and "Feline" are 100% different because they share no letters. We need a way to translate **Words** into **Meaning**.

## 🛠️ The Solution: Vectors & Cosine Similarity
We use an Embedding Model to turn text into lists of numbers (Vectors).

### How the "Black Box" Works
Imagine a giant map of concepts. The AI assigns coordinates to every word based on how it is used.
* **Cat:** `[0.01, 0.95, -0.3]`
* **Feline:** `[0.02, 0.94, -0.2]` (Very Close)
* **Banana:** `[0.85, -0.1, 0.5]` (Far Away)

**The Math (Cosine Similarity):**


[Image of Vector Space]

We calculate the angle between these vectors.
* Small Angle = High Similarity (Cat/Feline).
* Large Angle = Low Similarity (Cat/Banana).

**In this code:**
We send "A feline is resting" to OpenAI. It returns a vector. We compare that vector to our list of documents. The math proves that "feline" is mathematically close to "cat," allowing us to find the right document even without matching keywords.