#!/usr/bin/env python3
import sys
import os
from datetime import datetime

def log_reasoning(target_file, content):
    """
    Appends content verbatim to the target file with a timestamp header.
    Ensures no agent-side 'editing' occurs during the write process.
    """
    # Ensure the directory exists
    os.makedirs(os.path.dirname(target_file), exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header = f"\n\n--- [REASONING PIPE DUMP: {timestamp}] ---\n"
    
    with open(target_file, "a", encoding="utf-8") as f:
        f.write(header)
        f.write(content)
        f.write("\n")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ./reasoning_pipe.py <target_file> <content>")
        sys.exit(1)
    
    target = sys.argv[1]
    # Joining the content argument
    text = sys.argv[2]
    log_reasoning(target, text)
