# THE BRAIN VS. THE LIBRARY: COGNITIVE TIERS

> **Architectural Concept**: This document clarifies the distinction between **Memory** (Static Storage) and **Intelligence** (Active Processing), and how differnt models (L1/L2/L3) fit into the Gravitas Enterprise.

---

## 1. The Core Distinction
You asked: *"If vectors are intuition, what are the models?"*

Here is the distinction:
*   **Qdrant/Neo4j (Memory):** This is the **Library**. It contains the knowledge (Books, Maps, Facts). It is static; it does not "think."
*   **The Model (LLM):** This is the **Reader**. It enters the library, reads the books, and answers your question.

**The Crucial Insight:**
An empty brain (Gemini 3 Pro) without a library knows nothing about *your* data.
A massive library (Qdrant) without a brain cannot answer a question.
**Gravitas** is the combination: **Smart Brain + Organized Library.**

---

## 2. The Cognitive Hierarchy (IQ Levels)
Not all "Readers" are equal. In Gravitas Enterprise, we assign different models based on the difficulty of the task.

### **L1: The Clerk (Reflex)**
*   **Model:** Ollama / Llama 3 (Local, Fast, "Low IQ")
*   **Role:** The efficient desk clerk.
*   **Interaction with Memory:**
    *   Good at: "Fetch me the document titled 'Budget 2024'."
    *   Bad at: "Analyze the subtle economic implications of this budget."
*   **Use Case:** Quick retrieval, simple formatting, rigorous formatting (JSON).

### **L2: The Analyst (Reasoning)**
*   **Model:** DeepInfra / Qwen2.5-Coder (Cloud, "Mid IQ")
*   **Role:** The hard worker.
*   **Interaction with Memory:**
    *   Good at: "Read these 5 retrieved documents and summarize the key points."
    *   Bad at: "Invent a novel philosophical framework based on these documents."
*   **Use Case:** Coding, summarization, fact-checking.

### **L3: The Genius (Research)**
*   **Model:** Gemini 3 Pro / Claude 3.5 Sonnet (Elite, "High IQ")
*   **Role:** The visionary.
*   **Interaction with Memory:**
    *   Good at: "Synthesize these 50 disconncted facts from the Graph and write a compelling narrative about Grace for an INTJ."
    *   **The Difference:** The L3 model has the **"Intuition of Meaning."** It can see patterns in the Vector/Graph data that the L1 model misses.
*   **Use Case:** Strategic planning, complex writing (Author), architectural design.

---

## 3. The "Intuition" Nuance
You rightly noted a potential conflict: *If vectors are intuition, why do we need a smart model?*

*   **Vector Intuition:** The *mathematical* closeness of words. Qdrant knows "King" is close to "Queen" because of math.
*   **Model Intuition:** The *cognitive* understanding of context. Gemini knows "King" is close to "Queen," but it also understands the *implications* of monarchy, history, and power dynamics.

**The Workflow:**
1.  **Qdrant (Mathematical Intuition)** finds the *relevant text*.
2.  **Gemini (Cognitive Intuition)** reads that text and *understands the soul of it*.

---
*Drafted: 2026-01-06*
