# Phase 2, Day 9: Memory (State Management)

**Goal:** Build a continuous chat session where the AI remembers previous context.

## The Engineering Concept
LLMs are **Stateless**.
* If you say "Hi" -> The server processes it and forgets it immediately.
* If you then say "My name is Bob" -> The server processes it and forgets it.
* If you then ask "What is my name?" -> The server has no idea.

**The Illusion of Memory:**
To create a "Chat," the **Developer** (You) must manage the state.
You store a list of messages (History). Every time the user speaks, you send:
`[System Prompt, Message 1, Reply 1, Message 2, Reply 2, ... Current Message]`

The LLM re-reads the *entire* script every single time to generate the next line.

## Code Overview
In `chat_memory.py`, we use a simple Python List: `conversation_history`.

1.  **System Role:** Sets the behavior ("You are Jarvis").
2.  **User Role:** The input from the terminal.
3.  **Assistant Role:** The output from the AI.

**Crucial Step:** We must `.append()` the AI's response back to the list. If we don't, the AI will answer the next question without knowing what it just said.

## Usage

### 1. Run the Chat
    python chat_memory.py

### 2. Test the Memory
Try this sequence:
    You: Hi, I am Laba.
    Jarvis: Hello Laba...
    You: What is 2 + 2?
    Jarvis: It is 4.
    You: What was my name again?
    Jarvis: Your name is Laba.

If it answers correctly, the Memory Loop is working.