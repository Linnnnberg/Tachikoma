#!/usr/bin/env python3
"""
Development setup script for Tachikoma.

This script helps set up the development environment for the Tachikoma project.
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command: str, description: str) -> bool:
    """Run a command and return success status."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def main():
    """Main setup function."""
    print("🚀 Setting up Tachikoma development environment...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Create virtual environment if it doesn't exist
    venv_path = Path("venv")
    if not venv_path.exists():
        if not run_command("python -m venv venv", "Creating virtual environment"):
            sys.exit(1)
    else:
        print("✅ Virtual environment already exists")
    
    # Determine activation script based on OS
    if os.name == 'nt':  # Windows
        activate_script = "venv\\Scripts\\activate"
        pip_command = "venv\\Scripts\\pip"
    else:  # Unix-like
        activate_script = "venv/bin/activate"
        pip_command = "venv/bin/pip"
    
    # Upgrade pip
    if not run_command(f"{pip_command} install --upgrade pip", "Upgrading pip"):
        sys.exit(1)
    
    # Install requirements
    if not run_command(f"{pip_command} install -r requirements.txt", "Installing requirements"):
        sys.exit(1)
    
    # Install development requirements
    if not run_command(f"{pip_command} install -e .[dev]", "Installing development dependencies"):
        sys.exit(1)
    
    # Create necessary directories
    directories = [
        "exports",
        "logs", 
        "agent_states",
        "conversation_cache",
        "role_templates",
        "model_cache",
        "performance_logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")
    
    # Copy example environment file
    if not Path(".env").exists() and Path("env.example").exists():
        import shutil
        shutil.copy("env.example", ".env")
        print("✅ Created .env file from example")
    
    # Setup pre-commit hooks
    if run_command(f"{pip_command} install pre-commit", "Installing pre-commit"):
        if run_command("pre-commit install", "Setting up pre-commit hooks"):
            print("✅ Pre-commit hooks installed")
    
    print("\n🎉 Development environment setup complete!")
    print("\nNext steps:")
    print("1. Activate the virtual environment:")
    if os.name == 'nt':
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    print("2. Update .env file with your API keys")
    print("3. Run tests: python -m pytest")
    print("4. Start development: python -m tachikoma.main")

if __name__ == "__main__":
    main()

