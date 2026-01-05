# Module 4: Vector Database (ChromaDB)

**Phase 1 Status:** 💾 Long-Term Memory (4/5)

## 📖 The Story So Far
In Module 3, we successfully used Vectors to match "Feline" to "Cat." But we calculated those vectors from scratch every time the script ran. This is slow and expensive. If we had 10,000 documents, we would be paying OpenAI to re-read them every time you pressed "Enter."

## 🚧 The Problem: Scale & Amnesia
1.  **Speed:** Calculating math for 1 million documents takes too long.
2.  **Cost:** Re-embedding the same text over and over wastes money.
3.  **Amnesia:** Python variables disappear when the script stops. We need to save this data.

## 🛠️ The Solution: ChromaDB
We use a **Vector Database**. Think of it as a specialized "Excel Sheet" for numbers, but optimized for 3D navigation.

### Why ChromaDB?
* **It's Local:** It runs on your machine, not in the cloud. Perfect for privacy.
* **It's Persistent:** It saves data to the `./chroma_db_data` folder. You can restart your computer, and the AI will still remember what it learned.
* **It's Fast:** Instead of comparing your query to *every* document (Brute Force), it uses an index (HNSW) to jump straight to the relevant "neighborhood" of data.

**In this code:**
We ingest our documents once. ChromaDB turns them into vectors and saves them to your hard drive. When you query it, Chroma finds the "nearest neighbor" in milliseconds.