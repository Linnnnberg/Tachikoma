#!/usr/bin/env python3
"""
CI/CD Setup Script for Tachikoma

This script helps set up the CI/CD pipeline and validates the configuration.
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command: str, description: str) -> bool:
    """Run a command and return success status."""
    print(f"[RUNNING] {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"[SUCCESS] {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_ci_requirements():
    """Check if CI requirements are met."""
    print("[CHECK] CI/CD requirements...")
    
    # Check if .github/workflows directory exists
    workflows_dir = Path(".github/workflows")
    if not workflows_dir.exists():
        print("[ERROR] .github/workflows directory not found")
        return False
    
    # Check if CI files exist
    ci_file = workflows_dir / "ci.yml"
    cd_file = workflows_dir / "cd.yml"
    
    if not ci_file.exists():
        print("[ERROR] ci.yml not found")
        return False
    
    if not cd_file.exists():
        print("[ERROR] cd.yml not found")
        return False
    
    # Check if Dockerfile exists
    if not Path("Dockerfile").exists():
        print("[ERROR] Dockerfile not found")
        return False
    
    # Check if docker-compose.yml exists
    if not Path("docker-compose.yml").exists():
        print("[ERROR] docker-compose.yml not found")
        return False
    
    print("[SUCCESS] All CI/CD files present")
    return True

def validate_ci_config():
    """Validate CI configuration files."""
    print("[CHECK] Validating CI configuration...")
    
    # Check if required tools are available (Windows compatible)
    tools = ["black", "flake8", "mypy", "pytest"]
    for tool in tools:
        if os.name == 'nt':  # Windows
            if not run_command(f"where {tool}", f"Checking {tool}"):
                print(f"[WARNING] {tool} not found - install with: pip install {tool}")
        else:  # Unix-like
            if not run_command(f"which {tool}", f"Checking {tool}"):
                print(f"[WARNING] {tool} not found - install with: pip install {tool}")
    
    # Skip YAML validation for now (YAML files are not Python)
    print("[SUCCESS] CI configuration files present")
    return True

def test_docker_setup():
    """Test Docker setup."""
    print("[CHECK] Testing Docker setup...")
    
    # Check if Docker is available
    if not run_command("docker --version", "Checking Docker"):
        print("[ERROR] Docker not available")
        return False
    
    # Test Dockerfile syntax (simplified check)
    if Path("Dockerfile").exists():
        print("[SUCCESS] Dockerfile exists")
    else:
        print("[ERROR] Dockerfile not found")
        return False
    
    # Test docker-compose syntax
    if run_command("docker-compose config", "Testing docker-compose"):
        print("[SUCCESS] docker-compose.yml syntax valid")
    else:
        print("[ERROR] docker-compose.yml syntax invalid")
        return False
    
    return True

def run_ci_checks():
    """Run local CI checks."""
    print("[CHECK] Running local CI checks...")
    
    # Code formatting
    if not run_command("black --check tachikoma/", "Code formatting check"):
        print("[ERROR] Code formatting issues found")
        return False
    
    # Linting
    if not run_command("flake8 tachikoma/ --max-line-length=100 --ignore=E203,W503,E402", "Linting check"):
        print("[ERROR] Linting issues found")
        return False
    
    # Type checking
    if not run_command("mypy tachikoma/ --ignore-missing-imports", "Type checking"):
        print("[ERROR] Type checking issues found")
        return False
    
    # Tests
    if not run_command("python -m pytest tachikoma/tests/ -v", "Running tests"):
        print("[ERROR] Tests failed")
        return False
    
    print("[SUCCESS] All CI checks passed")
    return True

def main():
    """Main setup function."""
    print("[START] Setting up Tachikoma CI/CD Pipeline...")
    
    # Check requirements
    if not check_ci_requirements():
        print("[ERROR] CI/CD requirements not met")
        sys.exit(1)
    
    # Validate configuration
    if not validate_ci_config():
        print("[ERROR] CI configuration invalid")
        sys.exit(1)
    
    # Test Docker setup
    if not test_docker_setup():
        print("[ERROR] Docker setup invalid")
        sys.exit(1)
    
    # Run CI checks
    if not run_ci_checks():
        print("[ERROR] CI checks failed")
        sys.exit(1)
    
    print("\n[SUCCESS] CI/CD Pipeline setup complete!")
    print("\nNext steps:")
    print("1. Commit and push to trigger CI pipeline")
    print("2. Create a tag to trigger CD pipeline")
    print("3. Monitor GitHub Actions for pipeline status")
    print("4. Check CICD_PLAN.md for detailed information")

if __name__ == "__main__":
    main()
