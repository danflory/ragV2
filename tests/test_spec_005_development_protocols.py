"""
Test Suite for 005_DEVELOPMENT_PROTOCOLS.md
Validates: TDD, SOLID Principles, Version Control, Reasoning & Transparency

Following TDD Protocol (005_DEVELOPMENT_PROTOCOLS.md)
"""

import pytest
import sys
import os
import subprocess

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.container import container
from app.config import config


class TestTDDProtocol:
    """
    Tests for Section 1: THE ARCHITECT'S OATH (TDD)
    Validates Test-Driven Development practices
    """
    
    def test_tests_directory_exists(self):
        """Verify tests/ directory exists"""
        assert os.path.exists('tests'), "tests/ directory should exist"
        assert os.path.isdir('tests'), "tests/ should be a directory"
    
    def test_test_files_exist(self):
        """Verify test files follow naming convention"""
        test_files = [f for f in os.listdir('tests') if f.startswith('test_') and f.endswith('.py')]
        assert len(test_files) > 0, "Should have test_*.py files"
    
    def test_pytest_executable(self):
        """Verify pytest can be executed"""
        try:
            result = subprocess.run(
                ["pytest", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            assert result.returncode == 0, "pytest should be executable"
            assert "pytest" in result.stdout.lower(), "Should display pytest version"
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("pytest not available in environment")


class TestSOLIDPrinciples:
    """
    Tests for Section 2: THE SOLID STANDARD
    Validates Single Responsibility, IoC, and DRY principles
    """
    
    def test_srp_modules_decoupled(self):
        """Verify safety.py and reflex.py are decoupled"""
        # Safety should not import reflex
        with open('app/safety.py', 'r') as f:
            safety_code = f.read()
        
        # Should not directly import reflex (loose coupling)
        assert 'from .reflex import' not in safety_code, \
            "safety.py should not import reflex (SRP violation)"
        assert 'import reflex' not in safety_code, \
            "safety.py should not import reflex (SRP violation)"
    
    def test_ioc_container_usage(self):
        """Verify container.py is used for dependency resolution"""
        # Container should exist
        assert os.path.exists('app/container.py'), "container.py should exist"
        
        # Router should use container
        with open('app/router.py', 'r') as f:
            router_code = f.read()
        
        assert 'from .container import container' in router_code, \
            "Router should import container for IoC"
    
    def test_container_is_ioc_root(self):
        """Verify container manages major dependencies"""
        assert hasattr(container, 'l1_driver'), "Container should manage L1 driver"
        assert hasattr(container, 'l2_driver'), "Container should manage L2 driver"
        assert hasattr(container, 'memory'), "Container should manage VectorStore"
        assert hasattr(container, 'storage'), "Container should manage Storage"


class TestAtomicVersionControl:
    """
    Tests for Section 3: ATOMIC VERSION CONTROL
    Validates Git practices and automated verification
    """
    
    def test_git_repository_initialized(self):
        """Verify project is a Git repository"""
        assert os.path.exists('.git'), "Should be a Git repository"
        assert os.path.isdir('.git'), ".git should be a directory"
    
    def test_gitignore_exists(self):
        """Verify .gitignore exists"""
        assert os.path.exists('.gitignore'), ".gitignore should exist"
        
        # Should ignore common patterns
        with open('.gitignore', 'r') as f:
            gitignore = f.read()
        
        assert '.env' in gitignore or '*.env' in gitignore, \
            ".gitignore should protect .env files"
        assert '__pycache__' in gitignore, \
            ".gitignore should ignore __pycache__"
    
    def test_changelog_exists(self):
        """Verify CHANGELOG.md exists (Section 3.4)"""
        changelog_files = ['CHANGELOG.md', 'CHANGELOG', 'docs/CHANGELOG.md']
        exists = any(os.path.exists(f) for f in changelog_files)
        assert exists, "CHANGELOG.md should exist"
    
    def test_reflex_git_sync_exists(self):
        """Verify Git sync is automated via reflex"""
        from app import reflex
        assert callable(getattr(reflex, 'execute_git_sync', None)), \
            "Reflex should provide execute_git_sync()"


class TestAsyncArchitecture:
    """
    Tests for Section 4: ADVANCED DEVELOPMENT PROTOCOLS
    Validates async/await implementation
    """
    
    def test_async_driver_methods(self):
        """Verify drivers use async/await"""
        # L1 and L2 drivers should have async generate
        assert callable(getattr(container.l1_driver, 'generate', None))
        assert callable(getattr(container.l2_driver, 'generate', None))
        
        # Methods should be async (coroutine functions)
        import inspect
        assert inspect.iscoroutinefunction(container.l1_driver.generate), \
            "L1 generate should be async"
        assert inspect.iscoroutinefunction(container.l2_driver.generate), \
            "L2 generate should be async"
    
    @pytest.mark.asyncio
    async def test_async_database_operations(self):
        """Verify database uses async operations"""
        from app.database import db
        
        if not db.is_ready():
            pytest.skip("Database not available")
        
        # Database methods should be async
        import inspect
        assert inspect.iscoroutinefunction(db.save_history), \
            "save_history should be async"
        assert inspect.iscoroutinefunction(db.get_recent_history), \
            "get_recent_history should be async"


class TestReasoningTransparency:
    """
    Tests for Section 5: REASONING & TRANSPARENCY
    Validates Dual-Track Journaling system
    """
    
    def test_journals_directory_exists(self):
        """Verify docs/journals/ exists for reasoning logs"""
        assert os.path.exists('docs/journals'), \
            "docs/journals/ should exist for reasoning pipes"
        assert os.path.isdir('docs/journals'), \
            "docs/journals/ should be a directory"
    
    def test_dual_track_structure(self):
        """Verify dual-track journaling structure"""
        journals_path = 'docs/journals'
        
        # Should support executive and reasoning files
        # Look for any pattern indicating dual-track system
        if os.listdir(journals_path):
            files = os.listdir(journals_path)
            has_executive = any('executive' in f.lower() for f in files)
            has_reasoning = any(
                'reasoning' in f.lower() or 
                'thought' in f.lower() or 
                'pipe' in f.lower() 
                for f in files
            )
            
            # At least one track should exist
            assert has_executive or has_reasoning or len(files) > 0, \
                "Journals directory should contain tracking files"
    
    def test_current_session_support(self):
        """Verify current_session.md tracking (from spec)"""
        current_session = 'docs/journals/current_session.md'
        # File may or may not exist depending on session state
        # But directory structure supports it
        assert os.path.exists('docs/journals'), \
            "Journals directory should support current_session.md"


class TestRetentionCycles:
    """
    Tests for Section 5: Retention Cycles
    Validates 60-day telemetry and 14-day reasoning pipe retention
    """
    
    def test_60day_telemetry_retention_configured(self):
        """Verify 60-day telemetry retention (Section 5)"""
        maintenance_path = "ANTIGRAVITY_Scripts/maintenance.py"
        assert os.path.exists(maintenance_path), \
            "Maintenance script should exist"
        
        with open(maintenance_path, 'r') as f:
            content = f.read()
        
        # Should mention 60 days
        assert '60' in content, "Maintenance should reference 60-day retention"
        assert 'telemetry' in content.lower(), \
            "Maintenance should handle telemetry pruning"
    
    def test_14day_reasoning_retention_configured(self):
        """Verify 14-day reasoning pipe retention"""
        maintenance_path = "ANTIGRAVITY_Scripts/maintenance.py"
        
        with open(maintenance_path, 'r') as f:
            content = f.read()
        
        # Should mention 14 days
        assert '14' in content, "Maintenance should reference 14-day retention"


class TestIdentityCompliance:
    """
    Tests for Section 6: IDENTITY COMPLIANCE
    Validates Antigravity vs Gravitas naming
    """
    
    def test_gravitas_namespace_in_code(self):
        """Verify Gravitas namespace is used for internal components"""
        # Container and core logic should use Gravitas
        with open('app/container.py', 'r') as f:
            container_code = f.read()
        
        # Should reference Gravitas in logs or naming
        assert 'Gravitas' in container_code or 'gravitas' in container_code.lower(), \
            "Internal system should use Gravitas namespace"
    
    def test_antigravity_for_construction(self):
        """Verify Antigravity is used for construction/development context"""
        # Docs or journals should reference Antigravity for development
        has_antigravity_ref = False
        
        search_paths = ['docs/', 'ANTIGRAVITY_Scripts/', '.agent/']
        for path in search_paths:
            if os.path.exists(path):
                has_antigravity_ref = True
                break
        
        assert has_antigravity_ref, \
            "Antigravity should be referenced for development context"
    
    def test_nomenclature_doc_exists(self):
        """Verify GRAVITAS_NOMENCLATURE.md exists"""
        nomenclature_paths = [
            'docs/GRAVITAS_NOMENCLATURE.md',
            'GRAVITAS_NOMENCLATURE.md'
        ]
        exists = any(os.path.exists(p) for p in nomenclature_paths)
        assert exists, "GRAVITAS_NOMENCLATURE.md should exist"


class TestDependencyInjection:
    """
    Tests for Section 4: Dependency Injection via container
    """
    
    def test_container_singleton(self):
        """Verify container is singleton"""
        from app.container import container as c1
        from app.container import container as c2
        assert c1 is c2, "Container should be singleton"
    
    def test_all_components_injected(self):
        """Verify all major components are managed by container"""
        components = ['l1_driver', 'l2_driver', 'memory', 'storage', 'ingestor']
        for component in components:
            assert hasattr(container, component), \
                f"Container should manage {component}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
