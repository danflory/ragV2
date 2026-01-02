# **Technical Architecture and Extensibility Report: Google Antigravity Agentic Development Platform**

## **1\. The Paradigm Shift: From Intelligent Editing to Agentic Orchestration**

The contemporary software engineering landscape is undergoing a fundamental transformation, transitioning from the era of "copilots"—which primarily offer intelligent autocomplete and localized suggestions—to the dawn of **Agentic Development Environments (ADEs)**. The Google Antigravity platform represents the vanguard of this shift, architected not merely as a text editor with Large Language Model (LLM) integration, but as a "Mission Control" center designed to orchestrate a workforce of autonomous, asynchronous agents.1 This distinction is critical for architects and platform engineers; whereas traditional Integrated Development Environments (IDEs) focus on the synchronous interaction between a human developer and their codebase, Antigravity introduces an intermediary layer of "agentic" labor capable of planning, executing, verifying, and iterating on complex engineering tasks with minimal human intervention.2

The architectural philosophy underpinning Antigravity is the concept of the "Agent-First" workflow. In this paradigm, the developer's role evolves from that of an individual contributor writing lines of code to that of an architect or engineering manager supervising digital workers. The platform's interface reflects this shift: upon launch, the user is greeted not by a file tree, but by the **Agent Manager**—a dashboard dedicated to spawning, monitoring, and orchestrating parallel agentic threads.4 This "Mission Control" interface allows for the delegation of high-level objectives—such as "refactor the authentication module" or "generate a test suite for the billing API"—which the system then decomposes into actionable steps.1

Crucially, this system operates on a "Stack-First" protocol, treating the technology stack not as a collection of static libraries but as a dynamic cognitive layer. The agents within Antigravity do not simply generate text; they produce verifiable "Artifacts"—structured deliverables such as implementation plans, diffs, and test reports that serve as the primary medium of communication between the human architect and the synthetic workforce.3 This artifact-based workflow addresses the "black box" problem inherent in many AI tools by providing transparent, audit-ready evidence of the agent's logic and execution path.5 Furthermore, the platform integrates a headless browser subagent, enabling agents to "step out" of the code environment to perform end-to-end testing, verify UI changes, and even conduct web-based research to resolve dependencies or errors.6

For developers seeking to integrate custom model architectures, understanding this high-level paradigm is a prerequisite. The system is designed around specific cognitive expectations—latency profiles, context window sizes, and reasoning capabilities—that are codified in its **3-Layer Cognitive Pipeline**.8 Any attempt to attach a custom model hierarchy must respect the intricate balance of this "Inference Economy," ensuring that the replacement components can fulfill the rigorous demands of the Orchestrator.8

## **2\. The 3-Layer Cognitive Pipeline: Anatomy of the System Brain**

The core intelligence of the Antigravity platform is not monolithic. Instead, it is distributed across a hierarchical **3-Layer Cognitive Pipeline**, a sophisticated routing system designed to optimize performance by balancing the competing constraints of speed, intelligence, and cost.8 This tiered architecture is the primary integration point for developers wishing to attach custom models, as the system explicitly routes tasks to "L1," "L2," or "L3" based on complexity and risk.

### **2.1 Layer 1 (L1): The Reflex Layer**

The foundational tier of the hierarchy is **L1**, designated as the **Reflex Layer**. This layer is architected for high-frequency, low-latency interactions that require immediate responsiveness but limited reasoning depth. It handles routine traffic, syntax corrections, and "Action Reflexes," such as generating shell commands or performing minor file edits.8

Infrastructure and Constraints:  
To ensure zero marginal cost and negligible latency, the L1 layer is designed to execute on local hardware. The reference specification utilizes an NVIDIA Titan RTX with 24GB of VRAM.8 This hardware allocation is critical; the system enforces a strict 4GB VRAM safety floor to prevent "Out-Of-Memory" (OOM) errors that could crash the containerized environment.8 The L1 driver, typically implemented via Ollama or direct HTTPX calls found in app/L1\_local.py, acts as the immediate interface between the Orchestrator and the local silicon.8  
Operational Logic:  
L1 operates under a "propose and verify" model. Because it prioritizes speed over deep reasoning, its outputs—particularly those involving shell commands or file system modifications—are treated as untrusted proposals. These proposals are immediately intercepted by the system's Gatekeeper protocol, which filters them against safety policies before execution.8 When attaching a custom model to the L1 slot (e.g., a fine-tuned Llama-3 8B or Mistral), developers must ensure the model is optimized for "instruction following" and can output structured commands (like JSON or diffs) that the Gatekeeper can parse.

### **2.2 Layer 2 (L2): The Reasoning Layer**

Above the reflex tier lies **L2**, the **Reasoning Layer**. This layer functions as the system's "Judge" and "Architect." It is invoked when the task complexity exceeds the capabilities of L1, or when a security threshold is breached—such as a code diff exceeding 50 lines or modifications to sensitive directories like core/.8

Infrastructure and Routing:  
L2 is typically offloaded to high-performance cloud models to leverage greater parameter counts without consuming local VRAM. The system specification references models like DeepSeek or Qwen (accessed via providers like DeepInfra) or Claude Sonnet 4.5.8 The L2 layer is characterized by its high "IQ" and ability to perform complex logic, architectural refactoring, and safety reviews.  
The Escalation Mechanism:  
One of the most critical mechanisms in the Antigravity architecture is the Dynamic Selection & Escalation logic. The Orchestrator automatically routes tasks from L1 to L2 based on specific triggers. For instance, if the Gatekeeper flags an L1-proposed action as ambiguous or potentially destructive, it triggers an asynchronous L2 Review. The L1 action is held in a pending state until the L2 model analyzes the context and issues a verdict—approving, rejecting, or modifying the plan.8 When integrating a custom L2 model, it is essential that the model be capable of "critique and refinement" workflows, acting as a supervisor to the faster L1 model.

### **2.3 Layer 3 (L3): The Deep Research Layer**

The apex of the cognitive hierarchy is **L3**, the **Deep Research Layer**. This "Agentic Flagship" is reserved for tasks requiring massive context windows, multi-step planning, and deep document synthesis. It is currently powered by frontier models like **Gemini 3 Pro** or **GPT-OSS**.8

Workflow and Capabilities:  
L3 operates on a different temporal scale than L1 or L2. It is designed for asynchronous, long-horizon tasks such as "analyze the entire codebase and propose a migration strategy." This layer engages in "Thinking" loops—iterative chains of thought—to synthesize information from the vector store, the file system, and external documentation.9  
The Omni-RAG Connection:  
L3 is tightly integrated with the system's "Omni-RAG" (Retrieval-Augmented Generation) infrastructure. It utilizes the hybrid search capabilities of Qdrant and MinIO to retrieve and process unstructured data (PDFs, images) alongside code.8 When configuring a custom L3 model, developers must ensure the model supports large context windows (often 100k+ tokens) to effectively utilize the retrieved data. The roadmap indicates that results from L3 are often summarized by L2 before being injected back into the active context, creating a cyclical flow of information between the layers.8

## **3\. Technical Integration: Attaching Custom Models**

The primary objective of this technical dump is to elucidate the mechanisms for attaching a custom three-level model hierarchy. Antigravity handles this through a robust **Inversion of Control (IoC)** architecture, centered on a dependency injection container. There are two primary pathways for integration: the **Configuration Path** (using proxies and JSON configs) and the **Architectural Path** (modifying the source code drivers).

### **3.1 The Inversion of Control (IoC) Container**

The linchpin of Antigravity's extensibility is the app/container.py module. This file functions as the **IoC Switchboard**, the central authority responsible for instantiating the specific driver implementations for L1, L2, and L3.8

Dependency Injection Flow:  
The system follows a strict initialization sequence:

1. **Config Loading:** The Config module loads environment variables and settings using **Pydantic** (app/config.py).  
2. **Container Initialization:** container.py reads these configurations and instantiates the appropriate LLMDriver classes for each layer.  
3. **Orchestration:** The initialized drivers are injected into the **Orchestrator** (app/orchestrator.py), which manages the RAG loop.  
4. **Routing:** The **Router** (app/router.py) delegates API requests to the Orchestrator, which uses the injected drivers to generate responses.8

To attach a custom model hierarchy natively, one must register new driver instances within container.py. This ensures that the Orchestrator receives the custom models transparently, without requiring changes to the core business logic.

### **3.2 The LLMDriver Interface Contract**

To maintain system stability and prevent "Split Brain" issues—where different components expect different behaviors from the models—Antigravity enforces a strict **Interface Contract**. Defined in app/interfaces.py, the LLMDriver abstract base class dictates the behavior of all model drivers.8

Required Implementation:  
Any custom driver must inherit from LLMDriver and implement the following asynchronous methods:

* **async def generate(self, prompt: str) \-\> str**: This is the core generation method. It abstracts the nuances of the underlying API (e.g., transforming a prompt into the specific JSON payload required by Ollama, OpenAI, or a custom endpoint) and returns a raw string response.  
* **async def check\_health(self) \-\> bool**: A diagnostic hook used by the system to verify connectivity. The container calls this method during startup to ensure the "Brain" is operational before accepting traffic.8

Implementation Strategy:  
When creating a custom driver (e.g., app/drivers/custom\_l3.py), developers should prioritize using httpx for network requests rather than heavy, vendor-specific SDKs. This reduces "SDK Bloat" and aligns with the system's preference for lightweight, async-native communication.8

### **3.3 The Configuration Path: providers.json and CLIProxyAPI**

For developers who prefer not to modify the internal Python source code, Antigravity supports a "Configuration Path" using external provider definitions and proxy servers. This approach is heavily referenced in community discussions regarding "Opencode" and "CLIProxyAPI" integrations.11

The providers.json Structure:  
The system (or its associated model manager extensions) looks for a configuration file, typically located at \~/.config/code-assistant-manager/providers.json. This file allows for the registration of custom endpoints that masquerade as supported providers.11  
**Table 1: providers.json Configuration Schema**

| Key | Description | Example Value |
| :---- | :---- | :---- |
| endpoint | The URL of the model server or proxy. | http://localhost:8317 |
| api\_key\_env | Environment variable holding the API key. | CUSTOM\_L3\_KEY |
| list\_models\_cmd | Command to retrieve the model list. | python \-m my\_module.list\_models |
| supported\_client | Clients that can access this provider. | claude,codex,antigravity |

Mechanism of Action:  
By configuring this file, developers can point the Antigravity IDE to a local proxy (like CLIProxyAPI) that standardizes the API surface. The proxy intercepts requests from the IDE and routes them to the user's custom L1, L2, or L3 models. This effectively "tricks" the IDE's Model Selector into displaying and utilizing the custom models as if they were native options.11

### **3.4 The Opencode Integration**

The "Opencode" CLI tool appears frequently in the research as a bridge for authentication and model management.13 It allows for the injection of custom authentication tokens and model definitions into the Antigravity environment. Plugins such as opencode-google-antigravity-auth enable the CLI to authenticate against Google's servers while managing local model quotas, effectively creating a hybrid authentication layer that supports custom model routing.14

## **4\. The Model Context Protocol (MCP): Bridging Agents and Data**

A critical component of the Antigravity ecosystem, often overlooked in basic setups, is the **Model Context Protocol (MCP)**. This standard allows the IDE to securely connect to local tools, databases, and external services, providing the agents with real-time context beyond the open files.15 For a custom three-level model hierarchy, MCP offers a way to expose specialized L3 capabilities (like a specific RAG pipeline) as a "tool" rather than just a chat model.

### **4.1 MCP Architecture and Configuration**

MCP operates on a client-host model where the IDE (Antigravity) acts as the host, connecting to various MCP servers. These servers can expose **Resources** (data) and **Tools** (executable functions).16

Configuration (mcp\_config.json):  
To register a custom MCP server, developers must modify the mcp\_config.json file, which can be accessed via the "Manage MCP Servers" option in the Agent Manager.15  
**Table 2: MCP Server Configuration Structure**

| Field | Type | Description |
| :---- | :---- | :---- |
| command | String | The executable to launch the server (e.g., npx, python). |
| args | List | Arguments for the command (e.g., script path, flags). |
| env | Object | Environment variables required by the server (API keys). |

**Example Configuration:**

JSON

{  
  "mcpServers": {  
    "my-custom-l3-tool": {  
      "command": "python",  
      "args": \["-m", "my\_custom\_rag\_server"\],  
      "env": {  
        "L3\_API\_KEY": "sk-..."  
      }  
    }  
  }  
}

This configuration allows the Antigravity Orchestrator to invoke the my-custom-l3-tool as part of its planning process, effectively integrating a custom L3 capability into the workflow without replacing the primary chat model.16

### **4.2 Use Cases for MCP**

* **Database Introspection:** Connecting an agent to a PostgreSQL schema via MCP allows L2 models to write accurate SQL queries by inspecting the live database structure.18  
* **Contextual Debugging:** MCP servers can fetch recent build logs or error traces from external systems (e.g., Sentry, Datadog), providing L3 models with the necessary context to diagnose complex failures.19  
* **Documentation Retrieval:** A "Context-7" MCP server can provide up-to-date documentation for specific tech stacks, ensuring the agents do not hallucinate deprecated APIs.20

## **5\. Hardware Infrastructure: The "Inference Economy"**

The feasibility of a local L1 model hinges on the system's hardware-aware architecture. Antigravity implements a sophisticated **Dual-GPU** strategy to maximize the "Inference Economy"—the ratio of intelligence to cost/latency.8

### **5.1 Dual-GPU Segmentation**

The reference specification outlines a strict division of labor between two GPUs to prevent resource contention between the generation of text (The Brain) and the retrieval of memories (The Embedder).8

**Table 3: Dual-GPU Hardware Allocation**

| Component | Hardware Target | Function | Model Examples |
| :---- | :---- | :---- | :---- |
| **L1 (Reflex)** | **GPU 0: NVIDIA Titan RTX** | Text Generation & Logic | gemma2:27b, Llama-3 |
| **Embedder** | **GPU 1: GTX 1060** | Vectorization & Reranking | bge-m3, nomic-embed-text |
| **Display** | **GPU 1: GTX 1060** | OS & UI Rendering | Windows Desktop Manager (DWM) |

**Technical Implications:**

* **Context Headroom:** By isolating the L1 model on the 24GB Titan RTX, the system reserves approximately **7GB of VRAM** specifically for context. This allows the L1 model to handle large prompts and file dumps without triggering swapping, which would catastrophically increase latency.8  
* **Parallel Processing:** Running the embedding service (ollama\_embed) on the secondary GPU ensures that the "RAG lookup" phase does not block the generation phase. In single-GPU systems, the GPU must unload the LLM layers to load the embedding model, causing a noticeable stutter. The Dual-GPU architecture eliminates this bottleneck.8

### **5.2 Docker Containerization and Passthrough**

To achieve the "Brain Transplant"—making the system portable across machines—Antigravity utilizes **Docker Desktop** with the **NVIDIA Container Toolkit**.8

* **Service Definition:** The docker-compose.yml file defines separate services for agy\_ollama (L1) and agy\_ollama\_embed (Embedder).  
* **Device Mapping:** Crucially, the configuration uses explicit device\_ids to map the physical GPUs to the respective containers (e.g., device\_ids: \['0'\] for L1). This ensures that the L1 model never accidentally claims the embedding GPU resources.8  
* **Network Topology:** The containers interact via a dedicated bridge network, ensuring low-latency communication between the "Brain" and the "Memory" (Vector Store).8

## **6\. Dependency Ecosystem and Stack Analysis**

A successful integration of custom models requires a deep understanding of the Python dependency stack defined in requirements.txt. These libraries form the nervous system of the platform, and version mismatches can lead to subtle failures in the cognitive pipeline.

### **6.1 Core Framework Dependencies**

* **FastAPI (\>=0.109.0):** This version requirement is significant. FastAPI 0.109.0 introduces critical updates to **Starlette** and Pydantic v2 compatibility, which are essential for the asynchronous WebSocket connections used by the Agent Manager.21 The high-performance nature of FastAPI is what allows the Router to handle multiple concurrent agent streams without blocking.23  
* **Uvicorn (\>=0.27.0):** As the ASGI server, Uvicorn manages the low-level connections. Version 0.27.0 includes important fixes for signal handling and graceful shutdowns, which are vital for ensuring that agent states are saved correctly when the IDE is closed.24

### **6.2 Data Validation and Settings**

* **Pydantic (\>=2.6.0):** The shift to Pydantic v2 is a major architectural detail. Pydantic v2 uses a Rust-based core (pydantic-core) for validation, offering a significant speedup.26 This is crucial for parsing the massive JSON payloads exchanged between the agents and the UI.  
* **Implication for Custom Config:** When modifying config.py to add custom model providers, developers must use the pydantic-settings library (a separate package in v2) and adhere to the new model\_config paradigms, such as SettingsConfigDict, rather than the deprecated class Config.27

### **6.3 LLM and Vector Drivers**

* **Google GenAI SDK (\>=0.2.0):** This driver interfaces with the L3 Gemini models. The version constraint 0.2.0 indicates the use of the unified client, which standardizes access to both Vertex AI and Gemini Developer APIs.28  
* **Ollama (\>=0.1.0):** The official Python client for Ollama allows for programmatically switching models and managing chat sessions. This library is the backbone of the L1 local driver.29  
* **ChromaDB (\>=0.4.24) & Qdrant (\>=1.7.0):** These libraries manage the semantic memory. The specific versions ensure compatibility with the embedding models used on the secondary GPU.31

## **7\. Operational Protocols: Security and Workflow**

Attaching a custom model is not just about connectivity; it is about safety. Antigravity implements rigorous protocols to prevent autonomous agents from causing damage to the local environment.

### **7.1 The Gatekeeper and Safety Loops**

The **Gatekeeper** (app/safety.py) is the security firewall of the system. It intercepts every action proposed by the L1 model before it touches the operating system.8

* **Static Analysis:** The Gatekeeper checks commands against a "Deny List" to block dangerous operations (e.g., rm \-rf /, formatting drives).33  
* **Heuristic Escalation:** If a proposed code change is too large (e.g., \>50 lines) or impacts core infrastructure, the Gatekeeper automatically triggers an escalation to the **L2 Reasoning Model**. L2 acts as a "Judge," reviewing the intent and safety of the proposal before permitting execution.8  
* **Implication for Custom Models:** When integrating a custom L1, developers must ensure the model is "aligned" or prompted to respect these boundaries. An overly aggressive L1 model might repeatedly trigger Gatekeeper escalations, stalling the workflow.

### **7.2 Workflow Customization**

Antigravity supports the definition of custom **Workflows**—structured sequences of prompts that guide agents through complex tasks.35

* **Global vs. Workspace Workflows:** Developers can define global workflows (available everywhere) or workspace-specific ones (e.g., "Generate Unit Tests" for a specific project).35  
* **Implementation:** Workflows are created via the Customizations panel and are essential for standardizing the behavior of the agents, ensuring that even custom models follow the team's engineering practices.4

## **8\. Community Patterns and "Vibe Coding"**

The emerging practice of "Vibe Coding"—where developers focus on high-level direction while AI handles the implementation—has driven much of the community exploration of Antigravity.36

* **Real-World Implementations:** Developers have successfully used the platform to build complex applications, such as full Snake games in Python 38 and Obsidian plugins 39, often by chaining multiple models (e.g., using Claude for coding and Gemini for planning).37  
* **Visual Verification:** A key pattern is the reliance on visual artifacts. The community emphasizes the value of the platform's ability to generate UI mockups and browser recordings, which allows for rapid visual verification of the agent's work without reading every line of code.2  
* **Custom Stacks:** Advanced users are leveraging the providers.json configuration to create "Custom Stacks," effectively bypassing the default model limits and injecting their own fine-tuned local models or diverse cloud providers into the loop.12

## **9\. Conclusion**

The Google Antigravity Agentic Development Platform represents a sophisticated convergence of hardware-aware infrastructure, hierarchical cognitive pipelines, and agentic orchestration. It is not merely a tool for writing code but a framework for managing cognitive labor. For the technical architect, the platform offers a rich surface for customization, primarily through its **IoC Container**, **LLMDriver Interface**, and **Model Context Protocol** integrations. By mastering these components—and adhering to the strict hardware and security protocols—developers can successfully attach and orchestrate a custom three-level model hierarchy, transforming Antigravity from a standard product into a bespoke engine for autonomous software engineering. This report serves as the foundational technical dump required to navigate and execute that integration.

#### **Works cited**

1. Getting Started with Google Antigravity, accessed January 1, 2026, [https://codelabs.developers.google.com/getting-started-google-antigravity](https://codelabs.developers.google.com/getting-started-google-antigravity)  
2. Build with Google Antigravity, our new agentic development platform, accessed January 1, 2026, [https://developers.googleblog.com/build-with-google-antigravity-our-new-agentic-development-platform/](https://developers.googleblog.com/build-with-google-antigravity-our-new-agentic-development-platform/)  
3. Introducing Google Antigravity, a New Era in AI-Assisted Software Development, accessed January 1, 2026, [https://antigravity.google/blog/introducing-google-antigravity](https://antigravity.google/blog/introducing-google-antigravity)  
4. Tutorial : Getting Started with Google Antigravity | by Romin Irani \- Medium, accessed January 1, 2026, [https://medium.com/google-cloud/tutorial-getting-started-with-google-antigravity-b5cc74c103c2](https://medium.com/google-cloud/tutorial-getting-started-with-google-antigravity-b5cc74c103c2)  
5. Google Antigravity vs Cursor vs Copilot: Enterprise Dev Tool Guide \- iTecs, accessed January 1, 2026, [https://itecsonline.com/post/google-antigravity-vs-cursor-vs-copilot](https://itecsonline.com/post/google-antigravity-vs-cursor-vs-copilot)  
6. Build End-to-End Cloud Solutions Using Agentic IDE | Google Antigravity Full Demo with Gemini3 \- YouTube, accessed January 1, 2026, [https://www.youtube.com/watch?v=mDLmPOhDM0s](https://www.youtube.com/watch?v=mDLmPOhDM0s)  
7. Google Antigravity: Agentic Development Platform Discussion \- YouTube, accessed January 1, 2026, [https://www.youtube.com/watch?v=zXxgj\_uES3o](https://www.youtube.com/watch?v=zXxgj_uES3o)  
8. AGY\_SYSTEM\_SPEC.md  
9. Models \- Google Antigravity Documentation, accessed January 1, 2026, [https://antigravity.google/docs/models](https://antigravity.google/docs/models)  
10. Google's New Gemini Pro Features Are Out, but Most of Them Will Cost You | Lifehacker, accessed January 1, 2026, [Google's New Gemini Pro Features Are Out, but Most of Them Will Cost You | Lifehacker](https://lifehacker.com/tech/google-new-gemini-3-features)  
11. How to Connect Code Assistants Like Claude Code to Google ..., accessed January 1, 2026, [How to Connect Code Assistants Like Claude Code to Google Antigravity Models : r/vibecoding](https://www.reddit.com/r/vibecoding/comments/1pwmwv2/how_to_connect_code_assistants_like_claude_code/)  
12. Antigravity and Local LLM : r/LocalLLaMA \- Reddit, accessed January 1, 2026, [Antigravity and Local LLM : r/LocalLLaMA](https://www.reddit.com/r/LocalLLaMA/comments/1p1flkr/antigravity_and_local_llm/)  
13. Antigravity (Google) auth plugin for opencode \- GitHub, accessed January 1, 2026, [https://github.com/shekohex/opencode-google-antigravity-auth](https://github.com/shekohex/opencode-google-antigravity-auth)  
14. NoeFabris/opencode-antigravity-auth \- GitHub, accessed January 1, 2026, [https://github.com/NoeFabris/opencode-antigravity-auth](https://github.com/NoeFabris/opencode-antigravity-auth)  
15. MCP Server \- Nuxt UI, accessed January 1, 2026, [https://ui.nuxt.com/docs/getting-started/ai/mcp](https://ui.nuxt.com/docs/getting-started/ai/mcp)  
16. Antigravity Editor: MCP Integration, accessed January 1, 2026, [https://antigravity.google/docs/mcp](https://antigravity.google/docs/mcp)  
17. Context7 MCP Server \-- Up-to-date code documentation for LLMs and AI code editors \- GitHub, accessed January 1, 2026, [https://github.com/upstash/context7](https://github.com/upstash/context7)  
18. Connect Google Antigravity IDE to Google's Data Cloud services | Google Cloud Blog, accessed January 1, 2026, [https://cloud.google.com/blog/products/data-analytics/connect-google-antigravity-ide-to-googles-data-cloud-services](https://cloud.google.com/blog/products/data-analytics/connect-google-antigravity-ide-to-googles-data-cloud-services)  
19. An Introduction to the Google Antigravity IDE | Better Stack Community, accessed January 1, 2026, [https://betterstack.com/community/guides/ai/antigravity-ai-ide/](https://betterstack.com/community/guides/ai/antigravity-ai-ide/)  
20. Google Antigravity: How to add custom MCP server to improve Vibe Coding \- Medium, accessed January 1, 2026, [https://medium.com/google-developer-experts/google-antigravity-custom-mcp-server-integration-to-improve-vibe-coding-f92ddbc1c22d](https://medium.com/google-developer-experts/google-antigravity-custom-mcp-server-integration-to-improve-vibe-coding-f92ddbc1c22d)  
21. fastapi · PyPI, accessed January 1, 2026, [https://pypi.org/project/fastapi/](https://pypi.org/project/fastapi/)  
22. Release Notes \- FastAPI \- Tiangolo.com, accessed January 1, 2026, [https://fastapi.tiangolo.com/release-notes/](https://fastapi.tiangolo.com/release-notes/)  
23. FastAPI documentation \- DevDocs, accessed January 1, 2026, [https://devdocs.io/fastapi/](https://devdocs.io/fastapi/)  
24. uvicorn \- PyPI, accessed January 1, 2026, [https://pypi.org/project/uvicorn/](https://pypi.org/project/uvicorn/)  
25. Different Uvicorn behavior with global class attributes for CLI vs. lib and base vs. reload / workers \#2189 \- GitHub, accessed January 1, 2026, [https://github.com/encode/uvicorn/discussions/2189](https://github.com/encode/uvicorn/discussions/2189)  
26. Welcome to Pydantic \- Pydantic Validation, accessed January 1, 2026, [https://docs.pydantic.dev/latest/](https://docs.pydantic.dev/latest/)  
27. Settings Management \- Pydantic Validation, accessed January 1, 2026, [https://docs.pydantic.dev/latest/concepts/pydantic\_settings/](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)  
28. google-generativeai \- PyPI, accessed January 1, 2026, [https://pypi.org/project/google-generativeai/](https://pypi.org/project/google-generativeai/)  
29. Ollama Python library \- GitHub, accessed January 1, 2026, [Ollama Python library](https://github.com/ollama/ollama-python)  
30. ollama \- PyPI, accessed January 1, 2026, [https://pypi.org/project/ollama/](https://pypi.org/project/ollama/)  
31. chroma-core/chroma: Open-source search and retrieval database for AI applications., accessed January 1, 2026, [https://github.com/chroma-core/chroma](https://github.com/chroma-core/chroma)  
32. Qdrant Python Client Documentation — Qdrant Client documentation, accessed January 1, 2026, [https://python-client.qdrant.tech/](https://python-client.qdrant.tech/)  
33. Google Antigravity Exfiltrates Data \- PromptArmor, accessed January 1, 2026, [https://www.promptarmor.com/resources/google-antigravity-exfiltrates-data](https://www.promptarmor.com/resources/google-antigravity-exfiltrates-data)  
34. Google Antigravity Setup Guide: Secure Enterprise Installation for Dev Teams \- iTecs, accessed January 1, 2026, [https://itecsonline.com/post/antigravity-setup-guide](https://itecsonline.com/post/antigravity-setup-guide)  
35. Rules / Workflows \- Google Antigravity Documentation, accessed January 1, 2026, [https://antigravity.google/docs/rules-workflows](https://antigravity.google/docs/rules-workflows)  
36. Is This The Future of Dev? Google Antigravity AI Code Editor with Gemini 3 Pro \- YouTube, accessed January 1, 2026, [https://www.youtube.com/watch?v=vChJfIb4hvU](https://www.youtube.com/watch?v=vChJfIb4hvU)  
37. Antigravity \+ Claude Code \+ Gemini 3 Pro \= Incredible : r/vibecoding \- Reddit, accessed January 1, 2026, [https://www.reddit.com/r/vibecoding/comments/1pihn0c/antigravity\_claude\_code\_gemini\_3\_pro\_incredible/](https://www.reddit.com/r/vibecoding/comments/1pihn0c/antigravity_claude_code_gemini_3_pro_incredible/)  
38. How to Set Up and Use Google Antigravity \- Codecademy, accessed January 1, 2026, [https://www.codecademy.com/article/how-to-set-up-and-use-google-antigravity](https://www.codecademy.com/article/how-to-set-up-and-use-google-antigravity)  
39. on building an Obsidian Related Notes plugin using Google's Antigravity IDE, accessed January 1, 2026, [https://darcynorman.net/2025/11/21/on-building-an-obsidian-related-notes-plugin-using-googles-antigravity-ide/](https://darcynorman.net/2025/11/21/on-building-an-obsidian-related-notes-plugin-using-googles-antigravity-ide/)