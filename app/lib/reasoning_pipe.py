import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List
import logging

logger = logging.getLogger(__name__)

class ReasoningPipeWriteError(Exception):
    """Raised when there is an error writing to the reasoning pipe file."""
    pass

class ReasoningPipe:
    """
    Standard library for capturing reasoning model chain-of-thought and session metadata.
    """

    def __init__(self, ghost_name: str, session_id: str, model: str, tier: str, agent_name: str = None):
        """
        Initialize a ReasoningPipe for capturing agent reasoning.
        
        Args:
            ghost_name: The Ghost identity (permanent role like "Librarian", "Scout")
            session_id: Unique session identifier
            model: Shell model name (e.g., "gemma2:27b")
            tier: L1/L2/L3 tier
            agent_name: DEPRECATED - Use ghost_name instead. Kept for backward compatibility.
        """
        # Backward compatibility: if agent_name is provided but ghost_name is not, use agent_name
        if agent_name and not ghost_name:
            ghost_name = agent_name
        
        self.ghost_name = ghost_name
        self.agent_name = ghost_name  # Alias for backward compatibility
        self.session_id = session_id
        self.model = model
        self.tier = tier
        
        self.start_time = datetime.now()
        self.buffer: List[str] = []
        self.metrics: Dict = {
            "tokens": 0,
            "duration": 0.0,
            "cost": 0.0,
            "tokens_per_second": 0.0
        }
        self.task_description: Optional[str] = None
        self.is_finalized = False
        
        self.journals_dir = Path("docs/journals")
        self.output_path = self.journals_dir / f"{ghost_name}_{session_id}.md"
        self.summary_path = self.journals_dir / f"{ghost_name}_journal.md"

    def _get_timestamp_str(self, timestamp: Optional[datetime] = None) -> str:
        ts = timestamp or datetime.now()
        return ts.strftime("%H:%M:%S.%f")[:-3]

    def log_thought(self, content: str, timestamp: Optional[datetime] = None) -> None:
        """
        Logs a thought to the buffer.
        """
        if not isinstance(content, str) or not content.strip():
            raise ValueError("Thought content must be a non-empty string.")
        
        ts_str = self._get_timestamp_str(timestamp)
        self.buffer.append(f"**[{ts_str}]** THOUGHT: {content}")

    def log_action(self, action: str, details: Optional[Dict] = None) -> None:
        """
        Logs an action to the buffer.
        """
        ts_str = self._get_timestamp_str()
        action_str = f"**[{ts_str}]** ACTION: {action}"
        if details:
            details_str = ", ".join(f"{k}: {v}" for k, v in details.items())
            action_str += f" ({details_str})"
        self.buffer.append(action_str)

    def log_result(self, result: str, metrics: Optional[Dict] = None) -> None:
        """
        Logs the final result and updates session metrics.
        """
        ts_str = self._get_timestamp_str()
        self.buffer.append(f"**[{ts_str}]** RESULT: {result}")
        if metrics:
            self.metrics.update(metrics)

    def set_task(self, description: str) -> None:
        """
        Sets the task description for the session.
        """
        self.task_description = description

    def finalize(self) -> Path:
        """
        Writes the buffer to a markdown file and clears the buffer.
        """
        if self.is_finalized:
            logger.warning(f"ReasoningPipe for {self.ghost_name} session {self.session_id} already finalized.")
            return self.output_path

        try:
            self.journals_dir.mkdir(parents=True, exist_ok=True)
            
            end_time = datetime.now()
            duration = (end_time - self.start_time).total_seconds()
            self.metrics["duration"] = round(duration, 2)
            
            if self.metrics.get("tokens", 0) > 0 and duration > 0:
                self.metrics["tokens_per_second"] = round(self.metrics["tokens"] / duration, 2)

            buffer_contents = "\n\n".join(self.buffer)
            
            template = f"""# ReasoningPipe: {self.ghost_name} | Session: {self.session_id}

**Started**: {self.start_time.isoformat()}  
**Model**: {self.model}  
**Tier**: {self.tier}  
**Task**: {self.task_description or "N/A"}

---

## Thought Stream

{buffer_contents}

---

## Session Metadata

**Duration**: {self.metrics['duration']}s  
**Tokens Generated**: {self.metrics['tokens']}  
**Efficiency**: {self.metrics['tokens_per_second']} tok/s  
**Cost**: ${self.metrics['cost']} ({self.tier})  
**Finalized**: {end_time.isoformat()}
"""
            with open(self.output_path, "w") as f:
                f.write(template)

            # Append summary line to agent-specific journal
            summary_line = f"- {end_time.strftime('%Y-%m-%d %H:%M:%S')} | Session: [{self.session_id}]({self.output_path.name}) | Model: {self.model} | Tier: {self.tier} | Success: {self.metrics.get('success', 'N/A')}\n"
            with open(self.summary_path, "a") as f:
                f.write(summary_line)

            self.is_finalized = True
            self.buffer = []
            return self.output_path

        except Exception as e:
            logger.error(f"Failed to finalize ReasoningPipe: {e}")
            raise ReasoningPipeWriteError(f"Failed to write ReasoningPipe to {self.output_path}: {e}")
