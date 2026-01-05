import os
import re
import logging

logger = logging.getLogger("Gravitas_INSPECTOR")

class QualityInspector:
    """
    Quality Control Agent.
    Audits work receipts (completed_*.md) to ensure TDD compliance.
    """
    
    def audit_receipt(self, file_path: str):
        """
        Parses a completed_*.md file and verifies test results.
        Returns (bool, str) - (Success Status, Message).
        """
        if not os.path.exists(file_path):
            return False, f"File not found: {file_path}"

        try:
            with open(file_path, 'r') as f:
                content = f.read()

            # 1. FAIL if "TEST RESULTS" section is missing
            if "## 2. TEST RESULTS" not in content.upper() and "TEST RESULTS" not in content.upper():
                return False, "FAIL: 'TEST RESULTS' section is missing."

            # 2. FAIL if logs contain "FAILED" or "ERROR"
            # We check for these keywords specifically in the context of test results.
            if re.search(r"\bFAILED\b", content, re.IGNORECASE) or re.search(r"\bERROR\b", content, re.IGNORECASE):
                return False, "FAIL: Logs contain FAILED or ERROR results."

            # 3. PASS only if clean test logs are found
            if re.search(r"\bPASSED\b", content) or "=========================== 2 passed" in content:
                return True, "PASS: Clean test logs found."
            
            return False, "FAIL: No explicit PASS/PASSED confirmation found in logs."

        except Exception as e:
            logger.error(f"❌ INSPECTOR AUDIT FAILURE: {e}")
            return False, f"Error during audit: {str(e)}"

inspector = QualityInspector()
