#!/usr/bin/env python3
"""
CI/CD Timing Test Script

This script measures how long each CI/CD check takes to ensure
we stay within the 3-minute constraint.
"""

import time
import subprocess
import sys
from pathlib import Path

def time_command(command: str, description: str) -> tuple[bool, float]:
    """Run a command and measure execution time."""
    print(f"[TIMING] {description}...")
    start_time = time.time()
    
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            check=True, 
            capture_output=True, 
            text=True
        )
        end_time = time.time()
        duration = end_time - start_time
        print(f"[SUCCESS] {description} completed in {duration:.2f} seconds")
        return True, duration
    except subprocess.CalledProcessError as e:
        end_time = time.time()
        duration = end_time - start_time
        print(f"[ERROR] {description} failed after {duration:.2f} seconds: {e}")
        return False, duration

def main():
    """Run timing tests for all CI/CD checks."""
    print("=" * 60)
    print("TACHIKOMA CI/CD TIMING TEST")
    print("=" * 60)
    
    total_start = time.time()
    results = {}
    
    # Test individual checks
    checks = [
        ("black --check tachikoma/", "Code Formatting Check"),
        ("flake8 tachikoma/ --max-line-length=100 --ignore=E203,W503,E402", "Linting Check"),
        ("mypy tachikoma/ --ignore-missing-imports", "Type Checking"),
        ("python -m pytest tachikoma/tests/ -v", "Unit Tests"),
        ("python -c \"import tachikoma; print('Package imports successfully')\"", "Import Test"),
    ]
    
    print("\n[PHASE 1] Individual Checks")
    print("-" * 40)
    
    for command, description in checks:
        success, duration = time_command(command, description)
        results[description] = {"success": success, "duration": duration}
    
    # Test combined checks (simulating CI pipeline)
    print("\n[PHASE 2] Combined CI Pipeline Simulation")
    print("-" * 40)
    
    ci_start = time.time()
    
    # Quick checks (what would run in CI)
    quick_checks = [
        ("black --check tachikoma/", "Format Check"),
        ("flake8 tachikoma/ --max-line-length=100 --ignore=E203,W503,E402", "Lint Check"),
        ("python -m pytest tachikoma/tests/test_basic.py -v", "Basic Tests"),
        ("python -c \"import tachikoma\"", "Import Check"),
    ]
    
    ci_success = True
    for command, description in quick_checks:
        success, duration = time_command(command, description)
        if not success:
            ci_success = False
        results[f"CI_{description}"] = {"success": success, "duration": duration}
    
    ci_end = time.time()
    ci_duration = ci_end - ci_start
    
    # Test Docker operations
    print("\n[PHASE 3] Docker Operations")
    print("-" * 40)
    
    docker_checks = [
        ("docker --version", "Docker Version Check"),
        ("docker-compose config", "Docker Compose Config Check"),
    ]
    
    for command, description in docker_checks:
        success, duration = time_command(command, description)
        results[f"Docker_{description}"] = {"success": success, "duration": duration}
    
    # Summary
    total_end = time.time()
    total_duration = total_end - total_start
    
    print("\n" + "=" * 60)
    print("TIMING SUMMARY")
    print("=" * 60)
    
    print(f"\nTotal Test Duration: {total_duration:.2f} seconds")
    print(f"CI Pipeline Duration: {ci_duration:.2f} seconds")
    
    print(f"\nIndividual Check Times:")
    for check, data in results.items():
        status = "[PASS]" if data["success"] else "[FAIL]"
        print(f"  {status} {check}: {data['duration']:.2f}s")
    
    # Performance analysis
    print(f"\nPerformance Analysis:")
    print(f"  - CI Pipeline Target: 3 minutes (180 seconds)")
    print(f"  - Actual CI Duration: {ci_duration:.2f} seconds")
    print(f"  - Time Remaining: {180 - ci_duration:.2f} seconds")
    print(f"  - Efficiency: {(180 - ci_duration) / 180 * 100:.1f}% buffer")
    
    if ci_duration > 180:
        print(f"  [WARNING] CI pipeline exceeds 3-minute target!")
    else:
        print(f"  [SUCCESS] CI pipeline within 3-minute target")
    
    # Recommendations
    print(f"\nRecommendations:")
    if ci_duration < 60:
        print("  - Excellent performance! Consider adding more comprehensive tests")
    elif ci_duration < 120:
        print("  - Good performance! Room for additional checks")
    elif ci_duration < 180:
        print("  - Acceptable performance! Monitor for future additions")
    else:
        print("  - Performance issues! Consider optimizing or reducing checks")
    
    print("\n" + "=" * 60)
    print("TIMING TEST COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()
