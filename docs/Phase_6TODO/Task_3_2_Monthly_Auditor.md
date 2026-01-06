# Task 3.2: Monthly Auditor

**File**: `app/services/supervisor/auditor.py`

## Requirements
- [x] Create `ReasoningPipeAuditor` class
- [x] Implement `async def monthly_audit() -> AuditReport`
    - [x] List all certified agents
    - [x] Scan ReasoningPipe files from last 30 days
    - [x] Score quality for each agent
    - [x] Flag low-scoring agents
- [x] Implement `def _audit_quality(pipe_files: List[Path]) -> QualityScore`
    - [x] Score Format Compliance (40 pts)
    - [x] Score Completeness (30 pts)
    - [x] Score Efficiency (20 pts)
    - [x] Score Cost Accuracy (10 pts)
- [x] Implement `async def _flag_for_recertification(agent: str, reason: str)`
    - [x] Update certificate status to "pending_review"
    - [x] Add audit flag reason to certificate JSON

## CLI Interface
- [x] Add CLI block to trigger manual audit

## Test Coverage
- [x] Test quality scoring logic
- [x] Test flagging low-quality agents
- [x] Test audit report generation
