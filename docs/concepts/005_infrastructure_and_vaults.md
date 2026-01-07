# THE BUILDING: LOBBY, ROOMS, AND VAULTS

> **Architectural Concept**: This document defines the **Spatial Layout** of the Gravitas Enterprise. It distinguishes between the Public Social Space (The Lobby) and the Private Work Space (The Rooms/Vaults).

---

## 1. The Lobby (The Public Square)
*The first touchpoint. A place of transparency and community.*

*   **Access:** Open to All (Guests, Members, Public Users).
*   **Vibe:** Social, Transparent, Educational.
*   **Function:**
    *   **Hangout:** Guests can chat with other users.
    *   **Meet the Staff:** "Gravitas Sales Reps" and other unassigned Agents wander here. You can interview them ("What is your job, Scout?").
    *   **Public Content:** Display cases showing "Free Books," "Sample Articles," and "System Stats."
*   **Constraint:** **NO PRIVATE WORK.** You cannot write a book here. You cannot save files here. It is for consumption and conversation only.

---

## 2. The Researcher Rooms (The Private Workbench)
*Where the Lobby Visitor becomes a Researcher.*

To enter, you must be assigned a **Vault Key** (Account).
Once inside, the UI transforms into a "VSCode-like" dense workspace.

### **The Desk (The Editor)**
*   **Center Stage:** The active document (Book, Article, Thesis).
*   **Tools:** Spellcheck, Citation Finder, Style Transfer.

### **The Staff Door (Agent Access)**
*   **Intercom:** You don't "go" to the Librarian; you summon them to your room.
*   **Tasking:** "Scout, bring me data on X." "Librarian, verify this paragraph."

---

## 3. The Context Scopes (Vaults)
*Where the treasures are kept.*

When a user gets a room, they are assigned a specific **slice** of the enterprise infrastructure. This defines their **Context Scope**.

*   **Public Scope (The Lobby):** Read-only, ephemeral, shared visibility.
*   **Private Scope (The Room):** Read/Write, persistent, private visibility.

### The Storage Containers
*   **The Bookshelf (Read Access):**

*   **The Bookshelf (Read Access):**
    *   Access to the **Global Library** (The vast Qdrant store of public knowledge).
    *   You can "rent" books (load them into your context).
*   **The File Cabinet (Write Access):**
    *   **Private MinIO Bucket:** Where you store your research notes, PDFs, and scraped data.
    *   **Private Graph Subgraph:** Your own connections and insights, separate from the global truth.
*   **The Work Table (Active Memory):**
    *   The specialized, high-speed RAM where your current project lives.

---

## 4. The Furniture & Objects (The Object Hierarchy)
*The tangible items the user interacts with.*

*   **The DoorKey (Identity):** The JWT Token. It grants access to the building and specific rooms.
*   **The Window (Context View):** The Market View. It lets you see "outside" to neighbor nodes (External Internet/News) without leaving your room.
*   **The Work Table (Active Editor):** The central Monaco Editor pane. This is Mutable State.
*   **The Bookshelf (Knowledge):** The Qdrant Connection. Immutable reference material.
*   **The ChatScreen (Communication):** The Interface to Agents. It is the "Staff Door" visualized.
*   **The Donation Bin (Public Intake):** A slot for users to submit documents to the Global Library.
    *   *Constraint:* Items are held in Quarantine until passing Legal/Copyright review by the Security Officer.

---

## 5. The Engine Room (The Basement)
*   **Invisible Infrastructure:** The Docker containers (Ollama, Postgres) that power the lights and the agents. The user never sees this, but they feel the heat of the GPUs working for them.

---
*Revised: 2026-01-06 (Social Lobby & Private Vaults)*
