import pytest
from app.services.dispatcher.router import DispatcherRouter, UserQuery, TelemetryState, TargetModel

def test_dispatcher_ruleset():
    router = DispatcherRouter()
    
    # Test Rule A: Complexity > 8 -> L3
    q_complex = UserQuery(text="Solve complex architectural problem", code_complexity=9)
    t_normal = TelemetryState(vram_usage_percent=30, system_load_percent=20, avg_latency=0.5)
    assert router.route(q_complex, t_normal) == TargetModel.L3
    
    # Test Rule B: System Load > 90% -> L2
    q_simple = UserQuery(text="What is 2+2?", code_complexity=1)
    t_heavy = TelemetryState(vram_usage_percent=50, system_load_percent=95, avg_latency=0.5)
    assert router.route(q_simple, t_heavy) == TargetModel.L2
    
    # Test Rule C: Default -> L1
    t_light = TelemetryState(vram_usage_percent=30, system_load_percent=10, avg_latency=0.5)
    assert router.route(q_simple, t_light) == TargetModel.L1

    # Edge Case: Both Heavy Load and High Complexity -> Complexity takes precedence (Rule A)
    assert router.route(q_complex, t_heavy) == TargetModel.L3
