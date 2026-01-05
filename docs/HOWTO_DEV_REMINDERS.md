## Updated Content

# Gravitas Developer Reminders & How-To Guide

This document serves as a quick-reference for frequent developer workflows and operational shortcuts.

---

## 1. Updating Context for External AI (Gemini / OpenAI)

When you need to brainstorm high-level architecture or strategy in an external chat window that doesn't have direct codebase access, use the following workflow to ensure the AI has the latest "Source of Truth."

### The Workflow:
1.  **Open Terminal**: Ensure you are in your WSL/Ubuntu terminal.
2.  **Run Command**: Type the following alias:
    ```bash
    UpdateContext
    ```
3.  **Automatic Explorer**: A Windows Explorer window will automatically pop up, already navigated to the `D:\D\AntiGravityNexusContext\Text` directory.
4.  **Transfer**:
    -   Locate **`Initial Context Prompt.md`** (marked with a ⭐ in the terminal output).
    -   Open it and **copy/paste** its content into the chat as your **very first message**.
    -   Once the AI acknowledges, select **all other documents** in the Explorer window and **drag and drop** them into the chat interface.
5.  **Initialization**: The `Initial Context Prompt.md` automatically tells the AI to use the attached files as the "Source of Truth" and outlines the specific architecture (Dual-GPU, Phase 18, etc.).

---

## 2. Shared Aliases Summary

| Command | Action |
| :--- | :--- |
| `UpdateContext` | Refreshes external context files and opens Explorer. |
| `winE` | Opens Windows Explorer in the current WSL directory. |
| `reload` | Sources `~/.bashrc` to apply new configuration changes. |
| `py` | Jumps to project root and activates the Python virtual environment. |
| `Gravitas` | Launches the Antigravity editor for the current directory. |