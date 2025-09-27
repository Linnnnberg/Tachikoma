"""
Basic tests for Tachikoma system setup.
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from tachikoma.config.settings import Settings, load_settings
from tachikoma.utils.logging import setup_logging, get_logger


class TestBasicSetup:
    """Test basic system setup and configuration."""

    def test_settings_creation(self):
        """Test that settings can be created with default values."""
        settings = Settings()
        assert settings.model_name == "llama-3.1-70b-versatile"
        assert settings.max_agents == 10
        assert settings.log_level == "INFO"

    def test_settings_loading(self):
        """Test that settings can be loaded from environment."""
        settings = load_settings()
        assert isinstance(settings, Settings)
        assert hasattr(settings, "model_name")
        assert hasattr(settings, "max_agents")

    def test_logging_setup(self):
        """Test that logging can be set up."""
        setup_logging(level="DEBUG")
        logger = get_logger("test")
        assert logger is not None
        assert logger.level <= 10  # DEBUG level

    def test_project_structure(self):
        """Test that project structure is correct."""
        project_root = Path(__file__).parent.parent.parent
        assert (project_root / "tachikoma").exists()
        assert (project_root / "tachikoma" / "core").exists()
        assert (project_root / "tachikoma" / "agents").exists()
        assert (project_root / "tachikoma" / "ui").exists()
        assert (project_root / "tachikoma" / "utils").exists()
        assert (project_root / "tachikoma" / "config").exists()
        assert (project_root / "tachikoma" / "tests").exists()

    def test_imports(self):
        """Test that core modules can be imported."""
        try:
            from tachikoma.config.settings import Settings  # noqa: F401
            from tachikoma.utils.logging import setup_logging  # noqa: F401

            assert True
        except ImportError as e:
            pytest.fail(f"Import failed: {e}")


if __name__ == "__main__":
    pytest.main([__file__])
