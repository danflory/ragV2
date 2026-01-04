import os
import pytest
from app.governance.inspector import inspector

def test_audit_receipt_pass(tmp_path):
    """
    Verifies that a valid receipt passes the audit.
    """
    receipt_file = tmp_path / "completed_phase_test.md"
    receipt_file.write_text("""
# PHASE TEST RECEIPT
## 2. TEST RESULTS
`pytest` output:
tests/test_foo.py PASSED [100%]
=========================== 1 passed in 0.1s ===========================
""")
    
    success, message = inspector.audit_receipt(str(receipt_file))
    assert success is True
    assert "PASS" in message

def test_audit_receipt_fail_missing_section(tmp_path):
    """
    Verifies that missing TEST RESULTS section fails.
    """
    receipt_file = tmp_path / "invalid_receipt.md"
    receipt_file.write_text("# NO TESTS HERE\nJust some text.")
    
    success, message = inspector.audit_receipt(str(receipt_file))
    assert success is False
    assert "section is missing" in message

def test_audit_receipt_fail_on_errors(tmp_path):
    """
    Verifies that present FAILED or ERROR tokens cause failure.
    """
    receipt_file = tmp_path / "failed_receipt.md"
    receipt_file.write_text("""
# PHASE TEST RECEIPT
## 2. TEST RESULTS
tests/test_foo.py FAILED [100%]
=========================== 1 failed in 0.1s ===========================
""")
    
    success, message = inspector.audit_receipt(str(receipt_file))
    assert success is False
    assert "FAILED or ERROR" in message

def test_audit_receipt_fail_no_confirmation(tmp_path):
    """
    Verifies that absence of PASSED fails if no errors are present either.
    """
    receipt_file = tmp_path / "neutral_receipt.md"
    receipt_file.write_text("""
# PHASE TEST RECEIPT
## 2. TEST RESULTS
Just some random logs without keywords.
""")
    
    success, message = inspector.audit_receipt(str(receipt_file))
    assert success is False
    assert "No explicit PASS/PASSED confirmation" in message
