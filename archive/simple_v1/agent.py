"""
Simplified agent classes for Phase 1.

This module contains simplified agent definitions focused on
essential functionality for initial testing.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


class AgentRole(Enum):
    """Simplified agent roles."""
    LEGAL = "legal"
    MARKETING = "marketing"
    TECHNICAL = "technical"
    GENERAL = "general"


class PersonalityType(Enum):
    """Simplified personality types."""
    ANALYTICAL = "analytical"
    CREATIVE = "creative"
    PRACTICAL = "practical"
    COLLABORATIVE = "collaborative"


@dataclass
class SimpleAgent:
    """Simplified agent definition for Phase 1."""
    
    name: str
    role: AgentRole
    personality: PersonalityType
    expertise: List[str]
    performance_score: float = 0.0
    resource_allocation: float = 0.0
    message_count: int = 0
    task_completion_rate: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert agent to dictionary."""
        return {
            "name": self.name,
            "role": self.role.value,
            "personality": self.personality.value,
            "expertise": self.expertise,
            "performance_score": self.performance_score,
            "resource_allocation": self.resource_allocation,
            "message_count": self.message_count,
            "task_completion_rate": self.task_completion_rate
        }
    
    @classmethod
    def create_legal_consultant(cls, name: str) -> "SimpleAgent":
        """Create a legal consultant agent."""
        return cls(
            name=name,
            role=AgentRole.LEGAL,
            personality=PersonalityType.ANALYTICAL,
            expertise=["Legal Compliance", "Contract Review", "Risk Assessment"],
            performance_score=0.8
        )
    
    @classmethod
    def create_marketing_strategist(cls, name: str) -> "SimpleAgent":
        """Create a marketing strategist agent."""
        return cls(
            name=name,
            role=AgentRole.MARKETING,
            personality=PersonalityType.CREATIVE,
            expertise=["Digital Marketing", "Brand Strategy", "Market Analysis"],
            performance_score=0.7
        )
    
    @classmethod
    def create_technical_architect(cls, name: str) -> "SimpleAgent":
        """Create a technical architect agent."""
        return cls(
            name=name,
            role=AgentRole.TECHNICAL,
            personality=PersonalityType.PRACTICAL,
            expertise=["System Architecture", "Software Development", "Technical Planning"],
            performance_score=0.9
        )
    
    def get_role_description(self) -> str:
        """Get a description of the agent's role."""
        descriptions = {
            AgentRole.LEGAL: "Legal consultant focused on compliance and risk management",
            AgentRole.MARKETING: "Marketing strategist focused on brand and market growth",
            AgentRole.TECHNICAL: "Technical architect focused on system design and development",
            AgentRole.GENERAL: "General purpose agent for various tasks"
        }
        return descriptions.get(self.role, "Unknown role")
    
    def get_personality_description(self) -> str:
        """Get a description of the agent's personality."""
        descriptions = {
            PersonalityType.ANALYTICAL: "Thinks logically and focuses on data-driven decisions",
            PersonalityType.CREATIVE: "Generates innovative ideas and creative solutions",
            PersonalityType.PRACTICAL: "Focuses on practical, implementable solutions",
            PersonalityType.COLLABORATIVE: "Works well with others and builds consensus"
        }
        return descriptions.get(self.personality, "Unknown personality")
