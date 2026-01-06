Phase 3, Day 14: Automated Evals (LLM-as-a-Judge)

**Goal:** Build a testing system that automatically grades your Agent's accuracy without you needing to chat with it manually.

---

## 📂 What File Does What
* **`agent.py` (The Student):** The RAG system. It searches `knowledge.txt` and generates an answer.
* **`test_cases.json` (The Exam):** A list of questions ("Can I expense lunch?") and the matching truth ("No").
* **`eval_runner.py` (The Judge):** The test script. It runs the Agent, captures the output, and sends it to OpenAI to be graded.
* **`knowledge.txt` (The Textbook):** The raw policy data the agent uses to answer questions.

---

## 🔍 The Engineering Concept: "LLM-as-a-Judge"

In traditional software, we test code with strict equality:
`assert result == 5`

In AI Engineering, this breaks.
* **Expected Answer:** "No."
* **Agent Answer:** "Unfortunately, I cannot do that."
* **Code Result:** `FAIL` (Strings do not match).

To fix this, we use a second LLM call to act as the **Judge**. We ask the Judge: *"Does 'Unfortunately, I cannot do that' mean the same thing as 'No'?"*
The Judge says **YES**, and the test **PASSES**.

---

## 🧠 Deep Dive: The Evaluation Flow

How exactly does the script decide if the agent is "Right"?

### The Flowchart
1.  **The Input:** We pull a question from `test_cases.json`. ("Can I expense lunch?")
2.  **The Agent:** We run the agent. It retrieves context and answers. ("No, only for clients.")
3.  **The Package:** We bundle the **Agent's Answer** + the **Expected Fact**.
4.  **The Tribunal:** We send this bundle to a *different* LLM instance (The Judge).
5.  **The Verdict:** The Judge compares the *meaning* and returns "YES" or "NO".



### 💡 Why not use Embeddings? (The "Not" Problem)
A common question is: *"Why not just compare the embeddings of the Answer and the Fact? It's faster!"*

**The Reason:** Embeddings struggle with **Negation**.
* *Fact:* "You can **NOT** work on Fridays."
* *Hallucination:* "You **CAN** work on Fridays."

These two sentences have **High Cosine Similarity** (they share almost all the same words). An embedding test would say they are the same and **PASS** the hallucination.
An LLM Judge reads the word "NOT" and correctly marks it as **FAIL**.

---

## 🚀 Usage

### 1. Run the Evaluator
    python eval_runner.py

### 2. The Output
You will see a report card for your agent:

    Testing: 'Can I expense my lunch?'
    PASS

    Testing: 'How much PTO do I have?'
    PASS

    Total Score: 3/3

### 3. Analogy: The Professor and the TA
Think of your Agent as a **Student** taking an exam.
Think of the `test_cases.json` as the **Answer Key**.

* **You (The Engineer):** You are the Professor. You are too busy to grade every single quiz paper yourself.
* **The Judge (GPT-4o-mini):** You hire a Teaching Assistant (TA).

You give the TA the **Student's Answer** and the **Answer Key**.
You say: *"I don't care if the words are exactly the same. Just tell me if the student got the concept right."*