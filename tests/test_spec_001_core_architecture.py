"""
Test Suite for 001_CORE_ARCHITECTURE.md
Validates: IoC Container, Driver Patterns, Reflex System

Following TDD Protocol (005_DEVELOPMENT_PROTOCOLS.md)
"""

import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.container import container
from app.config import config


class TestDriverPattern:
    """
    Tests for Section 1: THE DRIVER PATTERN
    Validates driver interface standardization
    """
    
    def test_l1_driver_exists(self):
        """Verify L1 driver is initialized via container"""
        assert container.l1_driver is not None, "L1 driver should be initialized"
    
    def test_l1_driver_config_injection(self):
        """Verify L1 uses Config Object Injection pattern"""
        # L1 should have access to config-based settings
        assert hasattr(container.l1_driver, 'model_name'), "L1 should have model_name from config"
        assert hasattr(container.l1_driver, 'api_url'), "L1 should have api_url from config"
    
    def test_l2_driver_exists(self):
        """Verify L2 driver is initialized via container"""
        assert container.l2_driver is not None, "L2 driver should be initialized"
    
    def test_l2_driver_explicit_injection(self):
        """Verify L2 uses Explicit Constructor Injection pattern"""
        # L2 should have explicit parameters
        assert hasattr(container.l2_driver, 'api_key'), "L2 should have explicit api_key"
        assert hasattr(container.l2_driver, 'model_name'), "L2 should have explicit model_name"


    @pytest.mark.asyncio
    async def test_driver_interface_consistency(self):
        """Verify all drivers implement consistent generate() interface"""
        # Both drivers should have generate method
        assert callable(getattr(container.l1_driver, 'generate', None)), \
            "L1 should implement generate()"
        assert callable(getattr(container.l2_driver, 'generate', None)), \
            "L2 should implement generate()"


class TestContainer:
    """
    Tests for Section 2: THE CONTAINER
    Validates IoC (Inversion of Control) root functionality
    """
    
    def test_container_is_singleton(self):
        """Verify container follows singleton pattern"""
        from app.container import container as container2
        assert container is container2, "Container should be singleton"
    
    def test_container_has_drivers(self):
        """Verify container manages all driver instances"""
        assert hasattr(container, 'l1_driver'), "Container should manage L1 driver"
        assert hasattr(container, 'l2_driver'), "Container should manage L2 driver"
    
    def test_container_has_memory_components(self):
        """Verify container manages memory and ingestor"""
        # These may be None in DEV mode, so check attribute exists
        assert hasattr(container, 'memory'), "Container should manage VectorStore"
        assert hasattr(container, 'ingestor'), "Container should manage Ingestor"
    
    def test_container_mode_management(self):
        """Verify container tracks system mode"""
        assert hasattr(container, 'current_mode'), "Container should track current_mode"
        assert container.current_mode in [config.MODE_RAG, config.MODE_DEV], \
            "Mode should be RAG or DEV"


class TestReflexSystem:
    """
    Tests for Section 3: THE REFLEX SYSTEM
    Validates XML parsing and safety integration
    """
    
    def test_reflex_module_exists(self):
        """Verify reflex module is importable"""
        try:
            from app import reflex
            assert reflex is not None
        except ImportError:
            pytest.fail("app.reflex should be importable")
    
    def test_safety_module_exists(self):
        """Verify safety (gatekeeper) module exists"""
        try:
            from app import safety
            assert safety is not None
        except ImportError:
            pytest.fail("app.safety should be importable")
    
    def test_reflex_functions_exist(self):
        """Verify reflex provides required action functions"""
        from app import reflex
        
        assert callable(getattr(reflex, 'execute_shell', None)), \
            "Reflex should provide execute_shell()"
        assert callable(getattr(reflex, 'write_file', None)), \
            "Reflex should provide write_file()"
        assert callable(getattr(reflex, 'execute_git_sync', None)), \
            "Reflex should provide execute_git_sync()"


class TestArchitecturalCompliance:
    """
    Meta-tests validating adherence to architectural principles
    """
    
    def test_no_direct_driver_instantiation_in_router(self):
        """Rule: router.py MUST NEVER instantiate drivers directly"""
        with open('app/router.py', 'r') as f:
            router_code = f.read()
        
        # Check that router imports container, not drivers
        assert 'from .container import container' in router_code, \
            "Router should import container"
        
        # Should NOT instantiate drivers
        assert 'LocalLlamaDriver(' not in router_code, \
            "Router should not directly instantiate LocalLlamaDriver"
        assert 'DeepInfraDriver(' not in router_code, \
            "Router should not directly instantiate DeepInfraDriver"
    
    def test_container_manages_dependencies(self):
        """Verify container is the IoC root"""
        # Container should initialize all major components
        assert container.l1_driver is not None
        assert container.l2_driver is not None
        # Storage and telemetry should be managed
        assert hasattr(container, 'storage')
        assert hasattr(container, 'telemetry')


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
