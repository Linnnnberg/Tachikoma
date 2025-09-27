"""
Core Tachikoma system components.

This module contains the fundamental classes and systems that power the
Tachikoma multi-agent AI system.
"""

from .orchestrator import TachikomaOrchestrator
from .agent import AgentCharacter, AgentState, AgentRole
from .scorer import ResourceScorer
from .suggester import RoleSuggestionEngine
from .communication import MessagePassing, DebateProtocol

__all__ = [
    "TachikomaOrchestrator",
    "AgentCharacter",
    "AgentState",
    "AgentRole",
    "ResourceScorer",
    "RoleSuggestionEngine",
    "MessagePassing",
    "DebateProtocol",
]
