"""
Tachikoma Multi-Agent AI System

A dynamic, character-driven AI system where multiple agents with distinct principles
collaborate while maintaining their ground, featuring intelligent role suggestion,
resource scoring, and deferred user interaction.
"""

__version__ = "0.1.0"
__author__ = "Tachikoma Development Team"
__email__ = "tachikoma@example.com"

from .core.orchestrator import TachikomaOrchestrator
from .core.agent import AgentCharacter, AgentState
from .core.scorer import ResourceScorer
from .core.suggester import RoleSuggestionEngine

__all__ = [
    "TachikomaOrchestrator",
    "AgentCharacter",
    "AgentState",
    "ResourceScorer",
    "RoleSuggestionEngine",
]
