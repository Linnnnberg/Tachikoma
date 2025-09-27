"""
Agent classes and data structures for Tachikoma.

This module contains the core agent classes and data structures
used throughout the Tachikoma system.
"""

from typing import List, Dict, Any
from enum import Enum
from pydantic import BaseModel


class AgentCharacter(BaseModel):
    """Character definition for an agent."""

    name: str
    personality: str
    principles: List[str]
    expertise: List[str]
    communication_style: str


class AgentState(BaseModel):
    """Current state of an agent."""

    character: AgentCharacter
    performance_score: float
    resource_allocation: float
    conversation_history: List[Dict[str, Any]]


class AgentRole(Enum):
    """Enumeration of possible agent roles."""

    PLANNER = "planner"
    WRITER = "writer"
    SKEPTIC = "skeptic"
    ARBITER = "arbiter"
    CUSTOM = "custom"
