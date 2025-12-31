# app/safety.py
import re
import logging
import ast

logger = logging.getLogger("AGY_SAFETY")

# 1. THE BLACKLIST
# Commands that are absolutely forbidden, even with supervision.
BANNED_COMMANDS = [
    "rm -rf", "mkfs", "dd if=", ":(){ :|:& };:", # Fork bomb
    "shutdown", "reboot", "wget", "curl", # limit web access for now
    "chmod 777", "> /dev/sda", "mv /",
    ".env" # Never touch the env file directly
]

# 2. SECRET PATTERNS
# Regex to catch API keys before they leak into logs or files.
SECRET_PATTERNS = [
    r"sk-[a-zA-Z0-9]{20,}",           # OpenAI / DeepInfra style
    r"AIza[0-9A-Za-z-_]{35}",         # Google API keys
    r"ghp_[0-9a-zA-Z]{36}",           # GitHub Personal Tokens
]

def scan_for_secrets(content: str) -> bool:
    """Returns True if a secret is detected."""
    for pattern in SECRET_PATTERNS:
        if re.search(pattern, content):
            logger.critical("🛑 SECURITY: Attempted to leak a secret!")
            return True
    return False

def validate_command(command: str) -> bool:
    """
    Returns True if command is safe to execute.
    """
    # 1. Empty Check
    if not command or not command.strip():
        return False

    # 2. Blacklist Check
    for ban in BANNED_COMMANDS:
        if ban in command:
            logger.warning(f"🛑 BLOCKED: Banned command attempt -> '{ban}'")
            return False

    # 3. Secret Check
    if scan_for_secrets(command):
        return False

    return True

def validate_python_syntax(code: str) -> bool:
    """
    Parses Python code to ensure it compiles before saving.
    Prevents writing broken files that crash the server.
    """
    try:
        ast.parse(code)
        return True
    except SyntaxError as e:
        logger.error(f"❌ SYNTAX ERROR: {e}")
        return False