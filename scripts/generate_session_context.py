import os
import datetime

# --- CONFIGURATION ---
OUTPUT_FILE = "docs/AGY_SESSION_CONTEXT.md"
IGNORE_DIRS = {".git", "__pycache__", "venv", ".venv", "node_modules", ".idea", "chroma_db", "site-packages"}
IGNORE_FILES = {".DS_Store", "poetry.lock", "package-lock.json", "LICENSE"}

# --- MANUAL CONTEXT (The Strategic Brain) ---
STRATEGY_HEADER = """
# AntiGravity RAG - Session Context
**Generated:** {timestamp}
**L2 Provider:** DeepInfra (DeepSeek/Qwen)
**App State:** Dockerization / Security Hardening

## 1. IMMEDIATE TODO LIST
* [CRITICAL] **Secret Hygiene:** Scan codebase for hardcoded keys and move to `.env`.
* [HIGH] **Docker:** Finalize `docker-compose.yml` for GPU passthrough.
* [MED] **L2 Driver:** Verify `DeepInfra` integration in `L2_network.py`.
* [MED] **Gatekeeper:** Implement pre-commit hooks for safety.

## 2. RECENT CHANGES (The Delta)
* Split Spec into Hardware (Static) and App (Dynamic).
* Deprecated OpenRouter.
* Enforced 32GB RAM limit in documentation.
"""

def get_project_root():
    """Smart detection of project root."""
    current_dir = os.getcwd()
    # If we see 'app' folder, we are at root
    if os.path.exists(os.path.join(current_dir, "app")):
        return current_dir
    # If we see 'rag_local', we are one level up
    if os.path.exists(os.path.join(current_dir, "rag_local")):
        return os.path.join(current_dir, "rag_local")
    return current_dir

def generate_tree(startpath):
    """Generates a visual file tree."""
    tree_str = "## 3. PHYSICAL FILE MAP\n```text\n"
    # Just show the root folder name
    tree_str += f"{os.path.basename(startpath)}/\n"
    
    for root, dirs, files in os.walk(startpath):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        # Calculate indentation
        level = root.replace(startpath, '').count(os.sep)
        if root == startpath:
            level = -1
            
        indent = ' ' * 4 * (level + 1)
        subindent = ' ' * 4 * (level + 2)
        
        # Don't print the root line again, logic handles subfolders
        if root != startpath:
            tree_str += '{}{}/\n'.format(indent, os.path.basename(root))
        
        for f in files:
            if f not in IGNORE_FILES:
                # If at root, strict indent
                if root == startpath:
                     tree_str += '    {}\n'.format(f)
                else:
                     tree_str += '{}{}\n'.format(subindent, f)
    tree_str += "```\n"
    return tree_str

def read_key_files(startpath):
    """Reads content of critical files for context."""
    CRITICAL_FILES = [
        "app/main.py",
        "app/config.py",
        "app/L2_network.py",
        "app/router.py",
        "Dockerfile",
        "docker-compose.yml",
        ".env.example" # Never read .env directly!
    ]
    
    content_str = "## 4. CRITICAL FILE CONTENTS\n"
    for rel_path in CRITICAL_FILES:
        full_path = os.path.join(startpath, rel_path)
        if os.path.exists(full_path):
            content_str += f"\n### File: `{rel_path}`\n```python\n"
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content_str += f.read()
            except Exception as e:
                content_str += f"# Error reading file: {e}"
            content_str += "\n```\n"
        else:
             content_str += f"\n### File: `{rel_path}`\n*Not Found*\n"

    return content_str

def main():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    target_dir = get_project_root()
    
    print(f"🔍 Scanning Project Root: {target_dir}")
    
    output = STRATEGY_HEADER.format(timestamp=timestamp)
    output += "\n---\n"
    output += generate_tree(target_dir)
    output += "\n---\n"
    output += read_key_files(target_dir)
    
    # Ensure docs dir exists
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(output)
    
    print(f"✅ Context generated: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()