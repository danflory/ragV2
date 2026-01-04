I need you to implement the DeepSeek Sidecar MVP. This will allow us to use a local coding model for development while the main RAG pipeline is being built.

Use the following "TO DO" list as your execution plan. Adhere to the project's Test-First and Documentation standards.

Context
Target Hardware: GPU 0 (Titan RTX, 24GB VRAM).

Service Host: The existing agy_ollama container running on port 11434.

Objective: Deploy deepseek-coder-v2 alongside the existing gemma2:27b model and verify external access for IDE integration.

📋 TO DO: DeepSeek Sidecar MVP
1. Discovery & Validation
[ ] Check Container Health: Verify agy_ollama is running.

Command: docker ps | grep agy_ollama

[ ] Check GPU Status: Ensure GPU 0 has available VRAM or is ready for model swapping.

Command: nvidia-smi (Run inside WSL or check logs).

[ ] List Current Models: See what is currently installed.

Command: docker exec agy_ollama ollama list

2. Model Acquisition
[ ] Pull Model: Download the deepseek-coder-v2 model into the container.

Note: Use the standard tag (approx 16B parameters) to fit comfortably within the Titan RTX's 24GB VRAM.

Command: docker exec agy_ollama ollama pull deepseek-coder-v2

3. Verification (Test-First)
[ ] Create Test Script: Create tests/test_deepseek_sidecar.py.

Requirement: The test must hit http://localhost:11434/v1/chat/completions (OpenAI compatible endpoint).

Payload: { "model": "deepseek-coder-v2", "messages": [{"role": "user", "content": "Print hello world in python"}] }

Assertion: Verify HTTP 200 OK and that "content" exists in the response.

[ ] Execute Test: Run pytest tests/test_deepseek_sidecar.py and ensure it passes.

4. Documentation
[ ] Create Documentation: Create docs/DEEPSEEK_SIDECAR.md.

Content: Document the connection details for VS Code / Cline.

Details to include:

Provider: OpenAI Compatible

Base URL: http://localhost:11434/v1

Model ID: deepseek-coder-v2

API Key: ollama (placeholder)

Warning: Add a note about "Model Swapping Latency" (~2-3s) when switching between RAG (Gemma) and Coding (DeepSeek) tasks.

5. Cleanup
[ ] Git Status: Verify no unnecessary files were created.

[ ] Final Report: Confirm the service is ready for IDE connection.
