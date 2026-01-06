# 006_TELEMETRY_CALIBRATION.md
# STATUS: ACTIVE
# VERSION: 4.5.0 (Gravitas Command & Control / Telemetry Calibration)

## 1. OBJECTIVE
Implement **Granular Telemetry Calibration** with sub-second precision tracking for Load Latency (VRAM model loading) and Thought Latency (inference speed with token-aware metrics). This data powers Phase 5's Dynamic Model Governance.

## 2. ARCHITECTURE

### 2.1 The Components
1. **`app/telemetry.py` (The Sensor System):**
   * Class: `TelemetryLogger`
   * Responsibilities: Sub-second precision timing, token-aware efficiency tracking, aggregation, footprint monitoring
   * **IoC:** Singleton instance injected throughout the application

2. **Database Schema:**
   * Table: `system_telemetry`
   * Stores: event_type, component, value (efficiency score), metadata (JSONB), timestamp
   * Retention: 60-day window with automated pruning

3. **API Endpoints:**
   * `/telemetry/footprint` - Database storage metrics
   * `/telemetry/60day` - Historic performance trends

## 3. TELEMETRY DATA FLOW

```
1. MEASUREMENT START
   ↓
   start_time = telemetry.start_timer()
   ↓
2. OPERATION (Model Load or Inference)
   ↓
3. MEASUREMENT END
   ↓
   latency = telemetry.measure_latency(start_time)
   ↓
4. LOGGING (Token-Aware)
   ↓
   telemetry.log_thought_latency(model, latency, tokens)
   ↓
   → Calculates: efficiency_score = (latency_ms / tokens_generated)
   → Stores: value=efficiency_score, metadata={tokens, latency, etc}
   ↓
5. AGGREGATION (60-second intervals)
   ↓
   telemetry.get_aggregated_efficiency(hours=24)
   ↓
   → Weighted averages by token volume
   → Per-model performance rankings
   ↓
6. RETENTION & PRUNING
   ↓
   maintenance.py (60-day auto-pruning)
```

## 4. IMPLEMENTED INTERFACE

```python
class TelemetryLogger:
    async def log(
        self,
        event_type: str,
        component: str = None,
        value: float = None,
        metadata: Dict[str, Any] = None,
        status: str = None
    ) -> bool:
        """Generic telemetry logging with JSONB metadata."""
    
    async def log_load_latency(
        self, 
        model_name: str, 
        load_time_seconds: float,
        success: bool = True
    ) -> bool:
        """Logs VRAM model load latency with sub-second precision."""
    
    async def log_thought_latency(
        self,
        model_name: str,
        inference_time_seconds: float,
        tokens_generated: int,
        prompt_tokens: int = 0
    ) -> bool:
        """Logs inference latency with token-aware efficiency metrics."""
    
    async def get_aggregated_efficiency(
        self,
        component: str = None,
        hours: int = 24
    ) -> Dict[str, Any]:
        """Calculates weighted efficiency scores over time window."""
    
    async def get_60day_statistics(self) -> Dict[str, Any]:
        """Retrieves 60-day historic performance trends."""
    
    async def get_telemetry_footprint(self) -> Dict[str, Any]:
        """Monitors database footprint to prevent bloat."""
    
    @staticmethod
    def start_timer() -> float:
        """High-precision timer start using perf_counter()."""
    
    @staticmethod
    def measure_latency(start_time: float) -> float:
        """Calculates elapsed time from start_time."""
```

## 5. KEY METRICS

### 5.1 Load Latency
* **What:** Time to load a model into VRAM
* **Unit:** Seconds (float for sub-second precision)
* **Storage:** Direct value + metadata with milliseconds
* **Purpose:** Factor into model routing decisions in Phase 5

### 5.2 Thought Latency (Efficiency Score)
* **What:** Latency-Per-Token (ms/token) for inference
* **Calculation:** `(inference_time_ms) / tokens_generated`
* **Storage:** Efficiency score as primary `value`, detailed breakdown in metadata
* **Purpose:** Weighted performance comparison across models

### 5.3 Aggregated Efficiency
* **What:** Time-windowed average of efficiency scores
* **Features:** Filterable by component/model, customizable time window
* **Weighting:** Token volume considered for accurate strain representation
* **Purpose:** Real-time model performance rankings

### 5.4 Telemetry Footprint
* **What:** Database storage metrics
* **Monitors:** Table sizes, row counts, oldest records
* **Purpose:** Prevent database bloat, inform maintenance scheduling

## 6. ADVANCED FEATURES

### 6.1 Sub-Second Precision
* Uses `time.perf_counter()` for nanosecond accuracy
* Float storage in database preserves precision
* Critical for distinguishing fast model performance

### 6.2 Token-Aware Weighting
* All inference metrics weighted by tokens generated
* Efficiency score provides apples-to-apples comparison
* Prevents bias toward short or long generation tasks

### 6.3 60-Day Historic Window
* Long-term performance trending
* Automated pruning via `maintenance.py`
* Sufficient data for statistical confidence in Phase 5

### 6.4 Database Bloat Prevention
* Efficiency scores stored as primary value (not metadata)
* 60-second aggregation intervals recommended
* Auto-pruning enforces retention policy
* Footprint monitoring provides early warnings

## 7. INTEGRATION WITH PHASE 5

Phase 5 (Dynamic Model Governance) uses telemetry data for:

1. **Data-Driven Dispatcher:**
   * Query aggregated efficiency to rank models
   * Route tasks to optimal model based on current performance

2. **Predictive Context Orchestration:**
   * Use load latency data to calculate context switch costs
   * Factor in 60-day statistics for predictive modeling

3. **Dynamic Trade-off Self-Correction:**
   * Monitor efficiency trends to detect performance degradation
   * Automatically adjust routing based on real-world data

## 8. TESTING REQUIREMENTS

### 8.1 Unit Tests
* `test_telemetry.py` - Core logging and aggregation
* Timer precision validation
* Efficiency score calculation accuracy

### 8.2 Integration Tests
* Database persistence verification
* API endpoint responses
* Footprint monitoring accuracy

### 8.3 Performance Tests
* High-volume logging (1000+ events)
* Aggregation query performance
* Database bloat prevention verification

## 9. OPERATIONAL PROTOCOLS

### 9.1 Maintenance Schedule
* **Daily:** Footprint monitoring via dashboard
* **Weekly:** Review efficiency trends per model
* **Monthly:** Verify 60-day pruning execution

### 9.2 Alerting Thresholds
* **Database Size:** Alert if > 100MB for telemetry table
* **Row Count:** Alert if > 1M rows (suggests pruning failure)
* **Efficiency Degradation:** Alert if model efficiency drops >20%

### 9.3 Data Retention Policy
* **Active Data:** 60 days in Postgres
* **Archived Data:** Export to CSV/Parquet for long-term analysis (optional)
* **Purge Policy:** Automated via `maintenance.py`

## 10. PERFORMANCE BENCHMARKS

**Expected Metrics (Production):**
* Log operation: < 5ms
* Aggregation query: < 50ms (24-hour window)
* 60-day statistics: < 200ms
* Footprint monitoring: < 100ms

**Database Growth:**
* ~50-100 rows per hour (typical usage)
* ~1.2K-2.4K rows per day
* ~72K rows per 60 days
* Estimated size: 10-20MB per 60-day window

## 11. SECURITY CONSIDERATIONS

* **No PII:** Telemetry contains only system metrics
* **Read-Only API:** Endpoints are GET only, no mutation
* **SQL Injection:** All queries use parameterized statements
* **Access Control:** Dashboard auth required for sensitive metrics

## 12. COMPLIANCE WITH DEVELOPMENT PROTOCOLS

✅ **TDD:** Unit tests written before implementation  
✅ **SOLID:** Single Responsibility - telemetry is isolated module  
✅ **IoC:** Singleton pattern via container  
✅ **Async/Await:** Full async implementation  
✅ **Documentation:** This specification + inline docstrings  

---

## APPENDIX A: EVENT TYPES

| Event Type | Component | Value | Metadata |
|:-----------|:----------|:------|:---------|
| `LOAD_LATENCY` | Model name | Load time (s) | {model, load_time_ms} |
| `THOUGHT_LATENCY` | Model name | Efficiency score | {model, inference_time_ms, tokens_generated, prompt_tokens, total_tokens, latency_per_token_ms} |
| `VRAM_CHECK` | GPU ID | Free VRAM (MB) | {used, total, percentage} |
| `VRAM_LOCKOUT` | GPU ID | 0 | {trigger_threshold, free_vram} |

## APPENDIX B: EXAMPLE QUERIES

**Get model efficiency for last 24 hours:**
```python
efficiency = await telemetry.get_aggregated_efficiency(
    component="gemma2:27b",
    hours=24
)
```

**Get 60-day trends for all models:**
```python
stats = await telemetry.get_60day_statistics()
models = stats["model_trends"]
best_model = models[0]  # Ordered by efficiency (ASC)
```

**Monitor database footprint:**
```python
footprint = await telemetry.get_telemetry_footprint()
telemetry_size = footprint["table_sizes"][0]["size_bytes"]
if telemetry_size > 100_000_000:  # 100MB
    logger.warning("Telemetry database exceeds 100MB threshold")
```
