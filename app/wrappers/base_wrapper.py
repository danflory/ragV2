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

    def __init__(self, agent_name: str, session_id: str, model: str, tier: str):
        self.agent_name = agent_name
        self.session_id = session_id
        self.model = model
        self.tier = tier
        
        self.pipe = ReasoningPipe(agent_name, session_id, model, tier)
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
