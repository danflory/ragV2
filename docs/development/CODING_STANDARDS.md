# Gravitas Coding Standards & Best Practices

This document defines coding standards and policies to prevent common bugs and ensure code quality across the Gravitas codebase.

---

## Table of Contents
1. [Datetime Handling](#datetime-handling)
2. [Error Handling](#error-handling)
3. [Type Hints](#type-hints)
4. [Async/Await Patterns](#asyncawait-patterns)

---

## 1. Datetime Handling

### Policy: Always Use Timezone-Aware Datetimes

**Rationale**: Mixing timezone-aware and timezone-naive datetimes causes `TypeError: can't compare offset-naive and offset-aware datetimes`.

### ✅ DO: Use timezone-aware datetimes consistently

```python
from datetime import datetime, timezone
import pytz

# Option 1: UTC timezone (recommended for storage)
now = datetime.now(timezone.utc)
expires_at = datetime(2026, 12, 31, 23, 59, 59, tzinfo=timezone.utc)

# Option 2: Specific timezone
pacific = pytz.timezone('America/Los_Angeles')
now = datetime.now(pacific)

# Option 3: Match existing datetime's timezone
cert_time = cert.expires_at  # May or may not have timezone
now = datetime.now(cert_time.tzinfo) if cert_time.tzinfo else datetime.now()
```

### ❌ DON'T: Mix timezone-aware and naive datetimes

```python
# BAD: Will crash if cert.expires_at has timezone
now = datetime.now()  # Naive (no timezone)
if now > cert.expires_at:  # Crashes if cert.expires_at is timezone-aware
    raise CertificationExpiredError()

# BAD: Inconsistent timezone handling
issued_at = datetime.now()  # Naive
expires_at = datetime.now(timezone.utc)  # Aware
# Storing both will cause comparison issues later
```

### Best Practices

1. **Storage**: Always store datetimes as UTC in databases
   ```python
   # Write to DB
   db.execute("INSERT INTO events (created_at) VALUES (?)", 
              (datetime.now(timezone.utc),))
   
   # Read from DB and make timezone-aware
   created_at = row['created_at']
   if created_at.tzinfo is None:
       created_at = created_at.replace(tzinfo=timezone.utc)
   ```

2. **API Responses**: Use ISO 8601 format with timezone
   ```python
   # FastAPI response
   return {
       "timestamp": datetime.now(timezone.utc).isoformat()
       # Output: "2026-01-07T23:58:22+00:00"
   }
   ```

3. **Comparisons**: Ensure both sides have matching timezone awareness
   ```python
   def is_expired(expires_at: datetime) -> bool:
       """Check if certificate has expired"""
       # Match the timezone of the input datetime
       now = datetime.now(expires_at.tzinfo) if expires_at.tzinfo else datetime.now()
       return now > expires_at
   ```

4. **Dataclass/Pydantic Models**: Specify timezone in type hints
   ```python
   from pydantic import BaseModel, Field
   from datetime import datetime
   
   class Certificate(BaseModel):
       issued_at: datetime = Field(..., description="UTC timestamp")
       expires_at: datetime = Field(..., description="UTC timestamp")
       
       class Config:
           # Ensure all datetimes are serialized with timezone
           json_encoders = {
               datetime: lambda v: v.isoformat()
           }
   ```

### Common Bugs & Fixes

| Bug | Fix |
|-----|-----|
| `TypeError: can't compare offset-naive and offset-aware` | Use `datetime.now(tzinfo)` instead of `datetime.now()` |
| Certificate appears expired when it's not | Ensure both datetimes use same timezone (UTC recommended) |
| JSON serialization loses timezone | Use `.isoformat()` instead of `str()` |
| Database timestamp has no timezone | Add `tzinfo=timezone.utc` when reading from DB |

---

## 2. Error Handling

### Policy: Use Specific Exception Types

**Rationale**: Generic exceptions make debugging harder and prevent proper error recovery.

### ✅ DO: Define custom exceptions for domain errors

```python
class AgentNotCertifiedError(Exception):
    """Raised when an agent is not certified."""
    pass

class CertificationExpiredError(Exception):
    """Raised when an agent's certification has expired."""
    pass

# Usage
if agent not in self.certified_agents:
    raise AgentNotCertifiedError(f"Agent '{agent}' lacks a valid certificate")
```

### ❌ DON'T: Use generic exceptions

```python
# BAD: Too generic, hard to catch specific failures
if agent not in self.certified_agents:
    raise Exception("Agent not certified")  # Don't do this
```

### Best Practices

1. **HTTP Endpoints**: Map exceptions to HTTP status codes
   ```python
   @app.post("/validate")
   async def validate_certificate(req: ValidateCertificateRequest):
       try:
           # Business logic
           return {"valid": True}
       except AgentNotCertifiedError as e:
           raise HTTPException(status_code=403, detail=str(e))
       except CertificationExpiredError as e:
           raise HTTPException(status_code=403, detail=str(e))
       except Exception as e:
           logger.error(f"Unexpected error: {e}")
           raise HTTPException(status_code=500, detail="Internal server error")
   ```

2. **Logging**: Always log exceptions with context
   ```python
   try:
       result = process_data()
   except ValueError as e:
       logger.error(f"Invalid data format: {e}", exc_info=True)
       raise
   ```

---

## 3. Type Hints

### Policy: Use Type Hints for All Public Functions

**Rationale**: Type hints improve code clarity, enable better IDE support, and catch bugs early.

### ✅ DO: Annotate function signatures

```python
from typing import Dict, List, Optional
from datetime import datetime

def get_session_stats(self, agent: Optional[str] = None) -> Dict[str, any]:
    """Get session statistics for monitoring."""
    stats: Dict[str, dict] = {}
    # ...
    return stats

async def notify_session_start(
    self, 
    agent: str, 
    session_id: str,
    metadata: dict
) -> SessionPermission:
    """Notify Guardian of session start."""
    # ...
    return SessionPermission(allowed=True)
```

### ❌ DON'T: Skip type hints on public APIs

```python
# BAD: No type hints, unclear what types are expected
def process_data(data, options):  # What types?
    return result  # What type is returned?
```

---

## 4. Async/Await Patterns

### Policy: Don't Mix Sync and Async Code Incorrectly

**Rationale**: Mixing sync/async incorrectly causes runtime errors or blocks the event loop.

### ✅ DO: Use async/await consistently

```python
# Async function calling async dependency
async def process_chat(self, request: ChatRequest):
    permission = await self.guardian.notify_session_start(...)  # Await async call
    result = await wrapper.execute_task(task)  # Await async call
    return result

# HTTP client should be async
class GuardianClient:
    async def validate_certificate(self, agent: str) -> bool:
        resp = await self.client.post(...)  # Await HTTP call
        return resp.json()
```

### ❌ DON'T: Forget to await async calls

```python
# BAD: Forgot to await - returns coroutine, not result
async def process_chat(self):
    permission = self.guardian.notify_session_start(...)  # Missing 'await'
    # permission is now a coroutine object, not SessionPermission!
```

---

## Enforcement

### Pre-Commit Checks

1. **Type Checking**: Run `mypy` on all Python files
   ```bash
   mypy app/ --strict
   ```

2. **Linting**: Run `ruff` to catch common issues
   ```bash
   ruff check app/ --fix
   ```

3. **Formatting**: Use `black` for consistent code style
   ```bash
   black app/
   ```

### Code Review Checklist

- [ ] All datetime comparisons use timezone-aware datetimes
- [ ] Custom exceptions defined for domain-specific errors
- [ ] Type hints present on all public functions
- [ ] Async functions properly await async calls
- [ ] Error handling includes logging with context
- [ ] Database timestamps stored as UTC

---

## Resources

- [Python datetime documentation](https://docs.python.org/3/library/datetime.html)
- [PEP 484 - Type Hints](https://peps.python.org/pep-0484/)
- [FastAPI Best Practices](https://fastapi.tiangolo.com/tutorial/)
- [Async Python Best Practices](https://docs.python.org/3/library/asyncio.html)

---

**Last Updated**: 2026-01-07  
**Maintained By**: Gravitas Development Team
