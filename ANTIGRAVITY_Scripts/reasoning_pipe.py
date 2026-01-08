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
    """Appends verbatim content to both the session buffer and the daily thoughts log."""
    if not os.path.exists(THOUGHTS_DIR):
        os.makedirs(THOUGHTS_DIR)
    
    thoughts_log, _ = get_dated_filenames()
    entry_id = get_next_id()
    
    # Structure: [itj-XXX] Content
    formatted_entry = f"[{entry_id}] {content}"
    
    # 1. Live Feed: Daily Thoughts Log
    with open(thoughts_log, "a") as f:
        f.write(formatted_entry + "\n")
        f.flush()
        os.fsync(f.fileno())

    # 2. Buffer: Current Session (for /reason synthesis)
    with open(CURRENT_SESSION_FILE, "a") as f:
        f.write(formatted_entry + "\n")

def handle_session_transition():
    """Clears the session buffer. Since /log trickles live, archival is already done."""
    if not os.path.exists(CURRENT_SESSION_FILE):
        open(CURRENT_SESSION_FILE, 'w').close()
        return

    # Clear the buffer
    open(CURRENT_SESSION_FILE, 'w').close()
    print("✅ Session buffer cleared. Thoughts were trickled to the dated log during the session.")
    print("Status: [itj-000] Session Transition Complete.")

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

