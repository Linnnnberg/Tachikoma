"""
Settings and configuration management for Tachikoma.
"""

import os
from typing import Optional
from pydantic import BaseModel, Field
from pathlib import Path


class Settings(BaseModel):
    """Main settings class for Tachikoma system."""

    # API Configuration
    groq_api_key: Optional[str] = Field(default=None, description="Groq API key")
    model_name: str = Field(
        default="llama-3.1-70b-versatile", description="Default model name"
    )

    # System Configuration
    max_agents: int = Field(default=10, description="Maximum number of agents")
    conversation_timeout: int = Field(
        default=300, description="Conversation timeout in seconds"
    )
    resource_update_interval: int = Field(
        default=30, description="Resource update interval in seconds"
    )

    # UI Configuration
    ui_title: str = Field(
        default="Tachikoma Multi-Agent AI System", description="UI title"
    )
    ui_theme: str = Field(default="default", description="UI theme")
    enable_visualization: bool = Field(
        default=True, description="Enable resource visualization"
    )

    # Logging Configuration
    log_level: str = Field(default="INFO", description="Logging level")
    log_file: Optional[str] = Field(
        default="tachikoma.log", description="Log file path"
    )

    # Performance Configuration
    enable_caching: bool = Field(default=True, description="Enable response caching")
    cache_ttl: int = Field(default=3600, description="Cache TTL in seconds")
    max_concurrent_agents: int = Field(
        default=5, description="Maximum concurrent agents"
    )

    # Export Configuration
    export_format: str = Field(
        default="both", description="Export format: txt, csv, both"
    )
    export_directory: str = Field(default="./exports", description="Export directory")

    class Config:
        env_prefix = "TACHIKOMA_"
        case_sensitive = False


def load_settings() -> Settings:
    """Load settings from environment variables and config files."""

    # Load from environment variables
    settings_data = {}

    # Load from .env file if it exists
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, "r") as f:
            for line in f:
                if line.strip() and not line.startswith("#"):
                    key, value = line.strip().split("=", 1)
                    settings_data[key.upper()] = value

    # Override with environment variables
    for key, value in os.environ.items():
        if key.startswith("TACHIKOMA_"):
            settings_key = key[10:].lower()  # Remove TACHIKOMA_ prefix
            settings_data[settings_key] = value

    return Settings(**settings_data)  # type: ignore


def save_settings(settings: Settings, file_path: str = "tachikoma_config.json") -> None:
    """Save settings to a JSON file."""
    with open(file_path, "w") as f:
        f.write(settings.json(indent=2))
