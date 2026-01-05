# Module 1: Prompt Patterns (Few-Shot Learning)

**Phase 1 Status:** 🧠 Brain Calibration (1/5)

## 📖 The Story So Far
We are starting from zero. You have a powerful raw intelligence (GPT-4), but it’s unpredictable. If we ask it to "be professional," it might write a Shakespearean sonnet or a robotic legal notice. One cannot build a reliable business application on top of a random number generator.

## 🚧 The Problem
**Raw LLMs are Non-Deterministic.**
Without strict guidance, the model guesses the tone you want. In a production environment (like a Customer Support bot), inconsistent tone destroys user trust. You need a way to force the model to behave exactly the same way, every single time.

## 🛠️ The Solution: Few-Shot Prompting
We don't just *tell* the model what to do; we *show* it. By providing "Few-Shot Examples" (3 pairs of Input $\to$ Output), we force the model to recognize the pattern and complete it.

**In this code (`few_shot_sanitizer.py`):**
1.  **System Prompt:** We define the persona ("Corporate Assistant").
2.  **Delimiters:** We use `####` to separate our instructions from the user's messy input.
3.  **The Pattern:** We give 3 examples of turning "angry IT rant" into "polite status update." The model has no choice but to follow suit for the 4th input.