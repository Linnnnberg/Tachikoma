#!/usr/bin/env python3
"""
Tachikoma Multi-Agent AI System - Main Entry Point

This is the main entry point for the Tachikoma system.
"""

import asyncio
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tachikoma.core.orchestrator import TachikomaOrchestrator
from tachikoma.ui.main_interface import TachikomaInterface
from tachikoma.utils.logging import setup_logging, get_logger
from tachikoma.config.settings import load_settings

logger = get_logger(__name__)


async def main():
    """Main entry point for the Tachikoma system."""
    try:
        # Setup logging
        setup_logging()
        logger.info("Starting Tachikoma Multi-Agent AI System")

        # Load configuration
        settings = load_settings()
        logger.info(f"Configuration loaded: {settings}")

        # Initialize orchestrator
        orchestrator = TachikomaOrchestrator(settings)
        logger.info("Orchestrator initialized")

        # Initialize UI
        interface = TachikomaInterface(orchestrator)
        logger.info("UI interface initialized")

        # Launch the interface
        logger.info("Launching Tachikoma interface...")
        await interface.launch()

    except KeyboardInterrupt:
        logger.info("Shutting down Tachikoma system...")
    except Exception as e:
        logger.error(f"Error in main: {e}", exc_info=True)
        sys.exit(1)


def main_sync():
    """Synchronous wrapper for the main function."""
    asyncio.run(main())


if __name__ == "__main__":
    main_sync()
