# THE LOBBY AND THE WORKBENCH: USER EXPERIENCE

> **Architectural Concept**: This document distinguishes between the **Admin Infrastructure** (The Engineers) and the **Customer Experience** (The Users). It outlines the vision for a "Knowledge IDE."

---

## 1. The Tale of Two Interfaces
You identified a critical distinction: *"The Dashboard today is the engineer's workbench."*

### **The Nexus Dashboard (Current)**
*   **Role:** Monitoring Station.
*   **User:** The System Administrator (You).
*   **Function:** Checking VRAM, restarting containers, debugging costs.
*   **Metaphor:** The Server Room Console.

### **The Gravitas Client (Future)**
*   **Role:** Knowledge IDE.
*   **User:** The Researcher / The Customer.
*   **Function:** Creating, interviewing, writing.
*   **Metaphor:** "VSCode for Thought."

---

## 2. The Customer Journey
### **Stage 1: The Lobby (The Open Air)**
*   **Access:** Untruncated / Public.
*   **Experience:** "Transparency as a Service."
*   **Feature:** **The Fishbowl.**
    *   **Meet the Staff:** "Gravitas Sales Reps" and other unassigned Agents wander here. You can interview them ("What is your job, Scout?").
    *   **The Showcase:** Agents (Librarian, Authority) proactively offer "Samples" of their work.
        *   "Sales told me to show you this 20-page excerpt on Grace."
        *   "Here is a random volume from the 20,000-page Encyclopedia we just finished."
    *   **Value:** Trust. The customer sees the "employees" are real, working tools, not just a black box.

### **Stage 2: The Researcher (The Private Vault)**
*   **Access:** Authenticated (Account Created).
*   **Experience:** "Ownership."
*   **Feature:** **The Personal Vault.**
    *   A dedicated namespace in Qdrant/MinIO.
    *   Users upload *their* documents (File Cabinets).
    *   Users rent *our* books (The Library).

---

## 3. The UI Vision: "an IDE for Knowledge"
You described a "dense UI layout like VSCode." This is technically feasible and highly valuable.

**The Layout:**
1.  **Left Sidebar (Explorer):**
    *   *The "Cabinet":* User's uploaded files.
    *   *The "Library":* Rented/Available external resources.
2.  **Center Pane (The Workbench):**
    *   *Active Documents:* The text being written (The Book, The Article).
    *   *Tabs:* Multiple drafts open at once.
3.  **Right Pane (The Staff):**
    *   *Chat:* "Librarian, find me a quote for this paragraph."
    *   *Tools:* "Scout, go find the citation for this."
4.  **Bottom Pane (The Terminal):**
    *   *Logs:* "Scout searching google.com...", "Librarian linking graph..." (Transparency).

---

## 4. Feasibility Analysis: "Is this a pipe dream?"
**Verdict: NO.**

It is ambitious, but it is **Architecturally Sound**.
*   **Backend:** We already have the APIs. The "Agents" are just Python classes that return text.
*   **Frontend:** "VSCode in a Browser" is a solved problem (Monaco Editor, React Mosaic).
*   **Scale:** The "Vault" concept is just multi-tenancy (Tenant ID in Qdrant).

**MVP Path:**
1.  Keep Nexus Dashboard for Admin (Port 5050).
2.  Build "Gravitas Lite" (Port 3000) with just Chat + 1 Text Editor pane.
3.  Add "Explorer" (File Upload) later.
