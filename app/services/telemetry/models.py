"""
Gravitas Telemetry Service - Pydantic Models
API request/response models for telemetry event ingestion and querying.
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime


class TelemetryEvent(BaseModel):
    """Model for incoming telemetry events."""
    event_type: str = Field(..., description="Type of event (e.g., VRAM_CHECK, THOUGHT_LATENCY)")
    component: Optional[str] = Field(None, description="System component (e.g., L1, gemma2:27b)")
    value: Optional[float] = Field(None, description="Numeric value associated with event")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional JSON metadata")
    status: Optional[str] = Field(None, description="Event status (OK, WARNING, ERROR)")

    class Config:
        json_schema_extra = {
            "example": {
                "event_type": "THOUGHT_LATENCY",
                "component": "gemma2:27b",
                "value": 2.45,
                "metadata": {
                    "inference_time_ms": 245.3,
                    "tokens_generated": 100,
                    "prompt_tokens": 50
                },
                "status": "OK"
            }
        }


class TelemetryEventResponse(BaseModel):
    """Response after logging a telemetry event."""
    success: bool
    message: str
    event_id: Optional[int] = None


class TelemetryQuery(BaseModel):
    """Query parameters for retrieving telemetry events."""
    limit: int = Field(10, ge=1, le=1000, description="Maximum number of events to return")
    component: Optional[str] = Field(None, description="Filter by component name")
    event_type: Optional[str] = Field(None, description="Filter by event type")
    hours: Optional[int] = Field(None, ge=1, le=720, description="Time window in hours")


class TelemetryEventRecord(BaseModel):
    """Model for a stored telemetry event."""
    id: int
    event_type: str
    component: Optional[str]
    value: Optional[float]
    metadata: Optional[Dict[str, Any]]
    status: Optional[str]
    timestamp: datetime

    class Config:
        from_attributes = True


class TelemetryStatsResponse(BaseModel):
    """Response for aggregated statistics."""
    component: Optional[str]
    measurement_count: int
    avg_efficiency_score: Optional[float]
    best_efficiency: Optional[float]
    worst_efficiency: Optional[float]
    total_tokens: Optional[int]
    time_window_hours: int


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    service: str
    database: bool
    queue_depth: int = 0
