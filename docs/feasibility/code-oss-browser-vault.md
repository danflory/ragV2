# Feasibility Study: "Gravitas Grounded Research" Station (via code-server)

**Date:** 2026-01-08  
**Author:** Dan Flory + Antigravity  
**Scope:** Technical feasibility of a web-based "Grounded Research Station" for Gravitas members  
**Deployment Context:** Self-hosted for first 50 users  

---

## The Vision: Gravitas Grounded Research

We are **not** building a code editor. We are building a **Research Station for Thinkers**.
The goal is "Obsidian for the Web" — a powerful, split-pane, knowledge-management environment that lives in the browser.

### Key Requirements
1.  **Mode A: Rich Editor**
    *   Native `.md` file storage (non-negotiable).
    *   WYSIWYG-like experience (tables, bold/italic rendering, not just syntax).
    *   Rich footnotes support (superscript links).
2.  **Mode B: Research View (Code View)**
    *   **Multi-pane workflow:** Top-left (Research Paper 1), Top-right (Research Paper 2), Bottom (Drafting).
    *   **Explorer:** Full file tree navigation.
    *   **Splits:** Vertical and horizontal splits logic handled natively.

---

## Executive Summary

**Can we build this? YES.**

The best path is to use **code-server** (VS Code in browser) but **skinned and configured** to act as a Research Station.

*   **Why code-server?** It provides the world-class window management (splits, explorer) for free.
*   **Why NOT Monaco?** Building the "split pane" logic from scratch is wasted effort.
*   **The Bridge:** We will use VS Code Extensions to provide the "Rich Edit" (Mode A) experience within the code-server shell.

## Implementation Strategy: The "Research Station" Stack

We will deploy standard code-server, but use **Extensions** and **Settings Profiles** to transform it into two distinct modes.

### The Stack
*   **Core:** code-server (v4.x) running on Ubuntu.
*   **Interface:** Web Browser (Chrome/Edge/Firefox).
*   **Multi-Tenancy:** Each user gets their own sandboxed instance (Linux user separation).

### Satisfying Requirements

#### 1. Mode A: "Rich Editor" (The Writer's View)
*   **Solution:** Install **"Mark Sharp"** or **"Markdown Extended Pro"** extensions.
*   **Experience:**
    *   User opens a `.md` file.
    *   Instead of raw text, they see a Notion-like interface.
    *   **Toolbar:** Bold, Italic, Tables, Footnotes (superscript links).
    *   **Tables:** Native table editor (no more pipe `|` alignment hell).
*   **Files:** Still saved as pure, portable Markdown.

#### 2. Mode B: "Grounded Research" (The Thinker's View)
*   **Solution:** Native VS Code Window Management.
*   **Workflow:**
    *   **Left Pane:** File Explorer (Project/Vault Tree).
    *   **Main Area:** Split into 2x2 or 3+1 grid.
    *   **Content:**
        *   *Top Left:* PDF Viewer (Extension: `vscode-pdf`)
        *   *Top Right:* Browser Preview (Extension: `Simple Browser`) for web references.
        *   *Bottom:* Drafting in Markdown.
*   **Search:** "Search across all files" (grep) is native and lightning fast.

#### 3. Mode C: "Beach Mode" (E-Ink & Mobile)
*   **The Constraint:** e-ink screens on BOOX tablets are slow (low refresh), black & white, and hate animations. Phones have tiny screens.
*   **Solution:**
    *   **PWA Install:** Users must use Chrome/Edge on Android/iOS -> "Add to Home Screen". This removes the browser address bar and fixes the "app feel" issue.
    *   **Settings Profile:** We will create a specific `settings.json` profile for this mode.
    *   **Theme:** **"High Contrast Light"** (Critical for e-ink visibility).
    *   **Performance:**
        *   `"editor.cursorBlinking": "solid"` (stops constant refreshing).
        *   `"editor.smoothScrolling": false` (stops ghosting).
        *   `"workbench.list.smoothScrolling": false`.
        *   `"files.autoSave": "afterDelay"` (saves work even if connection drops).
    *   **Phone UI:** Use the "Zen Mode" toggle (Cmd+K Z) to hide all sidebars and focus purely on text.

---

## Roadmap to "Grounded Research"

### Phase 1: The Prototype (Days 1-2)
*   Spin up ONE instance of code-server on your current server.
*   Install "Mark Sharp" and "Markdown Extended Pro".
*   Configure the "Research Profile" (hide status bar, hide debug menu, clean UI).
*   **Goal:** You (Dan) verify if the writing experience feels "Grounded" enough.

### Phase 2: The Multi-User "Lobby" (Weeks 1-2)
*   Build the simple "Enter Vault" button in Gravitas Lobby.
*   Script the auto-creation of user folders.
*   Nginx routing to send `gravitas.ai/research/dan` to your implementation.

### Phase 3: "The Collective" (Month 1)
*   Shared folders (symlinks) allowing members to "read" each other's public work.
*   This enables the "Grounded Research" community aspect.

---

## Resource Verification (Re-Confirming)
*   **Current Hardware:** 48GB RAM, 16+ Cores.
*   **Requirement:** 5 Concurrent Users.
*   **Draft:** ~2GB RAM total for 5 users.
*   **Verdict:** **Massive Surplus.** You can run 50 users on this machine without sweating.

---

## Final Recommendation

**Proceed immediately with Phase 1 (Prototype).**
1.  Deploy code-server manually on port 8080.
2.  Install the "Rich Text" extensions.
3.  Test the "3-pane split" workflow with actual research papers.

**This is "Obsidian for the Web", but better because it's collaborative.**

