# Task 1.2: Supervisor Guardian (Session Manager)

**File**: `app/services/supervisor/guardian.py`

## Requirements
- [x] Create `SupervisorGuardian` class
- [x] Implement `__init__()`
    - [x] Load certificates from `app/.certificates/` directory
    - [x] Initialize `active_sessions` dict
    - [x] Log startup message with certificate count
- [x] Implement `_load_certificates() -> Dict[str, Certificate]`
    - [x] Read all JSON files in `app/.certificates/`
    - [x] Parse certificate format: `{"agent_name": str, "issued_at": ISO8601, "expires_at": ISO8601, "signature": str}`
    - [x] Return dict mapping agent_name → Certificate
    - [x] Ensure directory existence
- [x] Implement `notify_session_start(agent: str, session_id: str, metadata: dict) -> SessionPermission`
    - [x] Check agent certification status
    - [x] Validate certificate expiration
    - [x] Add session to `active_sessions`
    - [x] Return `SessionPermission`
- [x] Implement `notify_session_end(session_id: str, output_file: Path) -> None`
    - [x] Update session status to "completed"
    - [x] Calculate and log session duration
- [x] Implement `get_session_stats(agent: Optional[str] = None) -> dict`
    - [x] Aggregate active and completed session counts
    - [x] Include certification expiration info

## Custom Exceptions
- [x] `AgentNotCertifiedError`
- [x] `CertificationExpiredError`

## Certificate Storage
- [x] Files at `app/.certificates/{agent_name}.json`
- [x] JSON format validation

## Test Coverage
- [x] Test certificate loading from directory
- [x] Test session_start with valid cert
- [x] Test session_start with missing cert (raise error)
- [x] Test session_start with expired cert (raise error)
- [x] Test session_end updates status correctly
- [x] Test get_session_stats aggregation
