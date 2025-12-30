import subprocess
import logging

logger = logging.getLogger("AGY_REFLEX")

def execute_git_sync(commit_msg: str = "Auto-save: L1 Reflex Action") -> str:
    """
    Executes the Git Trilogy: Add -> Commit -> Push.
    """
    try:
        logger.info("⚡ Reflex Triggered: GIT_SYNC")
        
        # 1. Git Add
        subprocess.run(["git", "add", "."], check=True, stdout=subprocess.DEVNULL)
        
        # 2. Git Commit (allow empty if nothing changed)
        # We use run() but capture errors to avoid crashing if there's nothing to commit
        subprocess.run(["git", "commit", "-m", commit_msg], stderr=subprocess.DEVNULL)
        
        # 3. Git Push
        push_res = subprocess.run(["git", "push"], capture_output=True, text=True)
        
        if push_res.returncode == 0:
            return "✅ **System Action:** Codebase successfully synced to GitHub."
        else:
            return f"⚠️ **Sync Warning:** Push returned code {push_res.returncode}. (Check remote connection)"

    except Exception as e:
        logger.error(f"Reflex Error: {e}")
        return f"❌ **System Error:** Failed to execute Git Sync. ({str(e)})"