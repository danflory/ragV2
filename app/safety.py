import re
import logging
import ast
import json
import yaml
from typing import Optional, Union

logger = logging.getLogger("Gravitas_SAFETY")

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

# 3. SELF-PRESERVATION FILES
PROTECTED_FILES = [
    "safety.py",
    "container.py",
    "app/safety.py",
    "app/container.py"
]

# 4. DANGEROUS SQL KEYWORDS
DANGEROUS_SQL_KEYWORDS = [
    "DROP", "TRUNCATE", "GRANT", "REVOKE", "DELETE"
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

def validate_syntax(filepath: str, content: str) -> bool:
    """
    Multi-format syntax validator with file-type specific checks.
    """
    if not filepath or not content:
        return False

    file_ext = filepath.lower().split('.')[-1]

    try:
        if file_ext == 'py':
            return _validate_python_syntax(content)
        elif file_ext in ['yml', 'yaml']:
            return _validate_yaml_syntax(content)
        elif file_ext == 'json':
            return _validate_json_syntax(content)
        elif file_ext == 'sql':
            return _validate_sql_syntax(content)
        elif file_ext == 'sh' or filepath.endswith('.sh'):
            return _validate_shell_syntax(content)
        else:
            # For unknown file types, just check for secrets
            return not scan_for_secrets(content)
    except Exception as e:
        logger.error(f"❌ SYNTAX VALIDATION ERROR for {filepath}: {e}")
        return False

def _validate_python_syntax(code: str) -> bool:
    """Validate Python code with AST parsing and import auditing."""
    try:
        # Parse AST
        tree = ast.parse(code)

        # Import audit - block dangerous imports
        dangerous_imports = ['subprocess', 'os.system', 'shutil.rmtree']
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name in dangerous_imports:
                        logger.warning(f"🛑 BLOCKED: Dangerous import '{alias.name}' in Python code")
                        return False
            elif isinstance(node, ast.ImportFrom):
                if node.module in dangerous_imports:
                    logger.warning(f"🛑 BLOCKED: Dangerous import from '{node.module}' in Python code")
                    return False

        return True
    except SyntaxError as e:
        logger.error(f"❌ PYTHON SYNTAX ERROR: {e}")
        return False

def _validate_yaml_syntax(content: str) -> bool:
    """Validate YAML syntax and basic schema requirements."""
    try:
        data = yaml.safe_load(content)
        # Basic schema check - ensure it's a dict with required keys for known configs
        if isinstance(data, dict):
            # For docker-compose style files
            if 'services' in data or 'version' in data:
                if 'services' not in data:
                    logger.warning("⚠️ YAML: Missing 'services' key in docker-compose like file")
                    return False
        return True
    except yaml.YAMLError as e:
        logger.error(f"❌ YAML SYNTAX ERROR: {e}")
        return False

def _validate_json_syntax(content: str) -> bool:
    """Validate JSON syntax and type safety."""
    try:
        data = json.loads(content)
        # Type safety checks for common vector/metadata structures
        if isinstance(data, dict):
            # Check for vector arrays (should be lists of floats)
            for key, value in data.items():
                if 'vector' in key.lower() and isinstance(value, list):
                    if not all(isinstance(x, (int, float)) for x in value):
                        logger.warning(f"⚠️ JSON: Vector field '{key}' contains non-numeric values")
                        return False
        return True
    except json.JSONDecodeError as e:
        logger.error(f"❌ JSON SYNTAX ERROR: {e}")
        return False

def _validate_sql_syntax(content: str) -> bool:
    """Validate SQL by blocking dangerous keywords."""
    sql_upper = content.upper()
    for keyword in DANGEROUS_SQL_KEYWORDS:
        if keyword in sql_upper:
            logger.warning(f"🛑 BLOCKED: Dangerous SQL keyword '{keyword}' detected")
            return False
    return True

def _validate_shell_syntax(content: str) -> bool:
    """Validate shell commands with scope restrictions."""
    # Check for banned commands
    for ban in BANNED_COMMANDS:
        if ban in content:
            logger.warning(f"🛑 BLOCKED: Banned command '{ban}' in shell script")
            return False

    # Scope restriction - should only operate within /rag_local
    if '/' in content and not content.strip().startswith('cd /rag_local'):
        # Allow some safe absolute paths but restrict others
        allowed_paths = ['/rag_local', '/tmp', '/var/log']
        if not any(allowed in content for allowed in allowed_paths):
            logger.warning("🛑 BLOCKED: Shell command attempts to access restricted paths")
            return False

    return not scan_for_secrets(content)

def check(command: Optional[str] = None, content: Optional[str] = None, filepath: Optional[str] = None) -> bool:
    """
    Unified safety orchestrator that combines all security checks.
    """
    # Self-preservation check
    if filepath:
        filename = filepath.split('/')[-1]
        if filename in PROTECTED_FILES or filepath in PROTECTED_FILES:
            logger.critical(f"🛑 SELF-PRESERVATION: Attempted to modify protected file '{filepath}'")
            return False

    # Command validation
    if command:
        if not validate_command(command):
            return False

    # Content validation
    if content:
        if scan_for_secrets(content):
            return False

        if filepath:
            if not validate_syntax(filepath, content):
                return False

    return True
