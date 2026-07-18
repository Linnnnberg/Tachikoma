"""
Enhanced multi-dimensional agent classes for Tachikoma.

This module contains the core agent classes and data structures
with support for roles, personalities, political spectrum, and
correlated parameters for realistic multi-agent interactions.
"""

from typing import List, Dict, Any, Optional
from enum import Enum
from pydantic import BaseModel, Field


class PoliticalSpectrum(Enum):
    """Political orientation spectrum"""
    FAR_LEFT = "far_left"
    LEFT = "left" 
    CENTER_LEFT = "center_left"
    CENTER = "center"
    CENTER_RIGHT = "center_right"
    RIGHT = "right"
    FAR_RIGHT = "far_right"
    APOLITICAL = "apolitical"


class EconomicView(Enum):
    """Economic policy orientation"""
    SOCIALIST = "socialist"
    SOCIAL_DEMOCRAT = "social_democrat"
    MIXED_ECONOMY = "mixed_economy"
    CAPITALIST = "capitalist"
    LAISSEZ_FAIRE = "laissez_faire"
    APOLITICAL = "apolitical"


class SocialView(Enum):
    """Social policy orientation"""
    PROGRESSIVE = "progressive"
    MODERATE = "moderate"
    CONSERVATIVE = "conservative"
    TRADITIONALIST = "traditionalist"
    APOLITICAL = "apolitical"


class AgentRole(BaseModel):
    """Functional role based on expertise/position needed"""
    name: str
    domain: str
    responsibilities: List[str]
    required_expertise: List[str]
    decision_authority: str  # "Advisory", "Executive", "Operational"
    context_specific: bool = False  # True if role is context-dependent


class AgentPersonality(BaseModel):
    """Personality traits that affect communication style"""
    communication_style: str  # "Direct", "Diplomatic", "Analytical", "Creative"
    risk_tolerance: str  # "Conservative", "Moderate", "Aggressive"
    collaboration_style: str  # "Competitive", "Collaborative", "Independent"
    principles: List[str]  # Core values that guide decisions


class PoliticalProfile(BaseModel):
    """Political and ideological orientation (optional)"""
    political_spectrum: Optional[PoliticalSpectrum] = None
    economic_view: Optional[EconomicView] = None
    social_view: Optional[SocialView] = None
    key_issues: List[str] = Field(default_factory=list)
    ideological_principles: List[str] = Field(default_factory=list)


class CorrelatedParameters(BaseModel):
    """Parameters that correlate with political/ideological views"""
    environmental_stance: Optional[str] = None  # "Environmentalist", "Pragmatic", "Skeptical"
    technology_approach: Optional[str] = None  # "Tech-optimist", "Cautious", "Skeptical"
    globalization_view: Optional[str] = None  # "Globalist", "Moderate", "Nationalist"
    regulation_preference: Optional[str] = None  # "Pro-regulation", "Balanced", "Deregulation"
    social_equality_focus: Optional[str] = None  # "High", "Moderate", "Low"
    market_trust: Optional[str] = None  # "High", "Moderate", "Low"


class AgentDefinition(BaseModel):
    """Complete agent definition with all dimensions"""
    role: AgentRole
    personality: Optional[AgentPersonality] = None
    political_profile: Optional[PoliticalProfile] = None
    correlated_params: Optional[CorrelatedParameters] = None
    custom_instructions: str = ""
    context_tags: List[str] = Field(default_factory=list)  # "startup", "corporate", "academic"


class AgentState(BaseModel):
    """Current state of an agent during conversation"""
    definition: AgentDefinition
    performance_score: float = 0.0
    resource_allocation: float = 1.0
    conversation_history: List[Dict[str, Any]] = Field(default_factory=list)
    current_focus: Optional[str] = None
    energy_level: float = 1.0  # For dynamic resource allocation


# Legacy compatibility - keeping old classes for backward compatibility
class AgentCharacter(BaseModel):
    """Legacy character definition - use AgentDefinition instead"""
    name: str
    personality: str
    principles: List[str]
    expertise: List[str]
    communication_style: str
