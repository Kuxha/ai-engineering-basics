# Module 2: Naive RAG (Context Injection)

**Phase 1 Status:** 💉 Context Injection (2/5)

## 📖 The Story So Far
We taught the brain to be polite (Module 1). Now we need to teach it **secrets**. The AI doesn't know your password, your code, or your birthday because those aren't on the public internet.

## 🚧 The Problem
**The AI is frozen in time.**
You cannot "teach" the AI new things permanently without spending millions of dollars training it. We need a way to whisper secrets to it *just for this one conversation*.

## 🛠️ The Solution: Context Injection
We use a technique called **RAG (Retrieval Augmented Generation)**.
Think of it like an open-book exam.
1.  **Retrieve:** The code looks up the answer in a specific variable (`knowledge_base`).
2.  **Augment:** The code pastes that answer into the Prompt.
3.  **Generate:** The AI reads the prompt (with the answer inside) and tells the user.

**The Logic Flow:**
[Image of RAG Flow: User Query -> Python Script checks Keywords -> Python injects 'Secret' -> GPT-4 Answers]

## ⚠️ Why is it "Naive"?
This code uses **Keyword Matching** (`if "keyword" in string`).
* If you ask: "What is the code?" $\to$ **Success.**
* If you ask: "What is the password?" $\to$ **Failure.** (Because the word "password" isn't the word "code").
* *Solution:* In Module 3, we fix this with **Vectors**.