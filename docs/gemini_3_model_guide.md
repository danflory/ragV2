# Gemini 3: Flash vs Pro Capability Guide

**Status:** Current as of Jan 2026  
**Context:** Architectural Decision Support for Gravitas Grounded Research

---

## 1. Executive Summary
Google's Gemini 3 family includes two distinct models, Gemini 3 Flash and Gemini 3 Pro. Contrary to previous generations, the "smaller" model (Flash) is currently the superior choice for pure software engineering tasks, while the "larger" model (Pro) is specialized for deep reasoning and complex multimodal analysis.

This guide defines when to use which model within the Gravitas 3-Layer Cognitive Pipeline.

---

## 2. Executive Decision Matrix

| Feature | **Gemini 3 Flash** | **Gemini 3 Pro** | **Decision Rule** |
| :--- | :--- | :--- | :--- |
| **Primary Utility** | **High-Frequency Engineering** | **Deep Research & Architecture** | Use **Flash** for the loop; **Pro** for the plan. |
| **Key Advantage** | **Speed (3x faster)** & cost efficiency. | **Reasoning Depth** ("Deep Think"). | Use **Flash** when latency matters (e.g., chat). |
| **Coding Power** | **Superior (78% SWE-bench)**. | Strong (76.2% SWE-bench). | **Flash** is actually the better pure *coder*. |
| **Multimodal** | Multimedia summarization. | Pixel-precise, spatial analysis. | Use **Pro** for UI verification/screenshots. |
| **Cost** | ~$0.50 / 1M input tokens. | ~$2-4 / 1M input tokens. | **Flash** is ~5x cheaper. |

---

## 3. Detailed Capability Breakdown

### 3.1 Gemini 3 Flash: The "Software Engineer" (L2 Candidate)
*   **Best For:** Writing code, high-throughput log analysis, interactive chat, and acting as the "Judge" in your L2 layer.
*   **The Surprise:** Flash currently **outperforms** Pro on coding benchmarks (SWE-bench Verified: 78% vs 76.2%). It is optimized for the specific logic patterns of software engineering rather than general philosophical reasoning.
*   **Latency:** It is approximately **3x faster** than Gemini 2.5 Pro, making it ideal for "Vibe Coding" where you need near-instant feedback on small diffs.
*   **Gravitas Role:** It should be the default **L2 Reasoning Model**. It is smart enough to critique L1 but fast enough not to break flow.

### 3.2 Gemini 3 Pro: The "Principal Architect" (L3 Standard)
*   **Best For:** Massive context synthesis, novel problem solving, "Deep Thinking" loops (math/science/logic), and analyzing complex UI/Video artifacts.
*   **Differentiation:** Features a **"Deep Think"** mode that explores multiple hypotheses before outputting a plan. This makes it slower but far more reliable for "one-shot" architectural decisions.
*   **Multimodal Superiority:** If you are using the "Headless Browser" subagent to take screenshots of a web app and verify the CSS layout, **Pro** is required. Flash sees the image; Pro understands the *spatial relationships* and pixel alignments.
*   **Gravitas Role:** Remains the **L3 Deep Research** flagship. When you ask Antigravity to "analyze the entire codebase and refactor the auth system," Pro is the only model with the reasoning retention to handle that scope without getting lost.

---

## 4. Summary Recommendation

1.  **Switch to Gemini 3 Flash** for your daily driver, coding agents, and L2 "Reasoning" layer. The speed/cost benefit is massive, and it actually writes better code.
2.  **Invest in Gemini 3 Pro** solely for the **L3 layer** (Deep Research) or when specifically debugging visual UI issues where pixel-perfect understanding is required.
