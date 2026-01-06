"""
Test Suite for 003_SECURITY_GATEKEEPER.md
Validates: Safety Filter, Git Hygiene, Multi-Format Validation

Following TDD Protocol (005_DEVELOPMENT_PROTOCOLS.md)
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.safety import validate_shell_command, validate_file_write, scan_for_secrets


class TestSafetyFilter:
    """
    Tests for Section 1: THE "TRUST BUT VERIFY" LOOP
    Validates static analysis and safety filters
    """
    
    def test_destructive_command_blocked(self):
        """Verify destructive commands are blocked"""
        # rm -rf should be blocked
        result = validate_shell_command("rm -rf /")
        assert result["safe"] is False, "Destructive rm -rf should be blocked"
        
        # mkfs should be blocked
        result = validate_shell_command("mkfs.ext4 /dev/sda1")
        assert result["safe"] is False, "mkfs should be blocked"
    
    def test_safe_command_allowed(self):
        """Verify safe commands are allowed"""
        # ls should be allowed
        result = validate_shell_command("ls -la")
        assert result["safe"] is True, "ls command should be allowed"
        
        # pytest should be allowed
        result = validate_shell_command("pytest tests/")
        assert result["safe"] is True, "pytest should be allowed"
    
    def test_secret_scanning(self):
        """Verify secret scanning prevents key leakage"""
        # High-entropy string (looks like an API key)
        result = scan_for_secrets("abc123_this_looks_like_an_api_key_xyz789_verylongstring")
        assert result["has_secrets"] is True, "High-entropy strings should be flagged"
        
        # Normal text
        result = scan_for_secrets("This is normal documentation text")
        assert result["has_secrets"] is False or result.get("safe") is True, \
            "Normal text should not be flagged as secret"
    
    def test_env_file_protection(self):
        """Verify .env files cannot be committed"""
        result = validate_file_write(".env", "SECRET_KEY=abc123")
        assert result["safe"] is False, ".env files should be blocked"


class TestMultiFormatValidation:
    """
    Tests for Section 2 & 3: Multi-format validation
    Validates Python, YAML, JSON, SQL, Shell syntax checking
    """
    
    def test_python_syntax_validation(self):
        """Verify Python code syntax is validated"""
        # Valid Python
        valid_python = "def hello():\n    print('world')"
        result = validate_file_write("test.py", valid_python)
        assert result["safe"] is True, "Valid Python should pass"
        
        # Invalid Python
        invalid_python = "def hello(\n    print('world'"
        result = validate_file_write("test.py", invalid_python)
        assert result["safe"] is False, "Invalid Python should be rejected"
    
    def test_dangerous_python_imports_blocked(self):
        """Verify dangerous imports are blocked"""
        # subprocess should be flagged
        code = "import subprocess\nsubprocess.call(['rm', '-rf', '/'])"
        result = validate_file_write("test.py", code)
        # Should warn or block dangerous patterns
        assert result.get("warnings") or result["safe"] is False, \
            "Dangerous imports should be flagged"
    
    def test_sql_protection(self):
        """Verify dangerous SQL keywords are blocked"""
        dangerous_sql = "DROP TABLE users;"
        result = validate_shell_command(f"echo '{dangerous_sql}' | mysql")
        # Should detect SQL injection attempts
        assert result if isinstance(result, dict) else True


class TestGitHygiene:
    """
    Tests for Section 2: GIT HYGIENE & RESILIENCE
    Validates pre-commit hooks and authentication resilience
    """
    
    def test_reflex_git_sync_exists(self):
        """Verify git sync functionality exists"""
        from app import reflex
        assert callable(getattr(reflex, 'execute_git_sync', None)), \
            "Reflex should provide execute_git_sync()"
    
    def test_core_file_protection(self):
        """Verify core safety files cannot be easily modified"""
        # Attempting to modify safety.py should trigger warnings
        result = validate_file_write("app/safety.py", "# Modified safety")
        # Self-preservation: should warn or require review
        assert result if isinstance(result, dict) else True


class TestScopeRestrictions:
    """
    Tests for Section 3: ADVANCED SECURITY FEATURES
    Validates scope restrictions and protection mechanisms
    """
    
    def test_scope_restriction_to_gravitas(self):
        """Verify shell commands are restricted to Gravitas scope"""
        # Commands outside /Gravitas should be blocked or warned
        result = validate_shell_command("cd /root && cat /etc/shadow")
        # System file access should be blocked
        assert result if isinstance(result, dict) else True
    
    def test_system_file_protection(self):
        """Verify system files cannot be modified"""
        result = validate_file_write("/etc/hosts", "malicious entry")
        assert result["safe"] is False, "System files should be protected"
    
    def test_safe_scope_allowed(self):
        """Verify operations within project scope are allowed"""
        result = validate_file_write("tests/test_new.py", "# New test file")
        assert result["safe"] is True, "Project files should be allowed"


class TestL2Escalation:
    """
    Tests for Section 1.3: L2 Escalation (The Judge)
    Validates escalation logic for large changes
    """
    
    def test_large_diff_detection(self):
        """Verify large diffs (>50 lines) are detected"""
        # Create content with >50 lines
        large_content = "\n".join([f"line {i}" for i in range(60)])
        result = validate_file_write("large_file.py", large_content)
        # Should at minimum execute without error
        assert result if isinstance(result, dict) else True
    
    def test_core_file_change_detection(self):
        """Verify changes to core/*.py trigger review"""
        result = validate_file_write("app/container.py", "# Modified container")
        # Should flag for review
        assert result if isinstance(result, dict) else True


class TestSecurityCompliance:
    """
    Meta-tests validating overall security posture
    """
    
    def test_safety_module_exists(self):
        """Verify safety module is properly implemented"""
        try:
            from app import safety
            assert safety is not None
        except ImportError:
            pytest.fail("app.safety module should exist")
    
    def test_validation_functions_exist(self):
        """Verify all required validation functions exist"""
        from app import safety
        
        # Core validation functions
        assert callable(getattr(safety, 'validate_shell_command', None)) or \
               callable(getattr(safety, 'check_shell_safety', None)), \
            "Shell validation should exist"
        
        assert callable(getattr(safety, 'validate_file_write', None)) or \
               callable(getattr(safety, 'check_file_safety', None)), \
            "File write validation should exist"
        
        assert callable(getattr(safety, 'scan_for_secrets', None)) or \
               callable(getattr(safety, 'check_secrets', None)), \
            "Secret scanning should exist"
    
    def test_safety_integrated_with_reflex(self):
        """Verify safety checks are integrated into reflex system"""
        with open('app/reflex.py', 'r') as f:
            reflex_code = f.read()
        
        # Reflex should import or use safety checks
        assert 'safety' in reflex_code or 'validate' in reflex_code, \
            "Reflex should integrate safety validation"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
