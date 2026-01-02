# Cognitive Pipeline & Tools
- Call gravitas_learn_file immediately after modifying .py files.

# Development Workflow (Gatekeeper Protocol)
1. RED: Create failing test in tests/.
2. GREEN: Write minimal code in app/ (SOLID principles).
3. REFACTOR: Clean up and call gravitas_learn_file.

# Security & Safety
- Use os.getenv() for secrets. No rm -rf without confirmation.
