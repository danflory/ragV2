# Incident Report: Missing Dependencies Causing Reset Failures
**Date:** 2026-01-08  
**Time:** 13:05:29 - 13:20:00 EST  
**Severity:** High  
**Status:** Resolved  

---

## Executive Summary

The Gravitas reset script failed multiple times due to missing Python dependencies in the virtual environment. The failures occurred progressively as each missing dependency was discovered during different stages of the startup process.

---

## Timeline of Failures

### Incident 1: PyYAML Missing (13:05:29)
**Component:** Gravitas Lobby (Port 5050)  
**Failed at:** uvicorn startup → logging configuration  

**Error:**
```python
File "/home/dflory/dev_env/Gravitas/venv/lib/python3.12/site-packages/uvicorn/config.py", line 378
    import yaml
ModuleNotFoundError: No module named 'yaml'
```

**Root Cause:**
- `pyyaml` package was not installed in venv
- Required by uvicorn's `--log-config log_conf.yaml` parameter
- Not listed in `requirements.txt`

**Resolution:**
- Manually installed: `pip install pyyaml`
- Added to `requirements.txt` (line 57)

---

### Incident 2: GPUtil Missing (13:15:19)
**Component:** Application module loading  
**Failed at:** Import of `app.L1_local`  

**Error:**
```python
File "/home/dflory/dev_env/Gravitas/app/L1_local.py", line 3
    import GPUtil
ModuleNotFoundError: No module named 'GPUtil'
```

**Root Cause:**
- `GPUtil` package was not installed in venv
- Already listed in `requirements.txt` (line 55: `gputil==1.4.0`)
- Virtual environment was missing multiple dependencies from requirements.txt

**Resolution:**
- Manually installed: `pip install GPUtil`
- Subsequently ran: `pip install -r requirements.txt` to install all missing dependencies

---

## Root Cause Analysis

### Primary Issue
The virtual environment was **not synchronized with requirements.txt**. Many packages listed in requirements were not actually installed in the venv.

### Contributing Factors
1. **No dependency validation** in reset script before attempting to start services
2. **Late failure** - errors only appeared when code tried to import missing modules
3. **Incomplete requirements.txt** - missing `pyyaml` despite being a critical dependency
4. **No automated setup verification** after venv creation

---

## Impact Assessment

- **User Impact:** Unable to start Gravitas services until dependencies manually installed
- **Time Lost:** ~15 minutes of troubleshooting and iterative fixes
- **Service Availability:** 0% during incident window
- **Data Loss:** None
- **Blast Radius:** Local development environment only

---

## Preventive Measures Implemented

### 1. Enhanced Preflight Checks
Updated `scripts/reset_gravitas.sh` to validate critical dependencies **before** attempting any service starts:

**Checks now include:**
- ✅ docker-compose availability
- ✅ Docker daemon running
- ✅ Virtual environment exists
- ✅ requirements.txt exists
- ✅ Critical Python modules installed (yaml, GPUtil, fastapi, uvicorn, httpx, ollama, asyncpg)

**Auto-remediation:**
- If dependencies missing, automatically runs `pip install -r requirements.txt`
- Logs incident to system logs for tracking
- Exits with clear error message if auto-fix fails

### 2. Updated requirements.txt
- Added `pyyaml>=6.0.0` to ensure uvicorn logging works

### 3. Improved Error Messages
- Clear indication of which dependencies are missing
- Suggested manual fix commands
- Automatic incident logging on failure

### 4. Bashrc Integration
Updated `.bashrc_gravitas` reset function to:
- Change to Gravitas directory automatically
- Validate PyYAML before invoking reset script
- Provide clear error messaging

---

## Testing Performed

- ✅ Validated preflight checks catch missing dependencies
- ✅ Confirmed auto-install works when dependencies missing
- ✅ Verified all critical modules now load successfully
- ✅ Reset script completes successfully with all checks passing

---

## Recommendations

### Short Term
1. ✅ **COMPLETED:** Add comprehensive dependency validation to reset script
2. ✅ **COMPLETED:** Update requirements.txt with missing dependencies
3. ✅ **COMPLETED:** Add auto-remediation for missing packages

### Long Term
1. **Create setup script** to validate fresh venv installations
2. **Add CI/CD check** to ensure requirements.txt completeness
3. **Document dependency refresh procedure** in README
4. **Consider using poetry or pipenv** for better dependency management
5. **Add health check endpoint** that validates all dependencies at runtime

---

## Lessons Learned

1. **Fail fast is better** - Check dependencies upfront, not during runtime
2. **Trust but verify** - Don't assume venv matches requirements.txt
3. **Progressive failures are painful** - One comprehensive check > multiple incremental fixes
4. **Clear error messages save time** - Users need actionable guidance, not stack traces
5. **Auto-remediation improves UX** - When safe, automatically fix common issues

---

## Closed By
Antigravity AI Assistant

## Verified By
System automated validation checks

---

**Incident Status:** ✅ RESOLVED  
**Follow-up Required:** None - All preventive measures implemented
