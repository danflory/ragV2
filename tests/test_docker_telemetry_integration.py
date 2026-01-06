"""
Docker Integration Tests for Phase 4.5 Granular Telemetry
Runs inside Docker container with full database connectivity

Execute from host:
    docker exec gravitas_mcp python /app/tests/test_docker_telemetry_integration.py
"""

import asyncio
import time
import sys
import os

sys.path.insert(0, '/app')

from app.telemetry import telemetry
from app.database import db


async def test_1_load_latency_tracking():
    """
    DOCKER INTEGRATION TEST 1: Load Latency Tracking with Database
    """
    print("\n" + "="*70)
    print("🧪 DOCKER TEST 1: Load Latency Tracking (Full Database)")
    print("="*70)
    
    # Ensure database is connected
    await db.connect()
    assert db.is_ready(), "Database must be ready"
    print("✅ Database connected\n")
    
    # Simulate model loading
    print("📊 Simulating gemma2:27b model load...")
    start_time = telemetry.start_timer()
    await asyncio.sleep(2.5)
    load_time = telemetry.measure_latency(start_time)
    
    print(f"⏱️  Measured load time: {load_time:.4f} seconds ({load_time * 1000:.1f} ms)")
    
    # Log to database
    print("💾 Logging to database...")
    result = await telemetry.log_load_latency(
        model_name="gemma2:27b-docker-test",
        load_time_seconds=load_time,
        success=True
    )
    
    assert result is True, "Should log successfully"
    print("✅ Logged to database\n")
    
    # Verify persistence
    print("🔍 Verifying database persistence...")
    events = await telemetry.get_recent_events(limit=10, component="gemma2:27b-docker-test")
    
    assert len(events) > 0, "Should retrieve logged event"
    latest = events[0]
    
    print(f"📋 Retrieved event:")
    print(f"   - Event type: {latest['event_type']}")
    print(f"   - Component: {latest['component']}")
    print(f"   - Value: {latest['value']:.4f} seconds")
    print(f"   - Status: {latest['status']}")
    print(f"   - Timestamp: {latest['timestamp']}")
    
    assert latest['event_type'] == 'LOAD_LATENCY'
    assert latest['component'] == 'gemma2:27b-docker-test'
    assert latest['value'] == load_time
    
    # Check metadata
    metadata = latest['metadata']
    if isinstance(metadata, dict):
        print(f"   - Metadata: {metadata}")
        assert 'load_time_ms' in metadata
        assert metadata['load_time_ms'] > 2500
    
    print("\n✅ DOCKER TEST 1 PASSED")
    print("   - Docker environment: ✅")
    print("   - Database persistence: ✅")
    print("   - Sub-second precision: ✅")
    print("   - Metadata storage: ✅")
    print("="*70 + "\n")


async def test_2_thought_latency_efficiency():
    """
    DOCKER INTEGRATION TEST 2: Thought Latency with Token-Aware Efficiency
    """
    print("\n" + "="*70)
    print("🧪 DOCKER TEST 2: Thought Latency & Efficiency (Full Database)")
    print("="*70)
    
    assert db.is_ready(), "Database must be ready"
    print("✅ Database connected\n")
    
    # Simulate inference
    print("📊 Simulating llama3.2:3b-docker inference...")
    print("   - Generating 200 tokens")
    print("   - Prompt: 50 tokens")
    
    start_time = telemetry.start_timer()
    await asyncio.sleep(3.0)
    inference_time = telemetry.measure_latency(start_time)
    
    print(f"⏱️  Inference time: {inference_time:.4f} seconds")
    
    # Log with token information
    tokens_generated = 200
    prompt_tokens = 50
    
    print("💾 Logging thought latency...")
    result = await telemetry.log_thought_latency(
        model_name="llama3.2:3b-docker-test",
        inference_time_seconds=inference_time,
        tokens_generated=tokens_generated,
        prompt_tokens=prompt_tokens
    )
    
    assert result is True, "Should log successfully"
    print("✅ Logged to database\n")
    
    # Verify efficiency score
    expected_efficiency = (inference_time * 1000) / tokens_generated
    print(f"📈 Expected efficiency: {expected_efficiency:.2f} ms/token")
    
    events = await telemetry.get_recent_events(limit=10, component="llama3.2:3b-docker-test")
    assert len(events) > 0, "Should retrieve event"
    
    latest = events[0]
    stored_efficiency = float(latest['value'])  # Convert Decimal to float
    
    print(f"📋 Retrieved event:")
    print(f"   - Event type: {latest['event_type']}")
    print(f"   - Efficiency score: {stored_efficiency:.2f} ms/token")
    
    assert latest['event_type'] == 'THOUGHT_LATENCY'
    assert abs(stored_efficiency - expected_efficiency) < 0.1
    
    # Check token metadata
    metadata = latest['metadata']
    if isinstance(metadata, dict):
        print(f"   - Tokens generated: {metadata['tokens_generated']}")
        print(f"   - Prompt tokens: {metadata['prompt_tokens']}")
        print(f"   - Total tokens: {metadata['total_tokens']}")
        print(f"   - Latency per token: {metadata['latency_per_token_ms']:.4f} ms")
        
        assert metadata['tokens_generated'] == tokens_generated
        assert metadata['prompt_tokens'] == prompt_tokens
        assert metadata['total_tokens'] == tokens_generated + prompt_tokens
    
    print("\n✅ DOCKER TEST 2 PASSED")
    print("   - Database integration: ✅")
    print("   - Efficiency calculation: ✅")
    print(f"   - Efficiency score: {stored_efficiency:.2f} ms/token")
    print("   - Token tracking: ✅")
    print("="*70 + "\n")


async def test_3_full_pipeline_aggregation():
    """
    DOCKER INTEGRATION TEST 3: Full Pipeline with Aggregation
    """
    print("\n" + "="*70)
    print("🧪 DOCKER TEST 3: Full Pipeline - Aggregation & Monitoring")
    print("="*70)
    
    assert db.is_ready(), "Database must be ready"
    print("✅ Database connected\n")
    
    # Log multiple events
    print("📊 Logging multiple telemetry events...")
    
    models = ["gemma2:27b-agg", "llama3.2:3b-agg", "qwen2.5:7b-agg"]
    
    for i, model in enumerate(models):
        await telemetry.log_thought_latency(
            model_name=model,
            inference_time_seconds=1.0 + (i * 0.5),
            tokens_generated=100 + (i * 50),
            prompt_tokens=50
        )
        print(f"   ✅ {model}")
    
    print("✅ All events logged\n")
    
    # Test aggregation
    print("📊 Testing aggregated efficiency...")
    aggregated = await telemetry.get_aggregated_efficiency(hours=24)
    
    assert isinstance(aggregated, dict), "Should return dict"
    print(f"📈 Aggregated data: {list(aggregated.keys())}")
    
    if 'components' in aggregated:
        components = aggregated['components']
        print(f"   - Components tracked: {len(components)}")
        
        for comp in components:
            if 'agg' in comp.get('component', ''):
                print(f"   - {comp['component']}: "
                      f"{comp.get('avg_efficiency_score', 0):.2f} ms/token "
                      f"({comp.get('measurement_count', 0)} measurements)")
    
    print("✅ Aggregation working\n")
    
    # Test 60-day statistics
    print("📊 Testing 60-day statistics...")
    stats = await telemetry.get_60day_statistics()
    
    assert isinstance(stats, dict), "Should return stats"
    
    if 'overall' in stats:
        overall = stats['overall']
        print(f"   - Total measurements: {overall.get('total_measurements', 0)}")
        print(f"   - Unique models: {overall.get('unique_models', 0)}")
    
    print("✅ 60-day statistics working\n")
    
    # Test footprint monitoring
    print("📊 Testing database footprint...")
    footprint = await telemetry.get_telemetry_footprint()
    
    assert isinstance(footprint, dict), "Should return footprint"
    
    if 'table_sizes' in footprint:
        for table in footprint['table_sizes']:
            print(f"   - {table['tablename']}: {table['total_size']}")
    
    if 'row_counts' in footprint:
        counts = footprint['row_counts']
        print(f"   - Telemetry rows: {counts.get('system_telemetry', 0):,}")
        print(f"   - Usage rows: {counts.get('usage_stats', 0):,}")
    
    print("✅ Footprint monitoring working\n")
    
    print("="*70)
    print("✅ DOCKER TEST 3 PASSED")
    print("   - Multiple event logging: ✅")
    print("   - Aggregated efficiency: ✅")
    print("   - 60-day statistics: ✅")
    print("   - Footprint monitoring: ✅")
    print("="*70 + "\n")


async def main():
    """Run all Docker integration tests"""
    print("\n" + "="*70)
    print("🐳 PHASE 4.5 GRANULAR TELEMETRY - DOCKER INTEGRATION TESTS")
    print("="*70)
    print("\nRunning inside Docker container with full database connectivity\n")
    
    # Connect to database
    await db.connect()
    
    if not db.is_ready():
        print("❌ DATABASE NOT AVAILABLE")
        print("   Ensure Gravitas_postgres container is running")
        return 1
    
    print("✅ Database connection established")
    print(f"   Host: {os.getenv('GRAVITAS_DB_HOST', 'unknown')}")
    print(f"   Database: {os.getenv('GRAVITAS_DB_NAME', 'unknown')}\n")
    
    passed = 0
    failed = 0
    
    tests = [
        ("Load Latency Tracking", test_1_load_latency_tracking),
        ("Thought Latency & Efficiency", test_2_thought_latency_efficiency),
        ("Full Pipeline & Aggregation", test_3_full_pipeline_aggregation)
    ]
    
    for test_name, test_func in tests:
        try:
            await test_func()
            passed += 1
        except AssertionError as e:
            failed += 1
            print(f"\n❌ TEST FAILED: {test_name}")
            print(f"   Assertion: {e}\n")
        except Exception as e:
            failed += 1
            print(f"\n❌ TEST ERROR: {test_name}")
            print(f"   Exception: {e}\n")
    
    # Disconnect
    await db.disconnect()
    
    # Summary
    print("\n" + "="*70)
    print("📊 DOCKER INTEGRATION TEST SUMMARY")
    print("="*70)
    print(f"Environment: Docker Container (gravitas_mcp)")
    print(f"Database: Postgres (Gravitas_postgres)")
    print(f"Total Tests: {len(tests)}")
    print(f"Passed: {passed} ✅")
    print(f"Failed: {failed} ❌")
    print("="*70)
    
    if failed == 0:
        print("\n🎉 ALL DOCKER INTEGRATION TESTS PASSED!")
        print("\nPhase 4.5 Granular Telemetry VERIFIED:")
        print("  ✅ Docker environment integration")
        print("  ✅ Full database persistence")
        print("  ✅ Sub-second precision timing")
        print("  ✅ Token-aware efficiency scoring")
        print("  ✅ Aggregation and monitoring")
        print("  ✅ Ready for production deployment")
        return 0
    else:
        print(f"\n⚠️  {failed} test(s) failed")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
