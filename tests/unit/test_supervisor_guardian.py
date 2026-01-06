import pytest
import json
from pathlib import Path
from datetime import datetime, timedelta
from app.services.supervisor.guardian import (
    SupervisorGuardian, 
    AgentNotCertifiedError, 
    CertificationExpiredError,
    Certificate
)

@pytest.fixture
def certs_dir(tmp_path):
    d = tmp_path / "certs"
    d.mkdir()
    return d

def create_cert(directory: Path, agent_name: str, expired: bool = False):
    issued_at = datetime.now() - timedelta(days=5)
    if expired:
        expires_at = datetime.now() - timedelta(days=1)
    else:
        expires_at = datetime.now() + timedelta(days=30)
    
    cert_data = {
        "agent_name": agent_name,
        "issued_at": issued_at.isoformat(),
        "expires_at": expires_at.isoformat(),
        "signature": "mock_sig",
        "version": "1.0"
    }
    
    cert_file = directory / f"{agent_name}.json"
    cert_file.write_text(json.dumps(cert_data))
    return cert_file

@pytest.mark.asyncio
async def test_guardian_load_certificates(certs_dir):
    create_cert(certs_dir, "Scout")
    create_cert(certs_dir, "Librarian")
    
    guardian = SupervisorGuardian(certificates_dir=str(certs_dir))
    assert "Scout" in guardian.certified_agents
    assert "Librarian" in guardian.certified_agents
    assert len(guardian.certified_agents) == 2

@pytest.mark.asyncio
async def test_notify_session_start_valid(certs_dir):
    create_cert(certs_dir, "Scout")
    guardian = SupervisorGuardian(certificates_dir=str(certs_dir))
    
    permission = await guardian.notify_session_start(
        agent="Scout",
        session_id="sess_001",
        metadata={"task": "test"}
    )
    
    assert permission.allowed is True
    assert "sess_001" in guardian.active_sessions

@pytest.mark.asyncio
async def test_notify_session_start_not_certified(certs_dir):
    guardian = SupervisorGuardian(certificates_dir=str(certs_dir))
    
    with pytest.raises(AgentNotCertifiedError):
        await guardian.notify_session_start(
            agent="UnknownAgent",
            session_id="sess_002",
            metadata={}
        )

@pytest.mark.asyncio
async def test_notify_session_start_expired(certs_dir):
    create_cert(certs_dir, "OldAgent", expired=True)
    guardian = SupervisorGuardian(certificates_dir=str(certs_dir))
    
    with pytest.raises(CertificationExpiredError):
        await guardian.notify_session_start(
            agent="OldAgent",
            session_id="sess_003",
            metadata={}
        )

@pytest.mark.asyncio
async def test_notify_session_end(certs_dir):
    create_cert(certs_dir, "Scout")
    guardian = SupervisorGuardian(certificates_dir=str(certs_dir))
    
    await guardian.notify_session_start("Scout", "sess_004", {})
    
    output_path = Path("docs/journals/ReasoningPipe_Scout_sess_004.md")
    await guardian.notify_session_end("sess_004", output_path)
    
    assert "sess_004" not in guardian.active_sessions
    assert len(guardian.completed_sessions) == 1
    assert guardian.completed_sessions[0]["status"] == "completed"

@pytest.mark.asyncio
async def test_get_session_stats(certs_dir):
    create_cert(certs_dir, "Scout")
    guardian = SupervisorGuardian(certificates_dir=str(certs_dir))
    
    await guardian.notify_session_start("Scout", "sess_A", {})
    await guardian.notify_session_start("Scout", "sess_B", {})
    await guardian.notify_session_end("sess_A", Path("file1.md"))
    
    stats = guardian.get_session_stats("Scout")
    assert stats["Scout"]["active_sessions"] == 1
    assert stats["Scout"]["completed_total"] == 1
    assert "certification_expires" in stats["Scout"]
