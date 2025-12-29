import pytest
from app.interfaces import LLMDriver
from app.L1_local import L1Driver

def test_driver_contract_adherence():
    """
    Checks if L1Driver follows the new SOLID Interface.
    """
    # FIX: We must now provide args to satisfy the strict constructor
    driver = L1Driver(base_url="http://dummy", model_name="dummy-model")
    
    assert isinstance(driver, LLMDriver), "L1Driver does not adhere to the LLMDriver interface!"

def test_dependency_injection_structure():
    """
    Checks if L1Driver accepts configuration via constructor (IoC).
    """
    fake_url = "http://fake-url:1234"
    fake_model = "fake-model"
    
    # This should now succeed without TypeError
    driver = L1Driver(base_url=fake_url, model_name=fake_model)
    
    # Verify it actually used the args
    assert driver.base_url == fake_url.rstrip("/")
    assert driver.model == fake_model