#!/usr/bin/env python3
"""
Specification Test Runner - Gravitas v4.5.0
Runs all specification tests for the 00x series documentation

Usage:
    python tests/run_spec_tests.py          # Run all spec tests
    python tests/run_spec_tests.py 001      # Run specific spec test
    python tests/run_spec_tests.py --verbose # Verbose output
"""

import sys
import subprocess
import argparse
from pathlib import Path


SPEC_TESTS = {
    "001": "test_spec_001_core_architecture.py",
    "002": "test_spec_002_vector_memory.py",
    "003": "test_spec_003_security_gatekeeper.py",
    "004": "test_spec_004_hardware_operations.py",
    "005": "test_spec_005_development_protocols.py",
    "006": "test_spec_006_telemetry_calibration.py",
}

SPEC_NAMES = {
    "001": "Core Architecture (IoC, Drivers, Reflex)",
    "002": "Vector Memory (Qdrant, Hybrid Search)",
    "003": "Security Gatekeeper (Safety Filter, Git Hygiene)",
    "004": "Hardware Operations (Dual-GPU, VRAM Protection)",
    "005": "Development Protocols (TDD, SOLID, Reasoning)",
    "006": "Telemetry Calibration (Phase 4.5, Granular Metrics)",
}


def run_spec_test(spec_id, verbose=False):
    """Run a specific specification test"""
    if spec_id not in SPEC_TESTS:
        print(f"❌ Unknown spec ID: {spec_id}")
        print(f"Available specs: {', '.join(SPEC_TESTS.keys())}")
        return False
    
    test_file = SPEC_TESTS[spec_id]
    spec_name = SPEC_NAMES[spec_id]
    
    print(f"\n{'='*70}")
    print(f"📋 Testing Spec {spec_id}: {spec_name}")
    print(f"{'='*70}\n")
    
    cmd = ["pytest", f"tests/{test_file}", "-v" if verbose else "-q"]
    
    try:
        result = subprocess.run(cmd, check=False)
        success = result.returncode == 0
        
        if success:
            print(f"\n✅ Spec {spec_id} tests PASSED")
        else:
            print(f"\n❌ Spec {spec_id} tests FAILED")
        
        return success
    except FileNotFoundError:
        print("❌ pytest not found. Install with: pip install pytest pytest-asyncio")
        return False
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False


def run_all_spec_tests(verbose=False):
    """Run all specification tests"""
    print("\n" + "="*70)
    print("🚀 GRAVITAS SPECIFICATION TEST SUITE v4.5.0")
    print("="*70)
    print("\nRunning comprehensive tests for all 00x specifications...")
    
    results = {}
    for spec_id in sorted(SPEC_TESTS.keys()):
        results[spec_id] = run_spec_test(spec_id, verbose)
    
    # Summary
    print("\n" + "="*70)
    print("📊 TEST SUMMARY")
    print("="*70)
    
    total = len(results)
    passed = sum(1 for r in results.values() if r)
    failed = total - passed
    
    for spec_id, success in sorted(results.items()):
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {status}  Spec {spec_id}: {SPEC_NAMES[spec_id]}")
    
    print(f"\n{'='*70}")
    print(f"Total: {total} | Passed: {passed} | Failed: {failed}")
    print(f"{'='*70}")
    
    if failed == 0:
        print("\n🎉 All specification tests PASSED!")
        return True
    else:
        print(f"\n⚠️  {failed} specification test(s) FAILED")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Run Gravitas specification tests"
    )
    parser.add_argument(
        'spec_id',
        nargs='?',
        help='Specific spec to test (001-006), or run all if omitted'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose output'
    )
    parser.add_argument(
        '--list',
        action='store_true',
        help='List available specification tests'
    )
    
    args = parser.parse_args()
    
    if args.list:
        print("\n📋 Available Specification Tests:\n")
        for spec_id, name in sorted(SPEC_NAMES.items()):
            test_file = SPEC_TESTS[spec_id]
            print(f"  {spec_id}: {name}")
            print(f"         File: {test_file}\n")
        return
    
    if args.spec_id:
        # Run specific spec
        success = run_spec_test(args.spec_id, args.verbose)
        sys.exit(0 if success else 1)
    else:
        # Run all specs
        success = run_all_spec_tests(args.verbose)
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
