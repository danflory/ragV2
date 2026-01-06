import asyncio
import pytest
from app.services.scheduler.lock import ModelLock

@pytest.mark.asyncio
async def test_model_lock_tracking():
    lock = ModelLock()
    
    # Initially no model is hot
    assert lock.current_model is None
    assert lock.needs_switch("gemma2") is False
    
    # Set gemma2 as hot
    await lock.set_model("gemma2")
    assert lock.current_model == "gemma2"
    
    # Requesting gemma2 again should not need switch
    assert lock.needs_switch("gemma2") is False
    
    # Requesting llama3 should need a switch
    assert lock.needs_switch("llama3") is True
    
    # Switch to llama3
    await lock.set_model("llama3")
    assert lock.current_model == "llama3"
    assert lock.needs_switch("gemma2") is True
    
    # Clear lock
    await lock.clear()
    assert lock.current_model is None
