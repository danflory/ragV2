# 001_CORE_ARCHITECTURE.md
# STATUS: ACTIVE
# DATE: 2025-12-30

## 1. THE DRIVER PATTERN (The "Hands")
The system connects to LLMs via **Drivers**. These are low-level adapters that translate our internal requests into vendor-specific API calls.

### 1.1 Interface Divergence
We currently support two distinct initialization patterns due to the nature of the connections.

#### Type A: The Local Driver (L1 - Titan RTX)
* **Target:** `LocalLlamaDriver` (Ollama/Titan)
* **Injection Pattern:** **Config Object Injection**
* **Signature:** `__init__(self, config: Settings)`
* **Reasoning:** Local drivers often need access to multiple hardware settings (URL, VRAM limits, timeouts, model paths) simultaneously. Passing the full config object reduces argument bloat.
* **Pros:** Easy to add new local settings without changing the signature.
* **Cons:** Tighter coupling between Driver and Config.

#### Type B: The Cloud Driver (L2 - DeepInfra)
* **Target:** `DeepInfraDriver`
* **Injection Pattern:** **Explicit Constructor Injection**
* **Signature:** `__init__(self, api_key: str, base_url: str, model: str)`

#### Type C: The Research Driver (L3 - Gemini 3 Pro)
* **Target:** `GeminiDriver` (Vertex AI / Google)
* **Role:** High-context synthesis and research.
* **Injection Pattern:** **Explicit Constructor Injection**

## 2. THE CONTAINER (The "Switchboard")
* **File:** `app/container.py`
* **Role:** **Inversion of Control (IoC) Root**.
* **Responsibility:** It bridges the gap between the divergent driver interfaces.
    * It knows *how* to construct L1 (passing `config`).
    * It knows *how* to construct L2 (extracting strings).
* **Rule:** The rest of the application (`router.py`) **MUST NEVER** instantiate a driver directly. It must always import `container`.

## 3. THE REFLEX SYSTEM (The "Nervous System")
* **Rule:** Actions are proposed by L1/L2 and validated.
* **Gatekeeper:** `app/safety.py` sits between the Router and the Reflex (`app/reflex.py`).
* **Flow:** L2 (Thought) -> XML Tag -> Router (Parse) -> Safety (Check) -> Reflex (Act).