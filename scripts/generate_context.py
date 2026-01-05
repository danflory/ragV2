import os
import datetime

# --- CONFIGURATION ---
OUTPUT_FILE = "docs/GRAVITAS_SESSION_CONTEXT.md"

# FILES TO IGNORE IN TREE
IGNORE_DIRS = {".git", "__pycache__", "venv", ".venv", "node_modules", ".idea", "chroma_db", "site-packages", "data"}
IGNORE_FILES = {".DS_Store", "poetry.lock", "package-lock.json", "LICENSE", "GRAVITAS_SESSION_CONTEXT.md", "AGY_SESSION_CONTEXT.md"}

# --- HEADER ---
STRATEGY_HEADER = """
# Gravitas Grounded Research - Session Context
**Generated:** {timestamp}
**System:** Titan RTX (Local) + DeepInfra (Cloud)
**App State:** Docker Microservices

"""

def get_project_root():
    """Smart detection of project root."""
    current_dir = os.getcwd()
    if os.path.exists(os.path.join(current_dir, "app")):
        return current_dir
    return current_dir

def read_section(startpath, relative_path, section_title):
    """Generic helper to read a markdown file and wrap it as a section."""
    full_path = os.path.join(startpath, relative_path)
    content = ""
    
    if os.path.exists(full_path):
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                # We strip the existing headers to avoid markdown nesting chaos
                raw_text = f.read().strip()
                content = f"\n{raw_text}\n"
        except Exception as e:
            content = f"\n*Error reading {relative_path}: {e}*\n"
    else:
        content = f"\n*Missing {relative_path} - Please create this file.*\n"

    # Return formatted section
    return f"\n---\n## {section_title}\n{content}\n"

def generate_tree(startpath):
    """Generates a visual file tree."""
    tree_str = "## PHYSICAL FILE MAP\n```text\n"
    tree_str += f"{os.path.basename(startpath)}/\n"
    
    for root, dirs, files in os.walk(startpath):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        level = root.replace(startpath, '').count(os.sep)
        if root == startpath:
            level = -1
            
        indent = ' ' * 4 * (level + 1)
        subindent = ' ' * 4 * (level + 2)
        
        if root != startpath:
            tree_str += '{}{}/\n'.format(indent, os.path.basename(root))
        
        for f in files:
            if f not in IGNORE_FILES:
                if root == startpath:
                     tree_str += '    {}\n'.format(f)
                else:
                     tree_str += '{}{}\n'.format(subindent, f)
    tree_str += "```\n"
    return tree_str

def read_key_code_files(startpath):
    """Reads content of critical source code."""
    CRITICAL_FILES = [
        "app/main.py",
        "app/config.py",
        "app/L1_local.py",
        "app/L2_network.py",
        "app/router.py",
        "app/container.py",
        "Dockerfile",
        "docker-compose.yml",
        ".env.example",
        "scripts/monitor.sh"
    ]
    
    content_str = "## CRITICAL SOURCE CODE\n"
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
    root = get_project_root()
    
    print(f"🔍 Compiling Gravitas Context from: {root}")
    
    # 1. HEADER
    output = STRATEGY_HEADER.format(timestamp=timestamp)
    
    # 2. HARDWARE OPERATIONS
    print("   + Injecting Hardware Ops...")
    output += read_section(root, "docs/004_hardware_operations.md", "HARDWARE OPERATIONS")
    
    # 3. STRATEGIC ROADMAP
    print("   + Injecting Roadmap...")
    output += read_section(root, "docs/ROADMAP.md", "STRATEGIC ROADMAP")
    
    # 4. FILE TREE
    print("   + Generating File Tree...")
    output += "\n---\n"
    output += generate_tree(root)
    
    # 5. CODE
    print("   + Reading Critical Code...")
    output += "\n---\n"
    output += read_key_code_files(root)
    
    # SAVE
    outfile_path = os.path.join(root, OUTPUT_FILE)
    os.makedirs(os.path.dirname(outfile_path), exist_ok=True)
    
    with open(outfile_path, "w", encoding="utf-8") as f:
        f.write(output)
    
    print(f"✅ COMPILED: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
