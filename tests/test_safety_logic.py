import pytest
import sys
import os

# Add app directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.safety import validate_command, validate_syntax, scan_for_secrets, check

class TestSafetyMiddleware:
    @pytest.mark.parametrize("dangerous_cmd", [
        "rm -rf /",
        "shutdown -h now",
        "mkfs /dev/sda",
        "docker system prune -a"
    ])
    def test_banned_commands_blocking(self, dangerous_cmd):
        # Test that dangerous commands are blocked by validate_command
        result = validate_command(dangerous_cmd)
        assert result == False, f"Command '{dangerous_cmd}' should be blocked"

    def test_safe_commands_allowed(self):
        safe_commands = [
            "echo hello",
            "ls -la",
            "git status",
            "python -c 'print(1)'"
        ]
        for cmd in safe_commands:
            result = validate_command(cmd)
            assert result == True, f"Safe command '{cmd}' should be allowed"

    def test_syntax_validation_python_invalid(self):
        # Test Python syntax validation with invalid code
        invalid_python = "def x():\n    pass"  # Missing proper indentation after def
        result = validate_syntax("test.py", invalid_python)
        assert result == False, "Invalid Python syntax should fail validation"

    def test_syntax_validation_python_valid(self):
        # Test Python syntax validation with valid code
        valid_python = "def hello():\n    return 'world'"
        result = validate_syntax("test.py", valid_python)
        assert result == True, "Valid Python syntax should pass validation"

    def test_syntax_validation_json_invalid(self):
        # Test JSON syntax validation
        invalid_json = '{"key": "value",}'  # Trailing comma
        result = validate_syntax("test.json", invalid_json)
        assert result == False, "Invalid JSON should fail validation"

    def test_syntax_validation_json_valid(self):
        # Test JSON syntax validation
        valid_json = '{"key": "value"}'
        result = validate_syntax("test.json", valid_json)
        assert result == True, "Valid JSON should pass validation"

    def test_syntax_validation_yaml_invalid(self):
        # Test YAML syntax validation
        invalid_yaml = "key: value\n  nested: 1"  # Indentation error
        result = validate_syntax("test.yaml", invalid_yaml)
        assert result == False, "Invalid YAML should fail validation"

    def test_syntax_validation_yaml_valid(self):
        # Test YAML syntax validation
        valid_yaml = "key: value\nnested:\n  subkey: 1"
        result = validate_syntax("test.yaml", valid_yaml)
        assert result == True, "Valid YAML should pass validation"

    def test_secret_pattern_detection(self):
        test_cases = [
            "sk-abc123xyz789",  # OpenAI key pattern
            "AIza123456789",    # Google API key pattern
            "ghp_abcdef123456", # GitHub token pattern
        ]

        for secret in test_cases:
            result = scan_for_secrets(secret)
            assert result == True, f"Secret '{secret}' should be detected"

    def test_non_secret_content_allowed(self):
        safe_content = [
            "This is normal text",
            "config_value = 'hello'",
            "print('Hello world')"
        ]
        for content in safe_content:
            result = scan_for_secrets(content)
            assert result == False, f"Content '{content}' should not be flagged as secret"

    def test_self_preservation_protection(self):
        protected_files = [
            "safety.py",
            "app/safety.py",
            "container.py",
            "app/container.py"
        ]

        for filepath in protected_files:
            result = check(filepath=filepath, content="some content")
            assert result == False, f"Writing to protected file '{filepath}' should be blocked"

    def test_unified_check_function(self):
        # Test the unified check function with various scenarios

        # Safe command should pass
        assert check(command="echo hello") == True

        # Dangerous command should fail
        assert check(command="rm -rf /") == False

        # Content with secrets should fail
        assert check(content="API_KEY=sk-abc123") == False

        # Valid content should pass
        assert check(content="Hello world", filepath="test.txt") == True

        # Python with dangerous import should fail
        dangerous_python = "import subprocess\nsubprocess.call('rm -rf /')"
        assert check(content=dangerous_python, filepath="test.py") == False
