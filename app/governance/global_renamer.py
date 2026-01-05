import os
import logging
import asyncio
from typing import List, Optional
from app.container import container
from app.config import config

logger = logging.getLogger("Gravitas_GLOBAL_RENAME")

class GlobalRenamer:
    """
    Robust service for performant, LLM-guided refactoring of documentation.
    Specially designed to rename project identifiers with situational awareness.
    """
    
    def __init__(self, target_model: str = "deepseek-coder-v2"):
        self.target_model = target_model
        self.stats = {
            "files_processed": 0,
            "changes_made": 0,
            "errors": 0
        }

    async def _ensure_dev_mode(self):
        """Switches the system to DEV mode to ensure correct model is loaded."""
        if container.current_mode != "dev":
            logger.info(f"🔄 Switching to DEV mode for refactoring (Model: {self.target_model})...")
            # We bypass the container.switch_mode logic slightly if we want a specific model
            # But let's use the official switch
            await container.switch_mode("dev")

    async def refactor_text(self, content: str, search_term: str, replace_term: str) -> str:
        """
        Uses the LLM to surgically replace terms while maintaining context and link integrity.
        """
        # Prompt designed for DeepSeek Coder
        prompt = f"""
        ### Task
        Refactor the following text by replacing all occurrences of "{search_term}" (and its case variants or common combinations) with "{replace_term}".
        
        ### Constraints
        1. Maintain all Markdown formatting.
        2. Ensure internal Markdown links (e.g. [Link](old_name.md)) are preserved or logically updated.
        3. Do NOT change technical constants or code blocks unless they are specifically named "{search_term}".
        4. Consistency: If you see "AGY RAG", change it to "Gravitas RAG" if that is the standard intended.
        5. Return ONLY the refactored text. No explanations.
        6. Do NOT wrap the response in Markdown code blocks (e.g. ```python ... ```). Return raw text.

        ### Content to Refactor:
        {content}
        """
        
        try:
            # We use the L1 driver which should now be in DEV mode
            refined_content = await container.l1_driver.generate(prompt)
            
            # Simple heuristic to check if the LLM failed or returned an "I cannot" message
            if len(refined_content) < len(content) * 0.5 and len(content) > 100:
                 logger.warning("⚠️ LLM returned suspiciously short response. Reverting to safe string replace.")
                 return content.replace(search_term, replace_term)
            
            # HARD STRIP: Clean up markdown blocks if the LLM hallucinated them
            if refined_content.startswith("```"):
                lines = refined_content.splitlines()
                if lines[0].startswith("```"):
                    lines = lines[1:]
                if lines and lines[-1].startswith("```"):
                    lines = lines[:-1]
                refined_content = "\n".join(lines).strip()
                 
            return refined_content
        except Exception as e:
            logger.error(f"❌ LLM Refactor failed: {e}")
            return content.replace(search_term, replace_term)

    async def process_file(self, file_path: str, search_term: str, replace_term: str, dry_run: bool = True):
        """Processes a single file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            if search_term.lower() not in content.lower():
                return

            logger.info(f"📄 Processing: {file_path}")
            
            # Update heartbeat for monitor
            try:
                with open("/tmp/gravitas_heartbeat", "w") as f:
                    f.write(file_path)
            except:
                pass

            if dry_run:
                logger.info(f"🔎 [DRY RUN] Would refactor {file_path}")
                self.stats["files_processed"] += 1
                return

            # Execute Refactor
            new_content = await self.refactor_text(content, search_term, replace_term)
            
            if new_content != content:
                # Create backup
                backup_path = f"{file_path}.bak"
                with open(backup_path, 'w', encoding='utf-8') as b:
                    b.write(content)
                
                # Write changes
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                logger.info(f"✅ Refactored and saved: {file_path}")
                self.stats["changes_made"] += 1
            
            self.stats["files_processed"] += 1

        except Exception as e:
            logger.error(f"❌ Error processing {file_path}: {e}")
            self.stats["errors"] += 1

    async def run(self, directory: str, search_term: str, replace_term: str, extensions=[".md", ".txt"], dry_run: bool = True):
        """
        Walks the directory and refactors matching files.
        """
        await self._ensure_dev_mode()
        
        logger.info(f"🚀 Starting Global Rename: {search_term} -> {replace_term}")
        logger.info(f"📂 Target: {directory} | Dry Run: {dry_run}")

        for root, dirs, files in os.walk(directory):
            # Skip hidden dirs
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    file_path = os.path.join(root, file)
                    await self.process_file(file_path, search_term, replace_term, dry_run)

        logger.info("🏁 Global Rename Operation Finished.")
        logger.info(f"📊 Stats: {self.stats}")
        return self.stats

# Singleton for simplified usage
global_rename_service = GlobalRenamer()
