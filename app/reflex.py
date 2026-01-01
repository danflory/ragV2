import subprocess
import logging
import os
from datetime import datetime
from .safety import validate_command, validate_python_syntax, scan_for_secrets

logger = logging.getLogger("AGY_REFLEX")

async def execute_shell(command: str) -> str:
    """
    Executes a shell command in the container.
    """
    if not validate_command(command):
        return "❌ SECURITY BLOCK: Command failed Gatekeeper check."

    logger.info(f"⚡ EXECUTING: {command}")

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        output = result.stdout + result.stderr
        if result.returncode == 0:
            return f"✅ SUCCESS:\n{output}"
        else:
            return f"⚠️ FAILED (Code {result.returncode}):\n{output}"

    except subprocess.TimeoutExpired:
        return "⏱️ TIMEOUT: Command took too long."
    except Exception as e:
        return f"💥 EXCEPTION: {str(e)}"

async def write_file(filepath: str, content: str) -> str:
    """
    Overwrites a file with new content.
    """
    if ".." in filepath or filepath.startswith("/"):
        return "❌ PATH ERROR: Relative paths only (security)."
        
    if scan_for_secrets(content):
        return "❌ SECURITY BLOCK: Content contains secrets."

    if filepath.endswith(".py") and not validate_python_syntax(content):
        return "❌ SYNTAX ERROR: Python code does not compile. Write rejected."

    try:
        # FIX: Only create directory if path implies one
        directory = os.path.dirname(filepath)
        if directory:
            os.makedirs(directory, exist_ok=True)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
            
        logger.info(f"💾 WROTE: {filepath} ({len(content)} bytes)")
        return f"✅ FILE SAVED: {filepath}"

    except Exception as e:
        return f"💥 WRITE ERROR: {str(e)}"

async def execute_git_sync(message: str = "Auto-sync by AntiGravity") -> str:
    """
    Performs a full Git sync: Add -> Commit -> Push.
    """
    try:
        if message == "Auto-sync by AntiGravity":
            message = f"AGY Auto-sync: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

        commands = [
            "git config --global --add safe.directory /app",
            "git config --global user.email 'antigravity@internal.ai'",
            "git config --global user.name 'AntiGravity Agent'",
            "git add .",
            f'git commit -m "{message}"',
            "git push"
        ]

        log_output = []
        for cmd in commands:
            logger.info(f"🔄 GIT: {cmd}")
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True, timeout=30
            )
            output = result.stdout + result.stderr.strip()
            
            if result.returncode != 0 and "nothing to commit" not in output:
                 return f"⚠️ GIT ERROR on '{cmd}':\n{output}"
            
            log_output.append(f"$ {cmd} -> {output}")

        return f"✅ GIT SYNC COMPLETE:\n" + "\n".join(log_output)

    except Exception as e:
        return f"💥 GIT EXCEPTION: {str(e)}"