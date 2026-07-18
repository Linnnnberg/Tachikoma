#!/usr/bin/env python3
"""
Tachikoma Multi-Agent AI System - Main Entry Point

This is the main entry point for the Tachikoma system.
Provides CLI access to the system and can launch the Streamlit UI.
"""

import asyncio
import sys
import argparse
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tachikoma.core.orchestrator import TachikomaOrchestrator
from tachikoma.utils.logging import setup_logging, get_logger
from tachikoma.config.settings import load_settings

logger = get_logger(__name__)


def launch_ui():
    """Launch the Streamlit UI."""
    import subprocess
    ui_path = Path(__file__).parent / "ui" / "app.py"
    
    logger.info("Launching Streamlit UI...")
    print("🚀 Starting Tachikoma Streamlit UI...")
    print(f"📂 UI Location: {ui_path}")
    print("🌐 The UI will open in your browser at http://localhost:8501")
    print("\nPress Ctrl+C to stop the server.\n")
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", str(ui_path)])
    except KeyboardInterrupt:
        logger.info("Streamlit UI stopped by user")
        print("\n👋 Tachikoma UI stopped.")
    except Exception as e:
        logger.error(f"Error launching UI: {e}")
        print(f"\n❌ Error: {e}")
        print("\nMake sure Streamlit is installed: pip install streamlit")


async def main_cli():
    """CLI version of the main entry point."""
    try:
        # Setup logging
        setup_logging()
        logger.info("Starting Tachikoma Multi-Agent AI System (CLI)")

        # Load configuration
        settings = load_settings()
        logger.info(f"Configuration loaded: {settings}")

        # Initialize orchestrator
        orchestrator = TachikomaOrchestrator(settings)
        logger.info("Orchestrator initialized")

        print("\n🤖 Tachikoma Multi-Agent AI System")
        print("=" * 50)
        print("\nCLI mode is for development and testing.")
        print("For the full experience, use: tachikoma --ui")
        print("Or run: streamlit run tachikoma/ui/app.py")
        print("\n" + "=" * 50 + "\n")

    except KeyboardInterrupt:
        logger.info("Shutting down Tachikoma system...")
    except Exception as e:
        logger.error(f"Error in main: {e}", exc_info=True)
        sys.exit(1)


def main_sync():
    """Synchronous wrapper for the main function."""
    parser = argparse.ArgumentParser(
        description="Tachikoma Multi-Agent AI System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  tachikoma --ui              Launch the Streamlit web interface
  tachikoma --cli             Run in CLI mode (development)
  
For more information, visit: https://github.com/your-username/tachikoma
        """
    )
    
    parser.add_argument(
        "--ui",
        action="store_true",
        help="Launch the Streamlit web interface (recommended)"
    )
    
    parser.add_argument(
        "--cli",
        action="store_true",
        help="Run in CLI mode (for development)"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="Tachikoma v0.1.0"
    )
    
    args = parser.parse_args()
    
    if args.ui:
        launch_ui()
    elif args.cli:
        asyncio.run(main_cli())
    else:
        # Default: show help and launch UI
        print("🤖 Tachikoma Multi-Agent AI System\n")
        print("No mode specified. Launching Streamlit UI...")
        print("(Use --help for more options)\n")
        launch_ui()


if __name__ == "__main__":
    main_sync()
