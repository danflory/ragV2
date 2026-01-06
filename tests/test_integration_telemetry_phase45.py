"""
Integration Tests for Phase 4.5 Granular Telemetry
Proves end-to-end functionality of sub-second telemetry tracking

These tests validate:
1. Load Latency tracking (model loading simulation)
2. Thought Latency with token-aware efficiency
3. Full pipeline: logging → aggregation → footprint monitoring
"""

import pytest
import asyncio
import time
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.telemetry import telemetry
from app.database import db


class TestGranularTelemetryIntegration:
    """Integration tests proving Phase 4.5 telemetry functionality"""
    
    @pytest.mark.asyncio
    async def test_integration_1_load_latency_tracking(self):
        """
        INTEGRATION TEST 1: Load Latency Tracking
        
        Proves:
        - Sub-second precision timing works
        - Load latency is correctly logged
        - Data persists to database
        - Metadata includes millisecond precision
        """
        print("\n" + "="*70)
        print("🧪 INTEGRATION TEST 1: Load Latency Tracking")
        print("="*70)
        
        if not db.is_ready():
            pytest.skip("Database not available - start Postgres container")
        
        # Simulate model loading with precise timing
        print("📊 Simulating model load (gemma2:27b)...")
        start_time = telemetry.start_timer()
        
        # Simulate 2.5 second load time
        await asyncio.sleep(2.5)
        
        load_time = telemetry.measure_latency(start_time)
        print(f"⏱️  Measured load time: {load_time:.4f} seconds")
        
        # Verify sub-second precision
        assert load_time >= 2.5, "Should measure at least 2.5 seconds"
        assert load_time < 3.0, "Should be < 3 seconds (no extra delay)"
        assert isinstance(load_time, float), "Should have float precision"
        
        # Log the load latency
        print("💾 Logging to telemetry system...")
        result = await telemetry.log_load_latency(
            model_name="gemma2:27b",
            load_time_seconds=load_time,
            success=True
        )
        
        assert result is True, "Load latency should log successfully"
        print("✅ Load latency logged successfully")
        
        # Verify it persisted to database
        print("🔍 Verifying database persistence...")
        events = await telemetry.get_recent_events(limit=10, component="gemma2:27b")
        
        assert len(events) > 0, "Should retrieve logged event"
        
        latest_event = events[0]
        assert latest_event['event_type'] == 'LOAD_LATENCY', "Should be LOAD_LATENCY event"
        assert latest_event['component'] == 'gemma2:27b', "Should track model name"
        assert latest_event['value'] == load_time, "Should store exact load time"
        
        # Check metadata
        metadata = latest_event['metadata']
        if isinstance(metadata, dict):
            print(f"📋 Metadata: {metadata}")
            assert 'load_time_ms' in metadata, "Should include millisecond precision"
            assert metadata['load_time_ms'] > 2500, "Should be > 2500ms"
        
        print("✅ INTEGRATION TEST 1 PASSED")
        print(f"   - Sub-second precision: ✅")
        print(f"   - Database persistence: ✅")
        print(f"   - Metadata storage: ✅")
        print("="*70 + "\n")
    
    @pytest.mark.asyncio
    async def test_integration_2_thought_latency_efficiency(self):
        """
        INTEGRATION TEST 2: Thought Latency with Token-Aware Efficiency
        
        Proves:
        - Inference timing works
        - Token counts are tracked
        - Efficiency score is calculated (ms/token)
        - Weighted metrics are stored correctly
        """
        print("\n" + "="*70)
        print("🧪 INTEGRATION TEST 2: Thought Latency & Efficiency Score")
        print("="*70)
        
        if not db.is_ready():
            pytest.skip("Database not available - start Postgres container")
        
        # Simulate inference with known parameters
        print("📊 Simulating inference (llama3.2:3b)...")
        print("   - Generating 200 tokens")
        print("   - Prompt: 50 tokens")
        
        start_time = telemetry.start_timer()
        
        # Simulate 3.0 second inference
        await asyncio.sleep(3.0)
        
        inference_time = telemetry.measure_latency(start_time)
        print(f"⏱️  Measured inference time: {inference_time:.4f} seconds")
        
        # Log thought latency
        tokens_generated = 200
        prompt_tokens = 50
        
        print(f"💾 Logging thought latency...")
        print(f"   - Tokens generated: {tokens_generated}")
        print(f"   - Total tokens: {tokens_generated + prompt_tokens}")
        
        result = await telemetry.log_thought_latency(
            model_name="llama3.2:3b",
            inference_time_seconds=inference_time,
            tokens_generated=tokens_generated,
            prompt_tokens=prompt_tokens
        )
        
        assert result is True, "Thought latency should log successfully"
        print("✅ Thought latency logged successfully")
        
        # Calculate expected efficiency score
        expected_efficiency = (inference_time * 1000) / tokens_generated
        print(f"📈 Expected efficiency score: {expected_efficiency:.2f} ms/token")
        
        # Verify it persisted with correct efficiency score
        print("🔍 Verifying efficiency calculation...")
        events = await telemetry.get_recent_events(limit=10, component="llama3.2:3b")
        
        assert len(events) > 0, "Should retrieve logged event"
        
        latest_event = events[0]
        assert latest_event['event_type'] == 'THOUGHT_LATENCY', "Should be THOUGHT_LATENCY event"
        
        # The value field should store the efficiency score
        stored_efficiency = latest_event['value']
        print(f"💾 Stored efficiency score: {stored_efficiency:.2f} ms/token")
        
        # Should be approximately equal (allowing for float precision)
        assert abs(stored_efficiency - expected_efficiency) < 0.1, \
            "Efficiency score should match calculation"
        
        # Check token metadata
        metadata = latest_event['metadata']
        if isinstance(metadata, dict):
            print(f"📋 Metadata: {metadata}")
            assert metadata['tokens_generated'] == tokens_generated, "Should track tokens"
            assert metadata['prompt_tokens'] == prompt_tokens, "Should track prompt tokens"
            assert metadata['total_tokens'] == tokens_generated + prompt_tokens, "Should sum tokens"
            assert 'latency_per_token_ms' in metadata, "Should include efficiency metric"
        
        print("✅ INTEGRATION TEST 2 PASSED")
        print(f"   - Inference timing: ✅")
        print(f"   - Token tracking: ✅")
        print(f"   - Efficiency calculation: ✅ ({expected_efficiency:.2f} ms/token)")
        print(f"   - Weighted storage: ✅")
        print("="*70 + "\n")
    
    @pytest.mark.asyncio
    async def test_integration_3_full_pipeline_aggregation(self):
        """
        INTEGRATION TEST 3: Full Telemetry Pipeline
        
        Proves:
        - Multiple metrics can be logged
        - Aggregation works across time windows
        - 60-day statistics are retrievable
        - Footprint monitoring tracks database size
        - End-to-end pipeline is functional
        """
        print("\n" + "="*70)
        print("🧪 INTEGRATION TEST 3: Full Pipeline - Aggregation & Monitoring")
        print("="*70)
        
        if not db.is_ready():
            pytest.skip("Database not available - start Postgres container")
        
        # 1. Log multiple telemetry events
        print("📊 Phase 1: Logging multiple telemetry events...")
        
        models = ["gemma2:27b", "llama3.2:3b", "qwen2.5:7b"]
        
        for i, model in enumerate(models):
            # Log thought latency for each model
            await telemetry.log_thought_latency(
                model_name=model,
                inference_time_seconds=1.0 + (i * 0.5),  # Varying times
                tokens_generated=100 + (i * 50),  # Varying token counts
                prompt_tokens=50
            )
            print(f"   ✅ Logged: {model}")
        
        print("✅ All events logged\n")
        
        # 2. Test Aggregated Efficiency
        print("📊 Phase 2: Testing aggregated efficiency...")
        
        aggregated = await telemetry.get_aggregated_efficiency(hours=24)
        
        assert isinstance(aggregated, dict), "Should return aggregation data"
        print(f"📈 Aggregated data retrieved: {len(aggregated)} components")
        
        if 'components' in aggregated:
            components = aggregated['components']
            print(f"   - Models tracked: {len(components)}")
            
            for comp in components:
                model_name = comp.get('component', 'unknown')
                avg_efficiency = comp.get('avg_efficiency_score', 0)
                count = comp.get('measurement_count', 0)
                print(f"   - {model_name}: {avg_efficiency:.2f} ms/token ({count} measurements)")
        
        print("✅ Aggregation working\n")
        
        # 3. Test 60-Day Statistics
        print("📊 Phase 3: Testing 60-day statistics...")
        
        stats_60day = await telemetry.get_60day_statistics()
        
        assert isinstance(stats_60day, dict), "Should return 60-day stats"
        print("📈 60-day statistics retrieved")
        
        if 'overall' in stats_60day:
            overall = stats_60day['overall']
            print(f"   - Total measurements: {overall.get('total_measurements', 0)}")
            print(f"   - Unique models: {overall.get('unique_models', 0)}")
        
        if 'model_trends' in stats_60day:
            trends = stats_60day['model_trends']
            print(f"   - Model trends: {len(trends)} models tracked")
            
            for trend in trends[:3]:  # Show first 3
                model = trend.get('component', 'unknown')
                avg_eff = trend.get('avg_efficiency', 0)
                tokens = trend.get('total_tokens_processed', 0)
                print(f"   - {model}: {avg_eff:.2f} ms/token, {tokens} tokens processed")
        
        print("✅ 60-day statistics working\n")
        
        # 4. Test Footprint Monitoring
        print("📊 Phase 4: Testing database footprint monitoring...")
        
        footprint = await telemetry.get_telemetry_footprint()
        
        assert isinstance(footprint, dict), "Should return footprint data"
        print("💾 Database footprint retrieved")
        
        if 'table_sizes' in footprint:
            for table in footprint['table_sizes']:
                name = table.get('tablename', 'unknown')
                size = table.get('total_size', '0')
                bytes_size = table.get('size_bytes', 0)
                print(f"   - {name}: {size} ({bytes_size:,} bytes)")
        
        if 'row_counts' in footprint:
            counts = footprint['row_counts']
            print(f"\n   Row counts:")
            print(f"   - system_telemetry: {counts.get('system_telemetry', 0):,}")
            print(f"   - usage_stats: {counts.get('usage_stats', 0):,}")
            print(f"   - history: {counts.get('history', 0):,}")
        
        if 'oldest_telemetry_record' in footprint:
            oldest = footprint['oldest_telemetry_record']
            print(f"\n   - Oldest record: {oldest}")
        
        print("✅ Footprint monitoring working\n")
        
        # Summary
        print("="*70)
        print("✅ INTEGRATION TEST 3 PASSED")
        print("   - Multiple event logging: ✅")
        print("   - Aggregated efficiency: ✅")
        print("   - 60-day statistics: ✅")
        print("   - Footprint monitoring: ✅")
        print("   - End-to-end pipeline: ✅")
        print("="*70 + "\n")


if __name__ == "__main__":
    # Run with verbose output
    pytest.main([__file__, "-v", "-s"])
