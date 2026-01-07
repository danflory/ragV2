import pytest
import asyncio
import json
import os
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch, AsyncMock

from app.lib.reasoning_pipe import ReasoningPipe, ReasoningPipeWriteError
from app.services.supervisor.guardian import (
    SupervisorGuardian, 
    Certificate, 
    SessionPermission, 
    AgentNotCertifiedError, 
    CertificationExpiredError
)
from app.wrappers.base_wrapper import GravitasAgentWrapper
from app.services.supervisor.certifier import WrapperCertifier
from app.services.supervisor.auditor import ReasoningPipeAuditor

# --- Fixtures ---

@pytest.fixture
def temp_env(tmp_path):
    certs_dir = tmp_path / "certs"
    journals_dir = tmp_path / "journals"
    certs_dir.mkdir(parents=True)
    journals_dir.mkdir(parents=True)
    return certs_dir, journals_dir

# --- TestReasoningPipeClass ---

class TestReasoningPipeClass:
    def test_init_creates_proper_paths(self):
        pipe = ReasoningPipe(ghost_name="Scout", session_id="sess123", model="gpt-4", tier="L2")
        # Default journals_dir in implementation is docs/journals
        assert pipe.ghost_name == "Scout"
        assert pipe.agent_name == "Scout"  # Backward compatibility alias
        assert pipe.session_id == "sess123"
        assert "Scout_sess123.md" in str(pipe.output_path)
        assert "Scout_journal.md" in str(pipe.summary_path)

    def test_log_thought_adds_to_buffer(self):
        pipe = ReasoningPipe(ghost_name="Scout", session_id="sess123", model="gpt-4", tier="L2")
        pipe.log_thought("Thinking about gravitas")
        assert len(pipe.buffer) == 1
        assert "THOUGHT: Thinking about gravitas" in pipe.buffer[0]

    def test_log_action_formats_details(self):
        pipe = ReasoningPipe(ghost_name="Scout", session_id="sess123", model="gpt-4", tier="L2")
        pipe.log_action("Search", {"query": "gravitas", "engine": "google"})
        assert len(pipe.buffer) == 1
        assert "ACTION: Search" in pipe.buffer[0]
        assert "query: gravitas" in pipe.buffer[0]
        assert "engine: google" in pipe.buffer[0]

    def test_log_result_stores_metrics(self):
        pipe = ReasoningPipe(ghost_name="Scout", session_id="sess123", model="gpt-4", tier="L2")
        metrics = {"tokens": 100, "cost": 0.01}
        pipe.log_result("Success", metrics)
        assert len(pipe.buffer) == 1
        assert "RESULT: Success" in pipe.buffer[0]
        assert pipe.metrics["tokens"] == 100
        assert pipe.metrics["cost"] == 0.01

    def test_finalize_writes_file(self, temp_env):
        certs_dir, journals_dir = temp_env
        pipe = ReasoningPipe(ghost_name="Scout", session_id="sess123", model="gpt-4", tier="L2")
        # Point to temp dirs
        pipe.journals_dir = journals_dir
        pipe.output_path = journals_dir / f"{pipe.ghost_name}_{pipe.session_id}.md"
        pipe.summary_path = journals_dir / f"{pipe.ghost_name}_journal.md"
        
        pipe.log_thought("Initial thought")
        pipe.finalize()
        
        assert pipe.output_path.exists()
        assert pipe.summary_path.exists()
        content = pipe.output_path.read_text()
        assert "# ReasoningPipe: Scout" in content
        assert "THOUGHT: Initial thought" in content

    def test_finalize_creates_directory_if_missing(self, tmp_path):
        missing_dir = tmp_path / "missing_journals"
        pipe = ReasoningPipe(ghost_name="Scout", session_id="sess123", model="gpt-4", tier="L2")
        pipe.journals_dir = missing_dir
        pipe.output_path = missing_dir / "test.md"
        pipe.summary_path = missing_dir / "summary.md"
        
        pipe.finalize()
        assert missing_dir.exists()
        assert pipe.output_path.exists()

    def test_double_finalize_warning(self, temp_env, caplog):
        certs_dir, journals_dir = temp_env
        pipe = ReasoningPipe(ghost_name="Scout", session_id="sess123", model="gpt-4", tier="L2")
        pipe.journals_dir = journals_dir
        pipe.output_path = journals_dir / "test.md"
        pipe.summary_path = journals_dir / "summary.md"
        
        pipe.finalize()
        pipe.finalize()
        assert "already finalized" in caplog.text

# --- TestSupervisorGuardian ---

class TestSupervisorGuardian:
    def test_load_certificates_from_directory(self, temp_env):
        certs_dir, _ = temp_env
        cert_data = {
            "agent_name": "Scout",
            "issued_at": datetime.now().isoformat(),
            "expires_at": (datetime.now() + timedelta(days=30)).isoformat(),
            "signature": "hash123",
            "version": "1.0"
        }
        with open(certs_dir / "Scout.json", "w") as f:
            json.dump(cert_data, f)
            
        guardian = SupervisorGuardian(certificates_dir=str(certs_dir))
        assert "Scout" in guardian.certified_agents
        assert guardian.certified_agents["Scout"].signature == "hash123"

    @pytest.mark.asyncio
    async def test_notify_session_start_with_valid_cert(self, temp_env):
        certs_dir, _ = temp_env
        expires_at = datetime.now() + timedelta(days=30)
        cert_data = {
            "agent_name": "Scout",
            "issued_at": datetime.now().isoformat(),
            "expires_at": expires_at.isoformat(),
            "signature": "hash123"
        }
        with open(certs_dir / "Scout.json", "w") as f:
            json.dump(cert_data, f)
            
        guardian = SupervisorGuardian(certificates_dir=str(certs_dir))
        permission = await guardian.notify_session_start("Scout", "sess1", {})
        assert permission.allowed is True
        assert "sess1" in guardian.active_sessions

    @pytest.mark.asyncio
    async def test_notify_session_start_rejects_uncertified(self, temp_env):
        certs_dir, _ = temp_env
        guardian = SupervisorGuardian(certificates_dir=str(certs_dir))
        with pytest.raises(AgentNotCertifiedError):
            await guardian.notify_session_start("UnknownAgent", "sess1", {})

    @pytest.mark.asyncio
    async def test_notify_session_start_rejects_expired(self, temp_env):
        certs_dir, _ = temp_env
        expired_at = datetime.now() - timedelta(days=1)
        cert_data = {
            "agent_name": "Scout",
            "issued_at": (datetime.now() - timedelta(days=31)).isoformat(),
            "expires_at": expired_at.isoformat(),
            "signature": "hash123"
        }
        with open(certs_dir / "Scout.json", "w") as f:
            json.dump(cert_data, f)
            
        guardian = SupervisorGuardian(certificates_dir=str(certs_dir))
        with pytest.raises(CertificationExpiredError):
            await guardian.notify_session_start("Scout", "sess1", {})

    @pytest.mark.asyncio
    async def test_notify_session_end_updates_status(self, temp_env):
        certs_dir, journals_dir = temp_env
        guardian = SupervisorGuardian(certificates_dir=str(certs_dir))
        # Manually add session
        guardian.active_sessions["sess1"] = {
            "agent": "Scout",
            "start_time": datetime.now(),
            "status": "active"
        }
        await guardian.notify_session_end("sess1", journals_dir / "pipe.md")
        assert "sess1" not in guardian.active_sessions
        assert len(guardian.completed_sessions) == 1
        assert guardian.completed_sessions[0]["status"] == "completed"

    def test_get_session_stats_aggregation(self, temp_env):
        certs_dir, _ = temp_env
        guardian = SupervisorGuardian(certificates_dir=str(certs_dir))
        guardian.certified_agents["Scout"] = Certificate("Scout", datetime.now(), datetime.now()+timedelta(days=1), "sig")
        
        guardian.active_sessions["s1"] = {"agent": "Scout", "start_time": datetime.now()}
        guardian.completed_sessions.append({
            "agent": "Scout", 
            "duration": 10.0, 
            "status": "completed"
        })
        
        stats = guardian.get_session_stats("Scout")
        assert stats["Scout"]["active_sessions"] == 1
        assert stats["Scout"]["completed_total"] == 1
        assert stats["Scout"]["avg_duration"] == 10.0

# --- TestBaseWrapper ---

class MockWrapper(GravitasAgentWrapper):
    async def _execute_internal(self, task: dict) -> dict:
        self.pipe.log_thought("Mock thinking")
        self.pipe.log_result("Mock success")
        return {"output": "done"}
    def _parse_thought(self, chunk: dict): return None
    def _parse_action(self, chunk: dict): return None

class TestBaseWrapper:
    @pytest.mark.asyncio
    async def test_execute_task_calls_supervisor(self):
        wrapper = MockWrapper("Scout", "sess1", "gpt-4", "L2")
        wrapper.supervisor = AsyncMock(spec=SupervisorGuardian)
        wrapper.supervisor.notify_session_start.return_value = SessionPermission(allowed=True)
        
        # We need to mock ReasoningPipe.finalize to return a path
        with patch.object(ReasoningPipe, 'finalize', return_value=Path("dummy.md")):
            await wrapper.execute_task({"prompt": "test"})
            
        wrapper.supervisor.notify_session_start.assert_called_once()
        wrapper.supervisor.notify_session_end.assert_called_once()

    @pytest.mark.asyncio
    async def test_execute_task_enforces_certification(self):
        wrapper = MockWrapper("Scout", "sess1", "gpt-4", "L2")
        wrapper.supervisor = AsyncMock(spec=SupervisorGuardian)
        wrapper.supervisor.notify_session_start.return_value = SessionPermission(allowed=False, reason="Not certified")
        
        with pytest.raises(RuntimeError, match="Not certified"):
            await wrapper.execute_task({"prompt": "test"})

    def test_abstract_methods_must_be_implemented(self):
        with pytest.raises(TypeError):
            GravitasAgentWrapper(ghost_name="Scout", session_id="sess1", model="gpt-4", tier="L2")

# --- TestWrapperCertifier ---

class TestWrapperCertifier:
    def test_static_analysis_detects_missing_imports(self, tmp_path):
        bad_wrapper = tmp_path / "bad_wrapper.py"
        bad_wrapper.write_text("class MyWrapper: pass")
        
        certifier = WrapperCertifier(certificates_dir=str(tmp_path / "certs"))
        result = certifier._static_analysis(str(bad_wrapper))
        assert result.passed is False
        assert any("import GravitasAgentWrapper" in e for e in result.errors)

    def test_static_analysis_detects_inheritance(self, tmp_path):
        bad_wrapper = tmp_path / "bad_wrapper.py"
        bad_wrapper.write_text("from app.wrappers.base_wrapper import GravitasAgentWrapper\nclass MyWrapper: pass")
        
        certifier = WrapperCertifier(certificates_dir=str(tmp_path / "certs"))
        result = certifier._static_analysis(str(bad_wrapper))
        # The current implementation checks for method definitions via text search
        assert result.passed is False
        assert any("_execute_internal" in e for e in result.errors)

    @pytest.mark.asyncio
    async def test_dynamic_test_runs_wrapper(self, tmp_path):
        # Create a valid minimal wrapper file
        wrapper_code = """
from app.wrappers.base_wrapper import GravitasAgentWrapper
from typing import Optional, Dict

class ValidWrapper(GravitasAgentWrapper):
    def __init__(self, session_id: str = "test"):
        super().__init__("ValidAgent", session_id, "test-model", "L1")
    
    async def _execute_internal(self, task: Dict) -> Dict:
        self.pipe.log_thought("Thinking...")
        self.pipe.log_result("Success")
        return {"output": "ok"}
        
    def _parse_thought(self, chunk: Dict) -> Optional[str]: return None
    def _parse_action(self, chunk: Dict) -> Optional[str]: return None
"""
        wrapper_path = tmp_path / "valid_wrapper.py"
        wrapper_path.write_text(wrapper_code)
        
        certifier = WrapperCertifier(certificates_dir=str(tmp_path / "certs"))
        
        # We need to mock the environment for dynamic test
        # Since it tries to import app.wrappers.base_wrapper, it should work in the real env.
        # But we need to ensure the journals dir exists
        (Path.cwd() / "docs/journals").mkdir(parents=True, exist_ok=True)
        
        result = await certifier._dynamic_test(str(wrapper_path), "ValidAgent")
        assert result.passed is True
        assert result.pipe_file.exists()

    def test_output_validation_checks_format(self, tmp_path):
        pipe_file = tmp_path / "pipe.md"
        pipe_file.write_text("# ReasoningPipe: Scout\n**Started**: ...\n**Model**: ...\n**Tier**: L1\n**Task**: ...\n## Thought Stream\nTHOUGHT: hi\nRESULT: bye\n## Session Metadata\n**Duration**: 1s\n**Finalized**: ...")
        
        certifier = WrapperCertifier(certificates_dir=str(tmp_path / "certs"))
        result = certifier._validate_output(pipe_file)
        assert result.passed is True

    def test_issue_certificate_creates_file(self, tmp_path):
        wrapper_path = tmp_path / "wrapper.py"
        wrapper_path.write_text("dummy")
        certs_dir = tmp_path / "certs"
        certs_dir.mkdir()
        
        certifier = WrapperCertifier(certificates_dir=str(certs_dir))
        cert = certifier._issue_certificate("Scout", str(wrapper_path))
        
        assert (certs_dir / "Scout.json").exists()
        assert cert.agent_name == "Scout"

# --- TestReasoningPipeAuditor ---

class TestReasoningPipeAuditor:
    @pytest.mark.asyncio
    async def test_audit_quality_scoring(self, temp_env):
        certs_dir, journals_dir = temp_env
        # Create a "good" pipe file
        pipe_content = """# ReasoningPipe: Scout
**Started**: 2026-01-01T00:00:00
**Model**: gpt-4
**Tier**: L2
**Task**: test
## Thought Stream
**[00:00:01]** THOUGHT: think
**[00:00:02]** RESULT: done
## Session Metadata
**Duration**: 2s
**Tokens Generated**: 100
**Efficiency**: 50.0 tok/s
**Cost**: $0.01 (L2)
**Finalized**: 2026-01-01T00:00:02
"""
        pipe_file = journals_dir / "ReasoningPipe_Scout_1.md"
        pipe_file.write_text(pipe_content)
        
        auditor = ReasoningPipeAuditor(certificates_dir=str(certs_dir), journals_dir=str(journals_dir))
        score = auditor._audit_quality([pipe_file])
        
        assert score.total >= 75
        assert score.breakdown["format"] == 40
        assert score.breakdown["completeness"] == 30

    @pytest.mark.asyncio
    async def test_flag_for_recertification(self, temp_env):
        certs_dir, journals_dir = temp_env
        # Create a cert
        cert_data = {"agent_name": "Scout", "issued_at": datetime.now().isoformat(), "expires_at": datetime.now().isoformat(), "signature": "sig"}
        with open(certs_dir / "Scout.json", "w") as f:
            json.dump(cert_data, f)
            
        auditor = ReasoningPipeAuditor(certificates_dir=str(certs_dir), journals_dir=str(journals_dir))
        await auditor._flag_for_recertification("Scout", "Poor quality")
        
        with open(certs_dir / "Scout.json", "r") as f:
            updated_data = json.load(f)
        assert updated_data["status"] == "pending_review"
        assert updated_data["audit_flag"]["reason"] == "Poor quality"
