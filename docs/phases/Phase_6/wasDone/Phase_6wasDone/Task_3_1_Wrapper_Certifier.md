# Task 3.1: Wrapper Certifier (Static + Dynamic Validation)

**File**: `app/services/supervisor/certifier.py`

## Requirements
- [x] Create `WrapperCertifier` class
- [x] Implement `async def certify_wrapper(wrapper_path: str, agent_name: str) -> CertificationResult`
    - [x] Run logic: Static Analysis → Dynamic Test → Output Validation → Issue Cert
- [x] Implement `def _static_analysis(wrapper_path: str) -> AnalysisResult`
    - [x] Check base class inheritance
    - [x] Check required method definitions
- [x] Implement `async def _dynamic_test(wrapper_path: str, agent_name: str) -> TestResult`
    - [x] Import module dynamically
    - [x] Instantiate wrapper with test session ID
    - [x] Execute test task and catch exceptions
- [x] Implement `def _validate_output(pipe_file: Path) -> ValidationResult`
    - [x] Check file existence
    - [x] Validate markdown structure (Header, Metadata, Stream sections)
- [x] Implement `def _issue_certificate(agent_name: str, wrapper_path: str) -> Certificate`
    - [x] Calculate SHA-256 hash of wrapper file
    - [x] Create JSON certificate with issuance/expiry dates
    - [x] Save to `app/.certificates/`

## CLI Interface
- [x] Implement `argparse` CLI
- [x] Support `--certify <path> --agent-name <name>`
- [x] Support `--list` command to show existing certs

## Test Coverage
- [x] Test static analysis failures (missing imports/methods)
- [x] Test dynamic test success/failure
- [x] Test output validation logic
- [x] Test certificate file creation
