# Task 4.1: Specification Tests

**File**: `tests/test_spec_008_reasoning_pipes.py`

## Requirements
- [x] Implement `TestReasoningPipeClass`
    - [x] `test_init_creates_proper_paths()`
    - [x] `test_log_thought_adds_to_buffer()`
    - [x] `test_log_action_formats_details()`
    - [x] `test_log_result_stores_metrics()`
    - [x] `test_finalize_writes_file()`
    - [x] `test_finalize_creates_directory_if_missing()`
    - [x] `test_double_finalize_warning()`
- [x] Implement `TestSupervisorGuardian`
    - [x] `test_load_certificates_from_directory()`
    - [x] `test_notify_session_start_with_valid_cert()`
    - [x] `test_notify_session_start_rejects_uncertified()`
    - [x] `test_notify_session_start_rejects_expired()`
    - [x] `test_notify_session_end_updates_status()`
    - [x] `test_get_session_stats_aggregation()`
- [x] Implement `TestBaseWrapper`
    - [x] `test_execute_task_calls_supervisor()`
    - [x] `test_execute_task_enforces_certification()`
    - [x] `test_abstract_methods_must_be_implemented()`
- [x] Implement `TestWrapperCertifier`
    - [x] `test_static_analysis_detects_missing_imports()`
    - [x] `test_static_analysis_detects_inheritance()`
    - [x] `test_dynamic_test_runs_wrapper()`
    - [x] `test_output_validation_checks_format()`
    - [x] `test_issue_certificate_creates_file()`
- [x] Implement `TestReasoningPipeAuditor`
    - [x] `test_audit_quality_scoring()`
    - [x] `test_flag_for_recertification()`

## Execution
- [x] Run via `pytest tests/test_spec_008_reasoning_pipes.py -v`

