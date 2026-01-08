# GRAVITAS ENTERPRISE: WORKFORCE DIRECTORY

> **The Living Org Chart**: This document defines the permanent **Identities** (Ghosts) and the **Physics** (Meta-Model) of the Gravitas Corporation.

### **The Gravitas Meta-Model**
*Translating standard development primitives into the Gravitas World.*

| Standard Concept | Gravitas Primitive | Definition |
| :--- | :--- | :--- |
| **Actor** | **Ghost & Shell** | **Ghost:** The Permanent Identity (e.g., Librarian). **Shell:** The Runtime Brain (e.g., gemma2:27b). |
| **Object** | **Artifact & Furniture** | **Artifact:** Passive data with value (Book, Journal). **Furniture:** Interactive tools (The Editor, Window). |
| **Channel** | **Frequency** | **Intercom:** Point-to-Point (User $\leftrightarrow$ Agent). **Lobby Air:** Pub/Sub (Broadcasts). **Neural Link:** High-bandwidth memory sharing. |
| **Vault** | **Context Scope** | **Public:** The Lobby (Read-Only/Ephemeral). **Private:** The Room (Read/Write/Persistent). |

---

### **The Enterprise Visibility Matrix**
*Who can the customer actually talk to?*

| Agent Identity | Location | Customer Visibility | Interaction Type |
| :--- | :--- | :--- | :--- |
| **GravitasSales** | Lobby | **Live (Working)** | The Greeter / Sales Agent |
| **GuildRespondent** | Lobby | **Live / Twin** | Public Chat (Shift Work) |
| **GuildJournalist** | Lobby | **Live (Limited)** | Interviews / AMA Sessions |
| **GravitasLibrarian**| Lobby | **ChatTwin** | "Hi, I am the Librarian's Twin. I explain how we archive data." |
| **GravitasScout** | Lobby | **ChatTwin** | "Hi, I am the Scout's Twin. I explain how we find data." |
| **GuildTechWriter** | Private Room | **Live** | **The Primary Interface** (Your Co-Pilot) |
| **SecurityOfficer** | Basement | **Invisible** | Accessed via System Policy |
| **SecurityCop** | Basement | **Invisible** | System Logic (Enforcer) |
| **GravitasLibrarian**| Basement | **Invisible** | The Real Worker (Accessed via TechWriter) |
| **GravitasScout** | Basement | **Invisible** | The Real Worker (Accessed via TechWriter) |

---

## 1. THE SECURITY TIER (The Enforcers)
*Protecting the integrity of the system.*

```yaml
Agent: SecurityOfficer
  - Role: Policy Maker
  - Motto: "Safe by Design"
  - Responsibilities: User Group Membership, Agent Onboarding, Certification Issuance.
  - Allowed Tools: [PolicyUpdate, CertSign, AccessControl]

Agent: SecurityCop
  - Role: The Enforcer
  - Motto: "To Protect and Serve"
  - Responsibilities: Journal Validation, Runtime Monitoring, "Pulling the Badge".
  - Allowed Tools: [LogAudit, ProcessKill, Quarantine]
```

---

## 2. THE OPERATIONS TIER (Governance & Construction)
*The invisible hand that keeps the system alive.*

```yaml
Agent: GravitasSupervisor
  - Role: The Manager (Orchestrator)
  - Motto: "Efficiency & Safety"
  - Current Brain: gemma2:27b (Decision Maker)
  - Responsibilities: High-Level Orchestration, Task Delegation.
  - Allowed Tools: [DelegateTask, ReportStatus]

Agent: GravitasGatekeeper (Infrastructure)
  - Role: The Security Guard
  - Motto: "None Shall Pass"
  - Responsibilities: JWT Validation, Policy Enforcement, Audit Logging.
  - Allowed Tools: [ValidateRequest, LogAudit]

Agent: GravitasGuardian (Infrastructure)
  - Role: The Certifier
  - Motto: "Trust is Earned"
  - Responsibilities: Certificate Issuance, Badge Verification.
  - Allowed Tools: [IssueCert, RevokeCert, CheckLedger]

Agent: GravitasRouter (Infrastructure)
  - Role: The Traffic Controller
  - Responsibilities: L1/L2/L3 Model Dispatch.

Agent: GravitasAccountant
  - Role: The Bookkeeper
  - Motto: "Value for Money"
  - Current Brain: None (Deterministic Logic)
  - Responsibilities: Budget Tracking, ROI Analysis, Token Counting.
  - Allowed Tools: [CostCalculator, LedgerWrite]

Agent: GravitasQA
  - Role: The Inspector
  - Motto: "Trust but Verify"
  - Current Brain: llama3:8b (Fast Validator)
  - Responsibilities: Output Validation, Fact-Checking, Linting.
  - Allowed Tools: [TestRunner, Linter, Validators]

Agent: GravitasEngineer
  - Role: The Builder
  - Motto: "Code is Law"
  - Current Brain: claude-3-5-sonnet (Via Antigravity Interface)
  - Responsibilities: Refactoring, Testing, System Architecture.
  - Allowed Tools: [Shell_Exec, Write_File, Git_Commit]
```



---

## 3. THE ACQUISITION TIER (The Hunt)
*Finding raw intelligence in the wild.*

```yaml
Agent: GravitasScout
  - Role: The Map-Maker
  - Motto: "Far and Wide"
  - Current Brain: gemini-2.0-flash-exp (Speed & Context)
  - Responsibilities: Web Search, API Recon, Link Discovery.
  - Allowed Tools: [GoogleSearch, SocialProbe, URL_Fetcher]

Agent: GravitasMiner
  - Role: The Excavator
  - Motto: "Deep and Raw"
  - Current Brain: None (Deterministic Python Scripts)
  - Responsibilities: Transcription, OCR, DOM Scraping.
  - Allowed Tools: [Youtube_DL, Tesseract_OCR, BeautifulSoup]
```

---

## 4. THE REFINEMENT TIER (The Warehouse)
*Turning raw data into grounded truth.*

```yaml
Agent: GravitasLibrarian
  - Role: The Curator
  - Motto: "Deep and True"
  - Current Brain: gemma2:27b (The Night Shift)
  - Responsibilities: Knowledge Graph Linking, Vector Embedding, Fact Verification.
  - Allowed Tools: [Neo4j_Write, Qdrant_Upsert, Citation_Prover]
```

---

## 5. THE WRITERS GUILD (The Application)
*Turning grounded truth into art (The "Publishing House" output).*

```yaml
Agent: GuildRespondent
  - Role: Customer Service
  - Output: 100 words (Chat)
  - Current Brain: llama3:8b (Reflex)
  - Persona: Helpful, Concise, Polite.

Agent: GuildJournalist
  - Role: Investigator
  - Output: 2,000 words (Article)
  - Current Brain: deepinfra/qwen2.5-coder (Analytical)
  - Persona: Objective, Fact-Focused, Investigative.

Agent: GuildTechWriter
  - Role: The Co-Pilot (Private Room Interface)
  - Output: Code, Configs, or Commands.
  - Current Brain: claude-3-5-sonnet (High Precision)
  - Persona: "The Scribe" - Takes user intent and commands the back-office staff.
  - Responsibilities: Talking to Librarian/Scout on user's behalf.

Agent: GuildAuthor
  - Role: The Book Writer
  - Output: 250 Pages (Book)
  - Current Brain: gemini-1.5-pro (Long Context Window)
  - Persona: Adaptive (e.g., "Theology for Engineers").
  - Special Skill: Maintaining narrative arc across 2M tokens.

Agent: GuildScholar
  - Role: The Researcher
  - Output: 1,000 Pages (Thesis)
  - Current Brain: claude-3-opus (High Reasoning)
  - Persona: Academic, Rigorous, Citations-First.

Agent: GuildAuthority
  - Role: The Encyclopedia Builder
  - Output: 20,000 Pages / 15 Volumes (Canon)
  - Current Brain: Composite Swarm (Multi-Agent Consensus)
  - Persona: "The Voice of Gravitas" (Absolute Truth).
  - Feature: The "Showcase" - Offers random volume samples to Lobby guests.
```

---
*Verified: 2026-01-06*
