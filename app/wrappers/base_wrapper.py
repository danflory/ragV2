from abc import ABC, abstractmethod
from typing import Optional, Dict
from pathlib import Path
from app.lib.reasoning_pipe import ReasoningPipe
from app.services.supervisor.guardian import SupervisorGuardian

class GravitasAgentWrapper(ABC):
    """
    Base class all agent wrappers must inherit from.
    Handles the ReasoningPipe protocol and Supervisor certification enforcement.
    """

    def __init__(self, ghost_name: str = None, session_id: str = None, model: str = None, tier: str = None, agent_name: str = None):
        """
        Initialize the agent wrapper.
        
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
        
        self.pipe = ReasoningPipe(ghost_name=ghost_name, session_id=session_id, model=model, tier=tier)
        self.supervisor = SupervisorGuardian()

    async def execute_task(self, task: Dict) -> Dict:
        """
        The standardized execution flow for all agents.
        DO NOT OVERRIDE this method. Subclasses should implement _execute_internal.
        """
        # 1. Request permission from Supervisor
        permission = await self.supervisor.notify_session_start(
            agent=self.agent_name,
            session_id=self.session_id,
            metadata={"task": task, "model": self.model, "tier": self.tier}
        )
        
        if not permission.allowed:
            raise RuntimeError(f"Session rejected by Supervisor: {permission.reason}")

        try:
            # 2. Extract task description for ReasoningPipe if provided
            if "prompt" in task:
                self.pipe.set_task(task["prompt"][:200]) # Summary of task
            
            # 3. Execute model-specific logic
            result = await self._execute_internal(task)
            
            # 4. Finalize the reasoning pipe
            pipe_file = self.pipe.finalize()
            
            # 5. Notify Supervisor of completion
            await self.supervisor.notify_session_end(
                session_id=self.session_id,
                output_file=pipe_file
            )
            
            return result
        except Exception as e:
            # Even on failure, we should try to finalize if there's content
            if self.pipe.buffer:
                try:
                    self.pipe.log_result(f"Error occurred: {str(e)}")
                    pipe_file = self.pipe.finalize()
                    await self.supervisor.notify_session_end(self.session_id, pipe_file)
                except:
                    pass
            raise e

    @abstractmethod
    async def _execute_internal(self, task: Dict) -> Dict:
        """
        Model-specific execution logic.
        
        Must call:
        - self.pipe.log_thought() for reasoning steps
        - self.pipe.log_action() for concrete actions
        - self.pipe.log_result() for final output
        """
        pass

    @abstractmethod
    def _parse_thought(self, chunk: Dict) -> Optional[str]:
        """
        Extract reasoning content from model response chunk.
        """
        pass

    @abstractmethod
    def _parse_action(self, chunk: Dict) -> Optional[str]:
        """
        Extract action declarations from model response chunk.
        """
        pass
