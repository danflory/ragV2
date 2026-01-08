import sys
import os
import re
from datetime import datetime

# Antigravity Reasoning Pipe
# Technical Implementation of GOOGLE_ANTIGRAVITY_SPEC.md
# fulfills: 1. Thinking Transparency (RAW dumps)
#           2. Session Transition & Archival (Phase A & B)

JOURNAL_DIR = "docs/journals"
EXECUTIVE_DIR = os.path.join(JOURNAL_DIR, "executive")
THOUGHTS_DIR = os.path.join(JOURNAL_DIR, "thoughts")
CURRENT_SESSION_FILE = os.path.join(THOUGHTS_DIR, "current_session.md")

def get_dated_filenames():
    today = datetime.now().strftime("%Y-%m-%d")
    thoughts_log = os.path.join(THOUGHTS_DIR, f"{today}_thoughts.md")
    executive_log = os.path.join(EXECUTIVE_DIR, f"{today}_executive.md")
    return thoughts_log, executive_log

def get_next_id():
    """Reads the current session file to determine the next sequential [itj-XXX] ID."""
    if not os.path.exists(CURRENT_SESSION_FILE):
        return "itj-001"
    
    with open(CURRENT_SESSION_FILE, "r") as f:
        content = f.read()
    
    # Find all [itj-XXX] tags
    matches = re.findall(r"\[itj-(\d+)\]", content)
    
    if not matches:
        return "itj-001"
    
    last_id = int(matches[-1])
    next_id = last_id + 1
    return f"itj-{next_id:03d}"

def log_thought(content):
    """Appends verbatim content with auto-incrementing ID to the current session buffer."""
    if not os.path.exists(THOUGHTS_DIR):
        os.makedirs(THOUGHTS_DIR)
    
    # Auto-numbering logic
    entry_id = get_next_id()
    
    # Structure: [itj-XXX] Content
    formatted_entry = f"[{entry_id}] {content}"
    
    with open(CURRENT_SESSION_FILE, "a") as f:
        f.write(formatted_entry + "\n")

def handle_session_transition():
    """Fulfills Section 3 of the Spec: Buffer Archival and Executive Synthesis."""
    if not os.path.exists(CURRENT_SESSION_FILE) or os.path.getsize(CURRENT_SESSION_FILE) == 0:
        # Buffer is already clear, just ensure it exists
        open(CURRENT_SESSION_FILE, 'w').close()
        return

    thoughts_log, executive_log = get_dated_filenames()
    
    # PHASE A: Buffer Archival
    with open(CURRENT_SESSION_FILE, "r") as f:
        buffer_content = f.read()
    
    with open(thoughts_log, "a") as f:
        f.write(f"\n--- SESSION START: {datetime.now().strftime('%H:%M:%S')} ---\n")
        f.write(buffer_content)
    
    # PHASE B: Executive Synthesis (Triggered)
    # Note: Full automated synthesis requires LLM inference. 
    # This script prepares the buffer and clears it.
    
    # Clear the buffer
    open(CURRENT_SESSION_FILE, 'w').close()
    print(f"✅ Session archived to {thoughts_log}. Buffer cleared.")
    print("Status: [itj-000] Session Transition Complete. Thinking Transparency Active.")

if __name__ == "__main__":
    if not os.path.exists(EXECUTIVE_DIR):
        os.makedirs(EXECUTIVE_DIR)
    if not os.path.exists(THOUGHTS_DIR):
        os.makedirs(THOUGHTS_DIR)

    # Mode Selection
    if len(sys.argv) > 1:
        first_arg = sys.argv[1]

        if first_arg == "--init":
            # Explicit Initialization
            handle_session_transition()
            sys.exit(0)
        
        elif first_arg == "--stdin":
            # Safe Input Mode: Read from Stdin
            # Usage: echo "Content" | python3 reasoning_pipe.py --stdin
            # or from a file/heredoc
            content = sys.stdin.read().strip()
            if content:
                log_thought(content)
            sys.exit(0)
        
        else:
            # Legacy/Simple Mode: Arguments as content
            thought = " ".join(sys.argv[1:])
            log_thought(thought)
            sys.exit(0)

    # Default (No Args): Initialization Mode (Backward Compatibility for recon.md)
    handle_session_transition()

