import argparse
import asyncio
import hashlib
import importlib
import importlib.util
import inspect
import json
import logging
import os
import sys
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List, Dict

from app.services.supervisor.guardian import Certificate, SupervisorGuardian
from app.wrappers.base_wrapper import GravitasAgentWrapper

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

@dataclass
class AnalysisResult:
    passed: bool
    errors: List[str]

@dataclass
class TestResult:
    passed: bool
    error: Optional[str] = None
    pipe_file: Optional[Path] = None

@dataclass
class ValidationResult:
    passed: bool
    errors: List[str]

@dataclass
class CertificationResult:
    passed: bool
    agent_name: str
    wrapper_path: str
    analysis: AnalysisResult
    test: TestResult
    validation: ValidationResult
    certificate: Optional[Certificate] = None

class WrapperCertifier:
    """
    Pre-deployment validation of agent wrappers.
    """

    def __init__(self, certificates_dir: str = "app/.certificates"):
        self.certificates_dir = Path(certificates_dir)
        self.certificates_dir.mkdir(parents=True, exist_ok=True)
        self.guardian = SupervisorGuardian(certificates_dir=str(self.certificates_dir))

    async def certify_wrapper(self, wrapper_path: str, agent_name: str) -> CertificationResult:
        """
        Full certification pipeline.
        """
        logger.info(f"Starting certification for {agent_name} at {wrapper_path}")
        
        # 1. Static Analysis
        analysis = self._static_analysis(wrapper_path)
        if not analysis.passed:
            return CertificationResult(False, agent_name, wrapper_path, analysis, TestResult(False), ValidationResult(False, ["Static analysis failed"]))

        # 2. Dynamic Testing
        test = await self._dynamic_test(wrapper_path, agent_name)
        if not test.passed:
            return CertificationResult(False, agent_name, wrapper_path, analysis, test, ValidationResult(False, ["Dynamic test failed"]))

        # 3. Output Validation
        validation = self._validate_output(test.pipe_file)
        if not validation.passed:
            return CertificationResult(False, agent_name, wrapper_path, analysis, test, validation)

        # 4. Certificate Issuance
        cert = self._issue_certificate(agent_name, wrapper_path)
        
        logger.info(f"Certification successful for {agent_name}")
        return CertificationResult(True, agent_name, wrapper_path, analysis, test, validation, cert)

    def _static_analysis(self, wrapper_path: str) -> AnalysisResult:
        """
        Checks code structure without executing it.
        """
        errors = []
        path = Path(wrapper_path)
        if not path.exists():
            return AnalysisResult(False, [f"File {wrapper_path} does not exist"])

        with open(path, "r") as f:
            content = f.read()

        # Check for necessary imports and inheritance
        if "from app.wrappers.base_wrapper import GravitasAgentWrapper" not in content:
            errors.append("Wrapper must import GravitasAgentWrapper from app.wrappers.base_wrapper")
        
        # We'll do more rigorous checks during dynamic import in _dynamic_test
        # But here we can check for required method signatures via simple text searching or AST
        # For simplicity in Phase 6.0, we'll rely on text checks + dynamic loading checks
        
        required_methods = ["_execute_internal", "_parse_thought", "_parse_action"]
        for method in required_methods:
            if f"def {method}" not in content:
                errors.append(f"Missing required method definition: {method}")

        if "super().__init__" not in content:
            errors.append("Wrapper __init__ must call super().__init__")

        return AnalysisResult(len(errors) == 0, errors)

    async def _dynamic_test(self, wrapper_path: str, agent_name: str) -> TestResult:
        """
        Imports and executes the wrapper with a test task.
        """
        try:
            # Load module
            module_name = f"dynamic_wrapper_{agent_name}"
            spec = importlib.util.spec_from_file_location(module_name, wrapper_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)

            # Find the class that inherits from GravitasAgentWrapper
            wrapper_class = None
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and issubclass(obj, GravitasAgentWrapper) and obj is not GravitasAgentWrapper:
                    wrapper_class = obj
                    break

            if not wrapper_class:
                return TestResult(False, "Could not find a class inheriting from GravitasAgentWrapper")

            # Instantiate wrapper
            # Note: The __init__ of wrappers might vary in arguments. 
            # Most examples use session_id and maybe model_name.
            # For testing, we'll try to instantiate with Minimal arguments or use inspection.
            
            sig = inspect.signature(wrapper_class.__init__)
            params = sig.parameters
            kwargs = {}
            if 'session_id' in params:
                kwargs['session_id'] = f"test_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Phase 6.0: Handle wrappers that require model_name
            if 'model_name' in params and params['model_name'].default == inspect.Parameter.empty:
                kwargs['model_name'] = "model-for-testing"
            
            try:
                instance = wrapper_class(**kwargs)
            except TypeError as e:
                # Try to see if we can instantiate with just session_id if it failed
                return TestResult(False, f"Failed to instantiate wrapper: {e}. Ensure __init__ accepts session_id or has defaults.")

            # Mock SupervisorGuardian to allow test session without a cert
            # Actually, the certifier IS the one who issues certs. 
            # We can mock the guardian.notify_session_start to always return allowed.
            from unittest.mock import patch, MagicMock, AsyncMock
            # Ensure the supervisor's session start is mocked to allow test session
            if not isinstance(instance.supervisor.notify_session_start, (MagicMock, AsyncMock)):
                instance.supervisor.notify_session_start = AsyncMock(return_value=type('Permission', (), {'allowed': True})())
            
            with patch.object(SupervisorGuardian, 'notify_session_start', return_value=asyncio.Future()):
                # If it's already a mock from previous step, we ensure it returns allowed
                if hasattr(instance.supervisor.notify_session_start, 'return_value'):
                    instance.supervisor.notify_session_start.return_value = type('Permission', (), {'allowed': True})()
                
                # Run a simple task
                task = {"prompt": "Summarize the word 'gravitas'"}
                # We need to make sure we don't actually call external APIs if possible, 
                # but the dynamic test should verify the wrapper works.
                # For Phase 6.0, if it's a real model wrapper, it MIGHT try to call the API.
                # In a real environment, DEEPINFRA_API_KEY etc should be set.
                
                try:
                    # Timeout to prevent hanging tests
                    await asyncio.wait_for(instance.execute_task(task), timeout=30.0)
                except asyncio.TimeoutError:
                    return TestResult(False, "Dynamic test timed out after 30 seconds")
                except Exception as e:
                    return TestResult(False, f"Error during task execution: {e}")

            # Check if pipe file was created
            pipe_file = instance.pipe.output_path
            if not pipe_file.exists():
                return TestResult(False, f"ReasoningPipe file not created at {pipe_file}")

            return TestResult(True, pipe_file=pipe_file)

        except Exception as e:
            logger.exception("Dynamic test failed with exception")
            return TestResult(False, str(e))

    def _validate_output(self, pipe_file: Path) -> ValidationResult:
        """
        Validates the markdown structure of the ReasoningPipe file.
        """
        errors = []
        if not pipe_file or not pipe_file.exists():
            return ValidationResult(False, ["Pipe file missing"])

        with open(pipe_file, "r") as f:
            content = f.read()

        # Basic Markdown Structure Checks
        if not content.startswith("# ReasoningPipe:"):
            errors.append("Missing H1 header 'ReasoningPipe:'")
        
        required_sections = [
            "**Started**:",
            "**Model**:",
            "**Tier**:",
            "**Task**:",
            "## Thought Stream",
            "## Session Metadata",
            "**Duration**:",
            "**Finalized**:"
        ]
        
        for section in required_sections:
            if section not in content:
                errors.append(f"Missing required metadata/section: {section}")

        # Check for at least one THOUGHT and RESULT
        if "THOUGHT:" not in content:
            errors.append("No 'THOUGHT:' entries found in Thought Stream")
        if "RESULT:" not in content:
            errors.append("No 'RESULT:' entry found in Thought Stream")

        return ValidationResult(len(errors) == 0, errors)

    def _issue_certificate(self, agent_name: str, wrapper_path: str) -> Certificate:
        """
        Issues a 30-day certificate for the validated wrapper.
        """
        with open(wrapper_path, "rb") as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()

        now = datetime.now()
        expires_at = now + timedelta(days=30)
        
        cert = Certificate(
            agent_name=agent_name,
            issued_at=now,
            expires_at=expires_at,
            signature=file_hash,
            version="1.0"
        )

        cert_file = self.certificates_dir / f"{agent_name}.json"
        
        # Convert to dict for saving
        cert_data = {
            "agent_name": cert.agent_name,
            "issued_at": cert.issued_at.isoformat(),
            "expires_at": cert.expires_at.isoformat(),
            "signature": cert.signature,
            "version": cert.version
        }
        
        with open(cert_file, "w") as f:
            json.dump(cert_data, f, indent=4)
            
        logger.info(f"Certificate issued and saved to {cert_file}")
        return cert

    def list_certificates(self) -> List[Dict]:
        """
        Lists all existing certificates.
        """
        certs = []
        if not self.certificates_dir.exists():
            return certs

        for cert_file in self.certificates_dir.glob("*.json"):
            try:
                with open(cert_file, "r") as f:
                    data = json.load(f)
                    certs.append(data)
            except Exception as e:
                logger.error(f"Error reading cert file {cert_file}: {e}")
        return certs

def main():
    parser = argparse.ArgumentParser(description="Gravitas Wrapper Certifier")
    parser.add_argument("--certify", type=str, help="Path to the wrapper file to certify")
    parser.add_argument("--agent-name", type=str, help="Name of the agent")
    parser.add_argument("--list", action="store_true", help="List all certified agents")
    parser.add_argument("--test-only", type=str, help="Run validation without issuing a certificate")

    args = parser.parse_args()
    certifier = WrapperCertifier()

    if args.list:
        certs = certifier.list_certificates()
        if not certs:
            print("No certified agents found.")
        else:
            print(f"{'Agent Name':<20} | {'Issued At':<25} | {'Expires At':<25}")
            print("-" * 75)
            for c in certs:
                print(f"{c['agent_name']:<20} | {c['issued_at']:<25} | {c['expires_at']:<25}")
        return

    if args.certify:
        if not args.agent_name:
            print("Error: --agent-name is required when using --certify")
            sys.exit(1)
        
        result = asyncio.run(certifier.certify_wrapper(args.certify, args.agent_name))
        if result.passed:
            print(f"SUCCESS: Agent '{args.agent_name}' has been certified.")
            print(f"Certificate: {certifier.certificates_dir}/{args.agent_name}.json")
        else:
            print(f"FAILURE: Certification failed for '{args.agent_name}'")
            if result.analysis.errors:
                print("\nStatic Analysis Errors:")
                for e in result.analysis.errors:
                    print(f" - {e}")
            if result.test.error:
                print(f"\nDynamic Test Error: {result.test.error}")
            if result.validation.errors:
                print("\nOutput Validation Errors:")
                for e in result.validation.errors:
                    print(f" - {e}")
        return

    if args.test_only:
        # Simplified test-only mode
        name = args.agent_name or "TestAgent"
        print(f"Running test-only validation for {args.test_only}...")
        
        analysis = certifier._static_analysis(args.test_only)
        print(f"Static Analysis: {'PASSED' if analysis.passed else 'FAILED'}")
        for e in analysis.errors: print(f"  - {e}")
        
        if analysis.passed:
            test = asyncio.run(certifier._dynamic_test(args.test_only, name))
            print(f"Dynamic Test: {'PASSED' if test.passed else 'FAILED'}")
            if test.error: print(f"  - {error}")
            
            if test.passed:
                val = certifier._validate_output(test.pipe_file)
                print(f"Output Validation: {'PASSED' if val.passed else 'FAILED'}")
                for e in val.errors: print(f"  - {e}")

    if not any([args.certify, args.list, args.test_only]):
        parser.print_help()

if __name__ == "__main__":
    main()
