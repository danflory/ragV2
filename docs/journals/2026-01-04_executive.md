# Gravitas Grounded Research - Developer Journal
---
💡 **USER COMMAND**: If the volume of this log is too high, tell me: **"Gravitas, scale back logging"** or **"Gravitas, switch to Executive Only"**.
---


This document serves as a real-time log of the AI Assistant's reasoning, architectural decisions, and strategic options. It is designed to help the human lead understand the "Why" behind the "How," and to provide "Strategic Crossroads" for executive decision-making.

---

## [2026-01-04 19:48] - JOURNAL INITIALIZED
**Objective:** Create a persistent stream of thought for educational and strategic alignment.

### Current State
- **Rebranding:** Complete (v4.2.0-gravitas).
- **Cleanup:** Complete (Workspace reorganized).
- **Testing:** All core suites (Telemetry, Memory, Modes) are GREEN.

### Reasoning Strategy
My internal reasoning is now focused on **Operational Clarity**. By documenting decisions here, we create a "Paper Trail" that explains why we might choose a `sed` command over an LLM refactor, or why we hold back on renaming database users to preserve volume integrity.

### Strategic Crossroads
- **Entry Point:** Should we continue with the current CLI-heavy startup, or should we design a "Master Control" dashboard that handles service checks via the FastAPI backend?
- **Telemetry Policy:** Now that telemetry is stable, should we start logging "Thought Latency" to optimize L1/L2 selection?

---

## [2026-01-04 19:53] - PRIVACY & MAINTENANCE UPDATE
**Objective:** Secure the journal for local-only research and automate cleanup.

### Actions Taken
- **Git Hard-Lock:** Added `docs/GRAVITAS_DEV_JOURNAL*.md` to `.gitignore`. The journal is now **local-only**. This ensures that deep architectural critiques and secret brainstorming stay on the Titan RTX and never hit GitHub.
- **Maintenance Engine:** Created `scripts/maintenance.py`.
- **Reset Integration:** Hooked maintenance into `scripts/reset_gravitas.sh`. The system now automatically purges logs and dated journals older than **14 days**.

### Reasoning Strategy
The user intends to ingest these journals into the Gravitas RAG. By keeping them local-only, we can be much more "candid" in our logs without worrying about public repo footprints. The rotation/purge ensures the RAG isn't overwhelmed by 6-month-old "stale" thoughts while maintaining a high-fidelity 2-week "moving window" of context.

### Strategic Crossroads
- **Journal Rotation:** Should I start creating dated files (e.g., `GRAVITAS_DEV_JOURNAL_2026_01_04.md`) or keep appending to one large file and let the maintenance script truncate it? Dated files are better for RAG ingestion (fixed chunks of time).

---

## [2026-01-04 19:56] - DOCUMENTATION SYNC
**Objective:** Codify the Developer Journal into the system's official protocols.

### Actions Taken
- **Updated How-To:** Added Section 3 to `docs/HOWTO_DEV_REMINDERS.md` explaining the purpose and local-only nature of the journal.
- **Updated Protocols:** Added Section 5 to `docs/005_development_protocols.md` establishing "Reasoning & Transparency" as a core development standard.

### Reasoning Strategy
By embedding the journal into the official "How-To" and "Protocols," we ensure that this habit of "thinking out loud" becomes a permanent part of the Gravitas development lifecycle. It moves the journal from a "nice-to-have" feature to a "Standard Operating Procedure" (SOP).

### Strategic Crossroads
- **Journal Enforcement:** Should I automatically append my thoughts to the journal after every major command execution, or wait for logical "milestones"? Milestones keep the journal cleaner, but execution-level logging provides a better "forensic" trail for RAG ingestion.

---

## [2026-01-04 20:01] - STRATEGIC ALIGNMENT: NEXT STEPS
**Objective:** Acknowledge executive decisions on Command & Control and Intelligence Metrics.

### Actions Taken
- **Roadmap Updated:** Formally added **Phase 4 (Master Control Dashboard)** and **Phase 5 (Intelligence Optimization / Thought Latency)** to `docs/ROADMAP.md`.
- **Infrastructure Baseline:** The system is now locked in a "Ready" state for these upcoming features.

### Reasoning Strategy
The decision to prioritize the Master Control Dashboard is a high-impact UX choice. It moves Gravitas from a "Hacker's Rig" toward a "Managed System." Adding Thought Latency to the telemetry suite is the first step toward a **Self-Optimizing Neural Core**, where the system can eventually decide which model to use based on how fast the Titan RTX is currently responding compared to cloud APIs.

### Strategic Crossroads
- **Latency Source:** Should we measure total wall-clock time at the API Gateway (FastAPI router), or should we inject instrumentation directly into the L1/L2/L3 drivers to see exactly where the "lag" is occurring (Network vs. Inference)? Gateway is easier, Driver-level is much more precise for RAG ingestion analysis.

---

## [2026-01-04 20:06] - MASTER MANUAL RESTRUCTURING
**Objective:** Enhance visibility for humans and provide detail on system dashboards.

### Actions Taken
- **Manual Renamed:** `Gravitas_Grounded_Research.md` ➔ **`READ_ME_GRAVITAS_MASTER_MANUAL.md`**.
- **Dashboard Documentation:** Added Section 2 detailing the **Nexus Dashboard** (Web UI), **Monitor Dashboard** (CLI Metrics), and the upcoming **Master Control Dashboard** (Phase 4).
- **Architecture Sync:** Updated architecture diagrams and numbering for v4.2 consistency.

### Reasoning Strategy
Renaming the manual to include "**READ ME**" is a direct response to human cognitive patterns; we look for "magic words" when entering a new codebase. By documenting the upcoming Master Control Dashboard alongside the existing tools, we create a unified "Mission Control" mental model for the user.

### Strategic Crossroads
- **Dashboard Consolidation:** As we build the Master Control Dashboard, should we integrate the **Monitor** metrics (VRAM, Docker health) directly into the Web UI via SSE (Server-Sent Events), or keep the CLI monitor as a "low-level" fallback? Web is more modern, but CLI is "immortal" if the browser/JS engine hangs.

---

## [2026-01-04 20:13] - DUAL-JOURNAL STRATEGY ACTIVATED
**Objective:** Decouple high-level strategic milestones from granular execution data.

### Actions Taken
- **Executive Journal (This File):** Now strictly for milestones, strategic crossroads, and executive approvals.
- **Thought Log (`docs/GRAVITAS_THOUGHT_LOG.md`):** Created for "Stream of Consciousness" logging. It includes errors, manual corrections, and "Under the Hood" struggles.
- **Maintenance Engine:** Updated `scripts/maintenance.py` to auto-purge the Thought Log every 14 days.

### Reasoning Strategy
This dual-track approach provides the best of both worlds. You get a clean, human-readable summary here, while the Thought Log provides a "Forensic Trail" that shows exactly where I struggled (e.g., regex failures, service timeouts). This data is invaluable for model selection; if I'm struggling repeatedly on a task in the Thought Log, it's a signal to scale up to a larger model.

### Strategic Crossroads
- **Thought Log Detail:** How deep should I go? I currently log internal tool failures (like the gitignore edit failure just now). Should I also log "Drafting" thoughts before I execute a tool?

---

## [2026-01-04 20:12] - LATENCY INSTRUMENTATION DECISION
**Objective:** Finalize the approach for thought latency tracking.

### Actions Taken
- **Strategy Locked:** Executive decision to use **Driver-Level Instrumentation**.
- **Roadmap Updated:** Phase 5 now specifically outlines the injection of timing hooks into `app/L1_local.py`, `app/L2_network.py`, and `app/L3_google.py`.

### Reasoning Strategy
Choosing Driver-Level over Gateway-level is a commitment to precision. It allows us to distinguish between internal inference time (GPU latency) and external transportation time (Network lag). For a "Grounded Research" project, this distinction is critical for identifying exactly where the bottleneck occurs in a research cycle.

---

## [2026-01-04 20:15] - MISSION CONTROL CONSOLIDATION DECISION
**Objective:** Finalize the UX strategy for system health monitoring.

### Actions Taken
- **Strategy Locked:** Executive decision to **Integrate Monitor Metrics** (VRAM, Docker Health) directly into the Master Control Dashboard via **SSE (Server-Sent Events)**.
- **Roadmap Updated:** Phase 4 now explicitly requires real-time health streaming to the Web UI.

### Reasoning Strategy
Consolidating the CLI Monitor metrics into the Web UI is a major step toward a "Single Pane of Glass" management experience. While the CLI tool will remain as a low-level fallback, the primary interface for Gravitas will soon allow you to monitor hardware stress and container status without ever leaving the browser.

---

## [2026-01-04 20:20] - JOURNALING PROTOCOL FINALIZED
**Objective:** Codify the dual-journal system in the developer documentation.

### Actions Taken
- **How-To Update:** Updated `docs/HOWTO_DEV_REMINDERS.md` with detailed descriptions of the Executive Journal and Thought Log.
- **Control Interface:** Documented the "Magic Words" for human volume control.

### Reasoning Strategy
By formalizing the difference between "Executive" and "Thought" logs, we ensure that the RAG has a clean semantic path for high-level queries and a granular path for forensic debugging. This structure supports both human management and autonomous self-correction.

---

## [2026-01-04 20:40] - STRATEGIC PIVOT: KNOWLEDGE INDEXING
**Objective:** Evolve the RAG from "Simple Semantic Keys" to "Advanced Knowledge Indexes."

### Actions Taken
- **Roadmap Updated:** Formally added **Phase 6: Advanced Knowledge Indexing** to `docs/ROADMAP.md`.
- **Infrastructure Strategy:** Defined the requirement for hierarchical summarization and concept-aware chunking to move beyond simple 1000-char fixed windows.

### Reasoning Strategy
Our current system is "Grounded" but lacks deep structural understanding. By transitioning to a Knowledge Indexing model, we allow the LLM to understand parent-child relationships between concepts (e.g., how a specific log entry relates to a broader architectural decision). This reduces retrieval noise and increases the "Intelligence Density" of the context provided to L1/L2 layers.

---

## [2026-01-04 21:00] - CONCEPTUAL DESIGN: COMMUNITY COGNITIVE MESH
**Objective:** Transition from a "Single-User RAG" to a "Tiered Community Knowledge Architecture."

### Core Decisions
- **Conflict Resolution (The Synthesizer):** The system will NOT prioritize one layer over another by default. Instead, it will identify and present tensions (e.g., "Your personal journal reflects X, while the Minister's current teaching series suggests Y").
- **Ownership & Tenure:** Group owners (e.g., Church Staff) define the "Active Grounding Window" (e.g., 30 days) for shared documents. After this window, documents move from "Ambient Grounding" to "Deep Archive."
- **Permissions Model (SharePoint Scope, Gravitas Simplicity):** Targeted implementation of a robust group/membership system. Focus on "Clear Implementation" over the bloat of legacy enterprise systems.

### Philosophical Guardrails
- **Not a Legal System:** This is a consumer-facing product for "Thinking Enhancement." Retention and deletion are optimized for cognitive clarity, not forensic audit trails.
- **Multi-Tenant Grounding:** A single chat session can be grounded across multiple "Layers" (Personal Pouch, Group Circle, Sanctuary Feed, and the Commons).

### Reasoning Strategy
By treating grounding as a "Stack of Layers," we solve the problem of overwhelming the LLM with too much history while allowing institutional influence to co-exist with personal research. The "Synthesizer" logic transforms the LLM from a simple answer-engine into a dialectic partner that helps users navigate the space between their thoughts and their community's collective wisdom.

---

## [2026-01-04 21:10] - THE FOLDER-CENTRIC GOVERNANCE MODEL
**Objective:** Define the primary UI/UX unit for consumer-grade organization and policy control.

### Core Principles
- **Folders as Policy Containers:** A Folder is not just a directory for files; it is the entity where **Directives** (instructions) and **Tenure** (time limits) are defined.
- **The "Minimum Viable AI" Interface:** Reject the technical bloat of TypingMind. Normal users will not see "Temperature" or "Top-P." They will see "Folder Purpose" and "Active Memory Duration."
- **User-Driven Taxonomy:** The user (or Group Owner) manually creates the structure (e.g., /Sermons, /Programming, /Health). This human-centric organization provides the "Anchor" for all subsequent Librarian research.

### UX Specifications
1.  **Folder Directives:** Instead of complex system prompts, folders contain simple, high-level directives that shape how the "Synthesizer" behaves in that context.
2.  **Group Sync:** In a community setting, the "Sanctuary Feed" or "Group Circle" manifests as a shared folder appearing in the user's sidebar, with the tenure/retention logic pre-configured by the Owner.
3.  **Grounding Toggle:** Users can explicitly "mount" or "unmount" folders to a chat session, cleanly controlling what documents the LLM sees.

### Reasoning Strategy
By moving policy (time limits) and directives (instructions) into the Folder level, we align technical system management with natural human organization. This makes the power of a "Project-based LLM" accessible to non-technical users while maintaining the hierarchical complexity required for community grounding.

---

## [2026-01-04 21:15] - THE "EXPERT ORCHESTRATOR" SERVICE MODEL
**Objective:** Define the boundaries between Developer authority and User simplicity.

### The Value Proposition (The "Moat")
- **Curated Intelligence:** Unlike generic LLM apps that overwhelm users with sliders, Gravitas is a managed experience. The Developer (me) handles model selection (L1/L2/L3), prompt engineering, and configuration. 
- **The Customer Experience:** The user receives a high-performance system that "just works" for their context (Church, Programming, Health), with templates that have been hand-tuned for their results.

### UX Interaction Rules
1.  **Drag-and-Drop Ingestion:** Dragging a file into Gravitas is the universal signal for "Ingest into RAG." 
    - This triggers the Librarian to process the file (Summary + Vector + Blob).
    - The file immediately becomes subject to the **RAG Maintenance Rules** (Group-defined tenure/purge).
2.  **No "Under the Hood" Access:** API keys, model temperatures, and low-level prompt engineering are hidden from the consumer. They interact with "Folders" and "Missions," never "Hyperparameters."

### Reasoning Strategy
By positioning the Developer as the expert service provider, we solve the "Tool Fatigue" common in AI. The user doesn't want to be a Prompt Engineer; they want to think clearly. Gravitas provides the cognitive foundation, while the Developer ensures the engine is tuned to the specific frequency of the user's life.

---

## [2026-01-04 21:15] - DATA AUTONOMY: "DELETE MEANS DELETE"
**Objective:** Establish the principle of user control over their own cognitive history.

### Core Principle
- **Absolute Deletion:** In Gravitas, when a user selects "Delete" from the context menu, it represents an absolute command. The system will not maintain "Ghost Memories" in the active RAG research path for that user.
- **The "No Hidden Admin" Rule:** We reject the frustration of enterprise systems (e.g., Gemini) where deletions are merely "hidden" while admins retain control. If the user decides a thought or record is no longer valuable for their thinking process, it is purged.

### UX Features
1.  **Context Menu Actions:** Every chat and document will have explicit controls for:
    - **Move to Folder:** For organizing raw "Miscellaneous" thoughts into "Policy Containers."
    - **Rename:** For human-centric indexing.
    - **Delete:** The "Purge" trigger.

### Reasoning Strategy
By ensuring "Delete means Delete," we build trust with the consumer. The system is a tool for *their* thinking enhancement, not a surveillance or legal audit device. This clarity of purpose distinguishes Gravitas from corporate LLM offerings and aligns it with personal privacy and cognitive clarity.

---

## [2026-01-04 21:30] - RESEARCH-CENTRIC RETENTION & EXPORT
**Objective:** Finalize the "Research-First" data lifecycle and the "Output Path" for community sharing.

### Entity Model: Individual vs. Group
- **Simplicity Over Social Networking:** No "Friends Lists."
- **Individual User:** A single cognitive pouch. No membership management.
- **Group Entity:** A special type of "User" that supports members. This covers everything from a couple (Wife & I) to a full congregation. Groups own shared folders and set "Hold Times" for documents.

### The "Auto-Eviction" Research Loop
- **Default Retention:** 30 days for all external documents. 
- **The "Renewal" Click:** To keep the UI clean and the RAG high-fidelity, documents expire unless specifically "renewed." Clicking a document resets its 30-day timer. 
- **Non-Storage Philosophy:** Gravitas is explicitly NOT for long-term file storage. It is a research reactor. If you don't interact with a document, it is evicted to keep the "Truth Base" fresh and relevant.

### Exporting the Cognitive Value
- **Email Integration:** Research must be shareable. A "Send via Email" button will offer two scopes:
    1.  **Direct Message:** Export a specific insight or response.
    2.  **Session Transcript:** Export the entire grounded chat history.

### Reasoning Strategy
By enforcing a 30-day "Soft Expiration," we ensure the system never becomes a digital landfill. It forces the user (and the Librarian) to focus on the *current* research cycle. The "Send to Email" feature transitions Gravitas from a private thinking tool to a community communication tool, allowing insights to move from the digital mesh into real-world action.

---

## [2026-01-04 21:30] - IDENTITY & CONTEXT ABSTRACTION
**Objective:** Refine the "Group-as-User" model and cross-context functionality.

### The "Group-as-User" Abstraction
- **Unified Interface:** By treating a Group as a special instance of a User, we standardize the code for storage, search, and folders. A Group has the same "Pouch" capabilities as an Individual, but with shared access.
- **Context Switching:** Users (Owners) can seamlessly toggle between their **Personal Context** and their **Group Context(s)**. This determines which "Folder Stack" is active and which grounding layers the LLM is currently listening to.

### Output Communication (Email)
- **Sender Identity:** Email exports will default to the primary email of the Account Owner.
- **Service Integration:** The system acts as a research assistant, sending its findings back to the user's own inbox for further distribution or archival outside of the 30-day "Research Pulse."

### Reasoning Strategy
This abstraction simplifies the architecture significantly. Instead of building a complex "Social Graph," we build a robust "Context Switcher." This allows an Owner to wear multiple hats (Individual Researcher, Church Staff Member, Small Group Leader) within the same high-performance interface, while keeping their data silos clean and their export paths predictable.

---

## [2026-01-04 21:35] - THE "GREAT LIBRARY" TIER (PERMANENT KNOWLEDGE)
**Objective:** Incorporate long-term, non-expiring knowledge stores into the tiered grounding architecture.

### The "Infinite Heartbeat" Tier
- **The Great Library:** Beyond the 30-day "Research Pulse," Gravitas will support a "Permanent Knowledge" tier. This is for users who wish to ingest thousands of books or foundational texts that should **never** expire.
- **Offboarding the Local Machine:** Given the scale (thousands of books), this tier is envisioned as a cloud-hosted or centralized resource, rather than a local-only hardware burden.

### Implementation Strategy
- **A New Folder Type:** "Permanent Folders" (or "Libraries") will be distinct from "Research Folders." They will be exempt from the 30-day auto-eviction and will serve as the "High-Gravity" center of the cognitive mesh.
- **Expert Curated Indexes:** These permanent libraries will benefit most from our "Phase 6: Advanced Knowledge Indexing," as the Librarian can spend more "Night Shift" time building deep relationship maps between these thousands of volumes.

### Reasoning Strategy
By adding the "Great Library" tier, we move Gravitas from a "Current Thinking Assistant" to a **"Digital Cathedral of Wisdom."** We maintain the clean air of the 30-day Research Pulse for daily work, but provide a deep, permanent foundation of knowledge that the user can "summon" at any time. This fulfills the ultimate vision of a consumer product that scales from a small group chat to a life-long library.

---

## [2026-01-04 21:40] - THE "ETERNAL OUTBOX" ARCHIVAL MODEL
**Objective:** Replace destructive deletion with automated "External Archival" via Email.

### The Lifecycle Shift
- **Persistence vs. Performance:** Gravitas will no longer "delete" chats into the void. Instead of a hard purge after 30 days (or upon manual request), the system will trigger an **Automated Archival Export**.
- **Email as Long-Term Memory:** Gmail/Email becomes the user's permanent, searchable repository. This solves the "Trapped Lab" problem: research is never lost, it just moves out of the "High-Inference Research Zone" (Gravitas) into the "Long-Term Reference Zone" (Email).

### Technical Requirements
- **Naming as Semantic Key:** Archival email subjects will be precision-engineered by the Librarian. They will include the Date, the Folder/Mission, and a high-density keyword summary (e.g., "GRAVITAS ARCHIVE: [2026-01-04] [Theology] - The Synthesis of Grace and Choice").
- **Auto-Archive Trigger:** At the end of the 30-day "Heartbeat," the system automatically emails the full chat session to the Owner before clearing the local database/vector store.

### Reasoning Strategy
By offloading "Storage" to Email, we keep the Gravitas hardware (Titan RTX, local databases) slim and hyper-fast. We leverage the world's best search engine (Gmail/Outlook) for long-term discovery while ensuring the Gravitas "Neural Core" only focuses on the most active, relevant 30 days of thought. This elegantly balances the need for "Eternal Record" with the necessity of "Ephemeral Speed."

---

## [2026-01-04 21:45] - DIFFERENTIATED DATA LIFECYCLE: CHATS VS. DOCUMENTS
**Objective:** Fine-tune the retention logic to avoid metadata bloat and redundant storage.

### Data Expiration Matrix
- **Chat Sessions:**
    - **Duration:** 30-day "Heartbeat" (Reset on interaction).
    - **Expiration Action:** **Automated Export to Email.** We preserve the unique intellectual value created during the session.
- **Document Uploads:**
    - **Duration:** 30-day "Heartbeat" (Reset on "Renew" click).
    - **Expiration Action:** **Hard Purge (No Export).** Since the user is the source of the upload, Gravitas will not create redundant copies in their email. The RAG is a clean research environment, not a secondary backup service.

### Reasoning Strategy
This distinction reinforces Gravitas as a high-performance research engine. We treat **Conversational Intelligence** (the chat) as a disappearing asset that must be saved, while treating **Source Material** (the document) as a reusable context that can be re-ingested if needed but doesn't deserve a permanent "clutter footprint" in the user's secondary storage (Email). 

---

## [2026-01-04 21:50] - THE FREEMIUM STORAGE & SERVICE MODEL
**Objective:** Finalize the business and technical architecture for long-term document persistence.

### Internal Document Service (The "Vault")
- **Native Experience:** We will NOT rely on third-party cloud permissions (Dropbox/OneDrive/Google Drive). Gravitas will feature a native, "Google Docs-like" storage service.
- **Freemium Tiers:** 
    - **Standard Tier:** Free usage up to a specified storage ceiling (e.g., xxx MB). This supports the "Research Pulse" and basic small group usage.
    - **Premium Tier:** A paid subscription (e.g., 2TB) for power users, the "Great Library" (thousands of books), and long-term institutional archival.
- **Monetization Alignment:** This aligns Gravitas with the TypingMind business model, where the user pays for the infrastructure they consume.

### The Role of Email (Refined)
- **Convenience, Not Persistence:** Email remains the primary "Outbound Relay" for sharing insights and receiving session summaries in a familiar inbox. However, the **Source of Truth** for permanent files and the "Great Library" now resides in our internal Vault service.

### Reasoning Strategy
By bringing storage in-house, we eliminate the "Permission Friction" that kills user trust. We also create a sustainable business model that allows users to scale from lightweight personal research to massive permanent knowledge management without ever leaving the Gravitas ecosystem. This transforms the Librarian's role from a simple "Purge Engine" to a "Storage Manager" for the user's growing digital domain.

---

## [2026-01-04 21:55] - THE LIVE DOCUMENT: DIRECT COGNITIVE MANIPULATION
**Objective:** Transition the UI from "Chat Scrolling" to "Active Document Editing."

### The "Canvas" vs. "Chat" Paradigm
- **Document-as-Entity:** In Gravitas, a document (email draft, code file, book chapter) is not just a message in a stream. It is a "Live Document" living in the Vault.
- **Precision Editing:** The user can interact with the document using natural language commands without scrolling the history or losing their place.
    - *Commands:* "Change the salutation to...", "Add a thought about X after paragraph 3", "Refactor the error handling in this code file."
- **Persistent State:** Because we own the document store, the LLM treats the document as a "Grounding Anchor" that it is currently modifying, similar to how this AI assistant interacts with the local file system.

### UX Features
- **The Split-Pane View:** A future Nexus Dashboard requirement where the Chat lives on the left (Reflex/Reasoning) and the Live Document lives on the right (The Work). 
- **Non-Linear Interaction:** The LLM can "reach into" the document to perform surgeon-like edits rather than just re-pasting the whole text.

### Reasoning Strategy
This move distinguishes Gravitas from "Chat-only" RAGs. By treating the document as an active, mutable object in our own Vault, we enable a high-productivity workflow where the LLM becomes a co-author. This is the ultimate expression of "Grounded Research": the research isn't just *found*, it is *applied* directly to the product being built.

---

## [2026-01-04 22:00] - TRUST ARCHITECTURE: ISOLATION & FEDERATED SEARCH
**Objective:** Engineer "Zero-Leak" data privacy and manage the complexity of multi-store synthesis.

### The "Siloed Knowledge" Mandate
- **Physical Isolation:** To guarantee user trust, data isolation is enforced at the storage and indexing levels. 
    - **Per-User Indexes:** Knowledge indexes (Qdrant) and token stores are logically or physically partitioned. Data from a "Small Group" store NEVER leaks into a "Personal" store unless explicitly synthesized by the Librarian.
- **Data at Rest Security:** All Vault contents will be subject to industry-standard encryption protocols to ensure that "Grounded Research" remains private research.

### The New Librarian Complexity: Federated Search
- **Cross-Store Synthesis:** The Librarian must now perform **Parallel Federated Searches**. When a user asks a question, the Librarian must simultaneously probe:
    1.  The Personal Pouch (Isolates Store A).
    2.  The Group Circle (Isolated Store B).
    3.  The Sanctuary Feed (Isolated Store C).
- **The "Synthesizer" Challenge:** The burden moves to the Librarian to intelligently combine these disparate search results without violating the isolation boundaries. 

### Reasoning Strategy
This is the "Trust Moat." By building Gravitas with per-user/per-group siloed indexing, we move beyond the security failures of shared-context LLMs. The Librarian becomes a sophisticated "Federated Orchestrator" that brings relevant pieces of knowledge together only at the moment of inference. This provides the highest possible level of data security while maintaining the "Cognitive Mesh" experience.

---

## [2026-01-04 22:15] - FROM SINGLE AGENT TO "LIBRARIAN DEPARTMENT"
**Objective:** Decompose the Librarian's responsibilities into a multi-agent specialized workforce.

### The Librarian Department Roles
To manage the new complexity of "Cognitive Mesh" research, the Librarian is now redefined as a specialized department:

1.  **The Intake Clerk (Ingestion):** 
    - *Responsibility:* Watches for drag-and-drop events. Performs initial file summary (L1) and assigns "Mission/Folder" tags.
2.  **The Research Librarian (Federated Search):** 
    - *Responsibility:* Performs parallel, siloed probes across Personal, Group, and Public stores. Ensures no cross-leakage during discovery.
3.  **The Archivist (Lifecycle & Email):** 
    - *Responsibility:* Manages the 30-day "Heartbeat." Triggers the "Renewal" prompts and executes the "Eternal Outbox" (Emailing chats before purging).
4.  **The Synthesis Clerk (The Synthesizer):** 
    - *Responsibility:* Joins fragments from the Research Librarian and highlights tensions/contradictions between grounding layers for the LLM Brain.
5.  **The Vault Manager (Compliance & Security):** 
    - *Responsibility:* Enforces isolation, manages encryption at rest, and tracks freemium storage quotas.

### Reasoning Strategy
A single "Librarian" agent would become a bottleneck in a multi-tenant, federated environment. By creating a "Department" model, we allow for asynchronous, specialized processing. This ensures that a heavy ingestion task doesn't lag a real-time research search, and that security remains a dedicated, constant duty rather than a secondary function of a search script.
