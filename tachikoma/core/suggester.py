"""
Enhanced role suggestion engine for Tachikoma.

This module handles intelligent role suggestion based on
multi-dimensional analysis including roles, personalities,
political spectrum, and correlated parameters.
"""

from typing import Dict, Optional, Any, List
from .agent import AgentState, AgentDefinition, AgentRole, AgentPersonality, PoliticalProfile, CorrelatedParameters, PoliticalSpectrum, EconomicView, SocialView


class RoleSuggestionEngine:
    """Enhanced suggestion engine for multi-dimensional agent analysis."""

    def __init__(self):
        """Initialize the suggestion engine."""
        self.role_templates = self._load_role_templates()
        self.personality_templates = self._load_personality_templates()
        self.political_templates = self._load_political_templates()

    def _load_role_templates(self) -> Dict[str, AgentRole]:
        """Load predefined role templates."""
        return {
            "legal_consultant": AgentRole(
                name="Legal Consultant",
                domain="Legal",
                responsibilities=["Compliance", "Risk assessment", "Regulatory guidance"],
                required_expertise=["Corporate law", "Regulatory compliance", "Risk management"],
                decision_authority="Advisory",
                context_specific=True
            ),
            "marketing_strategist": AgentRole(
                name="Marketing Strategist",
                domain="Marketing",
                responsibilities=["Brand strategy", "Customer acquisition", "Market analysis"],
                required_expertise=["Digital marketing", "Consumer psychology", "Analytics"],
                decision_authority="Operational",
                context_specific=False
            ),
            "technical_architect": AgentRole(
                name="Technical Architect",
                domain="Technology",
                responsibilities=["System design", "Technology decisions", "Scalability planning"],
                required_expertise=["Software architecture", "Cloud platforms", "Security"],
                decision_authority="Executive",
                context_specific=False
            )
        }

    def _load_personality_templates(self) -> Dict[str, AgentPersonality]:
        """Load predefined personality templates."""
        return {
            "analytical": AgentPersonality(
                communication_style="Analytical",
                risk_tolerance="Conservative",
                collaboration_style="Independent",
                principles=["Data-driven decisions", "Evidence-based approach", "Thorough analysis"]
            ),
            "creative": AgentPersonality(
                communication_style="Creative",
                risk_tolerance="Moderate",
                collaboration_style="Collaborative",
                principles=["Innovation", "User experience", "Creative solutions"]
            )
        }

    def _load_political_templates(self) -> Dict[str, PoliticalProfile]:
        """Load predefined political profile templates."""
        return {
            "progressive": PoliticalProfile(
                political_spectrum=PoliticalSpectrum.LEFT,
                economic_view=EconomicView.SOCIAL_DEMOCRAT,
                social_view=SocialView.PROGRESSIVE,
                key_issues=["Social equality", "Environmental protection", "Healthcare access"],
                ideological_principles=["Social justice", "Environmental sustainability", "Inclusive growth"]
            ),
            "conservative": PoliticalProfile(
                political_spectrum=PoliticalSpectrum.RIGHT,
                economic_view=EconomicView.CAPITALIST,
                social_view=SocialView.CONSERVATIVE,
                key_issues=["Economic growth", "Traditional values", "Limited government"],
                ideological_principles=["Free markets", "Individual responsibility", "Traditional institutions"]
            ),
            "apolitical": PoliticalProfile(
                political_spectrum=PoliticalSpectrum.APOLITICAL,
                economic_view=EconomicView.APOLITICAL,
                social_view=SocialView.APOLITICAL,
                key_issues=["Technical excellence", "Professional standards"],
                ideological_principles=["Professional integrity", "Technical competence"]
            )
        }

    async def suggest_agents_for_context(
        self, context: str, existing_agents: Dict[str, AgentState], user_preferences: Dict[str, Any] = None
    ) -> List[AgentDefinition]:
        """Suggest agents based on context and multi-dimensional analysis."""
        suggestions = []
        
        # Analyze context for required roles
        required_roles = self._analyze_context_for_roles(context)
        
        # Check what roles we already have
        existing_roles = {agent.definition.role.name for agent in existing_agents.values()}
        
        # Suggest missing roles
        for role_name in required_roles:
            if role_name not in existing_roles:
                role_template = self.role_templates.get(role_name)
                if role_template:
                    # Create agent definition with appropriate personality and political profile
                    personality = self._suggest_personality_for_role(role_name, context)
                    political_profile = self._suggest_political_profile_for_context(context, user_preferences)
                    correlated_params = self._suggest_correlated_params(political_profile)
                    
                    agent_def = AgentDefinition(
                        role=role_template,
                        personality=personality,
                        political_profile=political_profile,
                        correlated_params=correlated_params,
                        custom_instructions=self._generate_custom_instructions(role_name, context),
                        context_tags=self._extract_context_tags(context)
                    )
                    suggestions.append(agent_def)
        
        return suggestions

    def _analyze_context_for_roles(self, context: str) -> List[str]:
        """Analyze context to determine required roles."""
        context_lower = context.lower()
        required_roles = []
        
        # Legal-related keywords
        if any(keyword in context_lower for keyword in ["legal", "compliance", "regulation", "law", "regulatory"]):
            required_roles.append("legal_consultant")
        
        # Marketing-related keywords
        if any(keyword in context_lower for keyword in ["marketing", "brand", "customer", "market", "advertising"]):
            required_roles.append("marketing_strategist")
        
        # Technology-related keywords
        if any(keyword in context_lower for keyword in ["tech", "software", "system", "architecture", "development"]):
            required_roles.append("technical_architect")
        
        return required_roles

    def _suggest_personality_for_role(self, role_name: str, context: str) -> Optional[AgentPersonality]:
        """Suggest appropriate personality for a role."""
        role_personality_map = {
            "legal_consultant": "analytical",
            "marketing_strategist": "creative",
            "technical_architect": "analytical"
        }
        
        personality_key = role_personality_map.get(role_name)
        return self.personality_templates.get(personality_key) if personality_key else None

    def _suggest_political_profile_for_context(self, context: str, user_preferences: Dict[str, Any] = None) -> Optional[PoliticalProfile]:
        """Suggest political profile based on context and user preferences."""
        # Default to apolitical for technical roles
        return self.political_templates["apolitical"]

    def _suggest_correlated_params(self, political_profile: Optional[PoliticalProfile]) -> Optional[CorrelatedParameters]:
        """Suggest correlated parameters based on political profile."""
        if not political_profile:
            return None
        
        params = CorrelatedParameters()
        params.environmental_stance = "Pragmatic"
        params.social_equality_focus = "Moderate"
        params.regulation_preference = "Balanced"
        
        return params

    def _generate_custom_instructions(self, role_name: str, context: str) -> str:
        """Generate custom instructions for an agent based on role and context."""
        base_instructions = {
            "legal_consultant": "Focus on compliance, risk mitigation, and regulatory requirements. Always consider legal implications first.",
            "marketing_strategist": "Focus on customer needs, brand positioning, and market opportunities. Be creative and data-driven.",
            "technical_architect": "Focus on scalability, security, and technical excellence. Consider long-term maintainability."
        }
        
        return base_instructions.get(role_name, f"Act as a {role_name} with expertise relevant to: {context}")

    def _extract_context_tags(self, context: str) -> List[str]:
        """Extract relevant context tags from the context string."""
        context_lower = context.lower()
        tags = []
        
        if any(keyword in context_lower for keyword in ["startup", "start-up"]):
            tags.append("startup")
        if any(keyword in context_lower for keyword in ["corporate", "enterprise"]):
            tags.append("corporate")
        if any(keyword in context_lower for keyword in ["fintech", "financial technology"]):
            tags.append("fintech")
        
        return tags

    async def analyze_gaps(
        self, context: str, existing_agents: Dict[str, AgentState]
    ) -> Optional[Any]:
        """Analyze conversation gaps and suggest new roles/personalities."""
        return await self.suggest_agents_for_context(context, existing_agents)
