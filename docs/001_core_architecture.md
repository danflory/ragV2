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
* **Reasoning:** Cloud drivers are "dumb pipes." They only need authentication and a target.
* **Pros:** Loose coupling. The driver can be used in other projects easily; it knows nothing about our `Settings` class.
* **Cons:** Signature must change if we add new required parameters.

## 2. THE CONTAINER (The "Switchboard")
* **File:** `app/container.py`
* **Role:** **Inversion of Control (IoC) Root**.
* **Responsibility:** It bridges the gap between the divergent driver interfaces.
    * It knows *how* to construct L1 (passing `config`).
    * It knows *how* to construct L2 (extracting strings).
* **Rule:** The rest of the application (`router.py`) **MUST NEVER** instantiate a driver directly. It must always import `container`.

## 3. THE REFLEX SYSTEM (The "Nervous System")
* **Rule:** L2 is the *only* entity allowed to request side-effects (File Writes/Shell).
* **Gatekeeper:** `app/safety.py` sits between the Router and the Reflex (`app/reflex.py`).
* **Flow:** L2 (Thought) -> XML Tag -> Router (Parse) -> Safety (Check) -> Reflex (Act).