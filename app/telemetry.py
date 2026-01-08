import logging
import json
import time
import os
from typing import Any, Dict, Optional
import httpx

logger = logging.getLogger("Gravitas_TELEMETRY")

#  Circuit breaker state
class CircuitBreaker:
    """Simple circuit breaker to prevent cascading failures."""
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.last_failure_time = None
        self.is_open = False
    
    def record_failure(self):
        """Record a failure and open circuit if threshold exceeded."""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.is_open = True
            logger.warning(f"🔴 Circuit breaker OPEN after {self.failure_count} failures")
    
    def record_success(self):
        """Record a success and reset circuit."""
        if self.failure_count > 0:
            logger.info("🟢 Circuit breaker CLOSED - telemetry service recovered")
        self.failure_count = 0
        self.is_open = False
    
    def can_attempt(self) -> bool:
        """Check if we should attempt a request."""
        if not self.is_open:
            return True
        
        # Check if enough time has passed to retry
        if self.last_failure_time and time.time() - self.last_failure_time > self.timeout:
            logger.info("⚡ Circuit breaker attempting retry...")
            self.is_open = False
            self.failure_count = 0
            return True
        
        return False


class TelemetryLogger:
    """
    HTTP-based telemetry logger for system events.
    Sends events to dedicated telemetry service via fire-and-forget HTTP requests.
    
    Supports:
    - Load Latency: VRAM model loading time tracking
    - Thought Latency: Inference speed tracking  
    - Token-aware efficiency metrics
    
    Features:
    - Circuit breaker pattern to prevent cascading failures
    - Fallback to stdout logging when service unavailable
    - Fire-and-forget async requests (non-blocking)
    """

    def __init__(self):
        # Get telemetry service URL from environment
        self.telemetry_url = os.getenv("TELEMETRY_URL", "http://gravitas_telemetry:8006")
        self.enabled = os.getenv("TELEMETRY_ENABLED", "true").lower() == "true"
        self.circuit_breaker = CircuitBreaker()
        self.client = None
        
        if self.enabled:
            logger.info(f"📊 Telemetry client initialized (service: {self.telemetry_url})")
        else:
            logger.warning("⚠️ Telemetry disabled via TELEMETRY_ENABLED=false")
    
    def _get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client instance."""
        if self.client is None:
            self.client = httpx.AsyncClient(
                timeout=httpx.Timeout(2.0, connect=1.0),  # Fast timeouts
                limits=httpx.Limits(max_keepalive_connections=5, max_connections=10)
            )
        return self.client

    async def log(
        self,
        event_type: str,
        component: str = None,
        value: float = None,
        metadata: Dict[str, Any] = None,
        status: str = None
    ) -> bool:
        """
        Logs a telemetry event asynchronously to the telemetry service.

        Args:
            event_type: Type of event (e.g., "VRAM_CHECK", "VRAM_LOCKOUT")
            component: System component (e.g., "L1", "memory")
            value: Numeric value associated with the event
            metadata: Additional JSON-serializable metadata
            status: Event status (e.g., "OK", "WARNING", "ERROR")

        Returns:
            bool: True if logged successfully, False otherwise
        """
        if not self.enabled:
            return False
        
        # Check circuit breaker
        if not self.circuit_breaker.can_attempt():
            logger.debug("⚠️ Circuit breaker OPEN - skipping telemetry log")
            return False

        try:
            # Prepare event payload
            event = {
                "event_type": event_type,
                "component": component,
                "value": value,
                "metadata": metadata,
                "status": status
            }
            
            # Fire-and-forget HTTP request
            client = self._get_client()
            response = await client.post(
                f"{self.telemetry_url}/v1/telemetry/log",
                json=event
            )
            
            if response.status_code == 200:
                self.circuit_breaker.record_success()
                logger.debug(f"📊 TELEMETRY LOGGED: {event_type} ({component or 'unknown'})")
                return True
            else:
                logger.warning(f"⚠️ Telemetry service returned {response.status_code}")
                self.circuit_breaker.record_failure()
                self._fallback_log(event)
                return False

        except (httpx.TimeoutException, httpx.ConnectError) as e:
            # Service unavailable - circuit breaker will open after threshold
            self.circuit_breaker.record_failure()
            logger.debug(f"⚠️ Telemetry service unavailable: {e}")
            self._fallback_log(event)
            return False
        
        except Exception as e:
            logger.error(f"❌ TELEMETRY LOG FAILURE: {e}")
            self._fallback_log(event)
            return False
    
    def _fallback_log(self, event: dict):
        """Fallback logging to stdout when service is unavailable."""
        logger.info(f"📊 [FALLBACK] {event['event_type']}: {json.dumps(event, default=str)}")

    async def get_recent_events(self, limit: int = 10, component: str = None) -> list:
        """
        Retrieves recent telemetry events from the service.

        Args:
            limit: Maximum number of events to return
            component: Filter by specific component (optional)

        Returns:
            List of telemetry event dictionaries
        """
        if not self.enabled or not self.circuit_breaker.can_attempt():
            return []

        try:
            client = self._get_client()
            params = {"limit": limit}
            if component:
                params["component"] = component
            
            response = await client.get(
                f"{self.telemetry_url}/v1/telemetry/events",
                params=params
            )
            
            if response.status_code == 200:
                self.circuit_breaker.record_success()
                return response.json()
            else:
                self.circuit_breaker.record_failure()
                return []
            
        except Exception as e:
            logger.error(f"❌ TELEMETRY QUERY FAILURE: {e}")
            self.circuit_breaker.record_failure()
            return []
    
    async def log_load_latency(
        self, 
        model_name: str, 
        load_time_seconds: float,
        success: bool = True
    ) -> bool:
        """
        Logs VRAM model load latency with sub-second precision.
        
        Args:
            model_name: Name of the model being loaded
            load_time_seconds: Time taken to load in seconds (float for precision)
            success: Whether the load succeeded
            
        Returns:
            bool: True if logged successfully
        """
        return await self.log(
            event_type="LOAD_LATENCY",
            component=model_name,
            value=load_time_seconds,
            metadata={"model": model_name, "load_time_ms": round(load_time_seconds * 1000, 2)},
            status="OK" if success else "ERROR"
        )
    
    async def log_thought_latency(
        self,
        model_name: str,
        inference_time_seconds: float,
        tokens_generated: int,
        prompt_tokens: int = 0
    ) -> bool:
        """
        Logs inference latency with token-aware efficiency metrics.
        
        Args:
            model_name: Name of the model used for inference
            inference_time_seconds: Time taken for inference (float for precision)
            tokens_generated: Number of tokens generated
            prompt_tokens: Number of tokens in the prompt
            
        Returns:
            bool: True if logged successfully
        """
        # Calculate efficiency score: Latency-Per-Token (ms/token)
        efficiency_score = (inference_time_seconds * 1000) / tokens_generated if tokens_generated > 0 else 0
        
        return await self.log(
            event_type="THOUGHT_LATENCY",
            component=model_name,
            value=efficiency_score,  # Store efficiency score as primary value
            metadata={
                "model": model_name,
                "inference_time_ms": round(inference_time_seconds * 1000, 2),
                "tokens_generated": tokens_generated,
                "prompt_tokens": prompt_tokens,
                "total_tokens": tokens_generated + prompt_tokens,
                "latency_per_token_ms": round(efficiency_score, 4)
            },
            status="OK"
        )
    
    @staticmethod
    def start_timer() -> float:
        """Returns current time for latency measurement."""
        return time.perf_counter()
    
    @staticmethod
    def measure_latency(start_time: float) -> float:
        """
        Calculates latency from start_time to now.
        
        Args:
            start_time: Result from start_timer()
            
        Returns:
            float: Elapsed time in seconds
        """
        return time.perf_counter() - start_time
    
    async def get_aggregated_efficiency(
        self,
        component: str = None,
        hours: int = 24
    ) -> Dict[str, Any]:
        """
        Calculates aggregated efficiency metrics over a time window.
        
        Args:
            component: Filter by model/component name (optional)
            hours: Time window in hours (default 24)
            
        Returns:
            Dict with weighted efficiency scores and statistics
        """
        if not self.enabled or not self.circuit_breaker.can_attempt():
            return {}
        
        try:
            client = self._get_client()
            params = {"hours": hours}
            if component:
                params["component"] = component
            
            response = await client.get(
                f"{self.telemetry_url}/v1/telemetry/stats",
                params=params
            )
            
            if response.status_code == 200:
                self.circuit_breaker.record_success()
                return response.json()
            else:
                self.circuit_breaker.record_failure()
                return {}
                
        except Exception as e:
            logger.error(f"❌ AGGREGATION QUERY FAILURE: {e}")
            self.circuit_breaker.record_failure()
            return {}
    
    async def close(self):
        """Close the HTTP client."""
        if self.client:
            await self.client.aclose()
            self.client = None


# Singleton Instance
telemetry = TelemetryLogger()
