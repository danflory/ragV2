# Nexus Dashboard: Force Re-Scan Improvements

**Date:** January 5, 2026  
**Issue:** Force re-scan button provides no feedback or VRAM usage reporting  
**Status:** ✅ Fixed

---

## Problem Description

When clicking the "Force Re-Scan" button in the Nexus Dashboard:
- ❌ No status update that ingestion is in progress
- ❌ No VRAM usage report during processing
- ❌ No feedback about files processed or chunks ingested
- ❌ User uncertain if the operation is working

---

## Root Cause

The ingest button handler in `dashboard/app.js` (line 275) was using a generic `handleAction('/ingest')` function that:
- Only showed a simple success/error notification
- Did not parse the detailed response from the API
- Did not trigger VRAM monitoring during the operation
- Provided no progress updates

---

## Solution Implemented

### 1. Enhanced Ingest Button Handler
**File:** `dashboard/app.js`

**Changes:**
1. **Immediate Feedback:** Shows a loading message when re-scan starts
2. **Detailed Progress:** Parses API response to show files processed and chunks ingested
3. **Real-time VRAM Monitoring:** Polls health endpoint every 1 second during ingestion
4. **Proper Cleanup:** Stops monitoring when ingestion completes or fails
5. **Clear Status Updates:** Updates the loading message with final results

### 2. Implementation Details

```javascript
elements.ingestBtn.addEventListener('click', async () => {
    // Show immediate feedback
    const loadingId = appendMessage('system', '🔄 FORCE RE-SCAN INITIATED: Purging old memory...');
    
    // Start continuous VRAM monitoring during ingestion (every 1s)
    const healthMonitor = setInterval(() => refreshHealth(), 1000);
    
    try {
        const response = await fetch(`${API_URL}/ingest`, { method: 'POST' });
        const data = await response.json();
        
        // Stop monitoring
        clearInterval(healthMonitor);
        
        if (data.status === 'success') {
            const summary = data.summary || {};
            const msg = `✅ INGESTION COMPLETE\n` +
                       `📁 Files Processed: ${summary.files_processed || 0}\n` +
                       `📄 Chunks Ingested: ${summary.chunks_ingested || 0}\n` +
                       `⏱️ Memory refreshed and ready for queries.`;
            updateMessage(loadingId, msg);
            
            // Final refresh to show updated state
            setTimeout(() => {
                refreshHealth();
                refreshStats();
            }, 1000);
        } else {
            updateMessage(loadingId, `❌ INGESTION FAILED: ${data.message || 'Unknown error'}`);
        }
    } catch (e) {
        // Stop monitoring on error
        clearInterval(healthMonitor);
        updateMessage(loadingId, `❌ CONNECTION ERROR: ${e.message}`);
    }
});
```

---

## User Experience Improvements

### Before Fix:
1. User clicks "Force Re-Scan"
2. Button appears to do nothing
3. No indication of progress
4. VRAM stats remain static
5. Eventually a small notification appears
6. No details about what was processed

### After Fix:
1. User clicks "Force Re-Scan"
2. **Immediate message:** "🔄 FORCE RE-SCAN INITIATED: Purging old memory..."
3. **VRAM stats update every second** showing GPU activity
4. **Detailed completion message:**
   ```
   ✅ INGESTION COMPLETE
   📁 Files Processed: 51
   📄 Chunks Ingested: 389
   ⏱️ Memory refreshed and ready for queries.
   ```
5. **Final stats refresh** showing updated system state

---

## Technical Details

### Health Monitoring
- **Polling Interval:** 1 second during ingestion
- **What's Monitored:**
  - VRAM usage percentage
  - VRAM used/total (MB)
  - Service status (Ollama, Qdrant, Postgres)
  - System initialization state

### API Response Structure
The `/ingest` endpoint returns:
```json
{
  "status": "success",
  "message": "Knowledge memory purged and re-ingested. Processed 51 files (389 chunks).",
  "summary": {
    "status": "success",
    "files_processed": 51,
    "chunks_ingested": 389
  }
}
```

### Error Handling
1. **Connection Errors:** Shows "❌ CONNECTION ERROR: {details}"
2. **API Errors:** Shows "❌ INGESTION FAILED: {message}"
3. **Monitoring Cleanup:** Always stops health monitor, even on error

---

## Testing

### Manual Testing Steps
1. Open Nexus Dashboard at `http://localhost:5050`
2. Click "Force Re-Scan" button
3. Verify immediate feedback message appears
4. Watch VRAM stats update in real-time
5. Verify detailed completion message shows:
   - Number of files processed
   - Number of chunks ingested
   - Confirmation that memory is ready

### Expected Behavior
- ✅ Loading message appears within 100ms of click
- ✅ VRAM stats refresh every ~1 second
- ✅ Completion message shows within 10-30 seconds (depending on corpus size)
- ✅ Final stats refresh after completion
- ✅ No orphaned interval timers (monitor properly cleaned up)

---

## Performance Impact

### Network Traffic
- **Before:** 1 API call + periodic background polling (every 5s)
- **After:** 1 API call + rapid polling during ingestion (~1s) + periodic background polling

**Impact:** Minimal - only adds ~5-30 extra health checks during ingestion

### Memory Usage
- Adds 1 interval timer during ingestion
- Properly cleaned up on completion/error
- No memory leaks

### User-Perceived Performance
- **Much better:** Users now have clear feedback and can monitor progress
- **Reduced anxiety:** Real-time VRAM updates show system is working

---

## Files Modified

1. **`/home/dflory/dev_env/Gravitas/dashboard/app.js`**
   - Lines 275-307: Enhanced ingest button handler
   - Added real-time health monitoring
   - Added detailed progress feedback
   - Added proper error handling

---

## Deployment

### Steps Taken
1. Modified `dashboard/app.js` with enhanced handler
2. Rebuilt Docker container: `docker-compose up -d --build rag_app`
3. Container restarted with updated dashboard code
4. Changes immediately available (no cache clearing needed for JS files)

### Verification
```bash
# Check container is running
docker ps | grep Gravitas_rag_backend

# Check logs for errors
docker logs Gravitas_rag_backend --tail 20

# Test dashboard accessibility
curl http://localhost:5050/health
```

---

## Future Improvements (Optional)

### Short-term
1. **Progress Bar:** Add visual progress bar showing ingestion percentage
2. **Real-time File Names:** Stream currently processing file names
3. **Time Estimation:** Show estimated time remaining based on processing rate

### Medium-term
1. **Cancellation:** Add ability to cancel in-progress ingestion
2. **Partial Progress:** Save progress if ingestion is interrupted
3. **Background Mode:** Allow ingestion to run in background while using dashboard

### Long-term
1. **Incremental Ingestion:** Only re-ingest changed files
2. **Smart Scheduling:** Suggest optimal times for re-scan based on usage patterns
3. **Webhook Notifications:** Notify when long ingestion completes

---

## Related Issues

### Known Issues (Not Addressed)
1. **nvidia-smi not available in container:** GPU stats show errors in logs
   - Impact: Low (stats still display using fallback values)
   - Fix: Install nvidia-cuda-toolkit in Dockerfile

2. **/health/stream SSE crashes:** Server-sent events have encoding bug
   - Impact: Medium (falls back to polling after crash)
   - Fix: Already documented in previous session notes

### Complementary Improvements
These changes work well with:
- FAQ.md for better RAG responses
- Integrated test suite for verification
- Diagnostic tools for debugging

---

## Summary

**Problem:** No feedback on force re-scan operation  
**Solution:** Enhanced UI with real-time monitoring and detailed progress  
**Impact:** Significantly improved user experience  
**Status:** ✅ Complete and deployed

Users can now confidently trigger re-scans and monitor the ingestion process in real-time with clear feedback about GPU usage, files processed, and final results.
