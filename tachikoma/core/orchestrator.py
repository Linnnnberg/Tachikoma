"""
Enhanced Tachikoma Orchestrator - Multi-dimensional agent coordinator.

This module contains the main orchestrator class that coordinates
agents with roles, personalities, political spectrum, and correlated
parameters for realistic multi-agent interactions.
"""

from typing import Dict, List, Optional, Any
import asyncio
from .agent import AgentDefinition, AgentState, AgentRole, AgentPersonality, PoliticalProfile, CorrelatedParameters
from .scorer import ResourceScorer
from .suggester import RoleSuggestionEngine
from .communication import MessagePassing, DebateProtocol


class TachikomaOrchestrator:
    """Enhanced orchestrator for multi-dimensional agent coordination."""

    def __init__(self, settings=None):
        """Initialize the orchestrator with enhanced capabilities."""
        self.settings = settings
        self.agents: Dict[str, AgentState] = {}
        self.input_queue: List[str] = []
        self.conversation_state = "idle"
        self.resource_scorer = ResourceScorer()
        self.role_suggester = RoleSuggestionEngine()
        self.message_passing = MessagePassing()
        self.debate_protocol = DebateProtocol()
        self.conversation_context: Dict[str, Any] = {}

    async def add_agent(self, definition: AgentDefinition) -> str:
        """Dynamically add a new agent with complete definition."""
        agent_id = f"agent_{len(self.agents)}"
        self.agents[agent_id] = AgentState(
            definition=definition,
            performance_score=0.0,
            resource_allocation=1.0,
            conversation_history=[],
            current_focus=None,
            energy_level=1.0
        )
        return agent_id

    async def suggest_agents_for_context(self, context: str, user_preferences: Dict[str, Any] = None) -> List[AgentDefinition]:
        """Suggest agents based on context and multi-dimensional analysis."""
        return await self.role_suggester.suggest_agents_for_context(
            context, 
            self.agents, 
            user_preferences or {}
        )

    async def analyze_conversation_gaps(self, conversation_context: str) -> Optional[Any]:
        """Analyze conversation and suggest new roles/personalities if needed."""
        return await self.role_suggester.analyze_gaps(conversation_context, self.agents)

    async def process_deferred_input(self, user_input: str):
        """Queue user input for processing after current generation."""
        self.input_queue.append(user_input)
        # Process after current agent interactions complete

    async def orchestrate_collaboration(self, task: str, context: str = "") -> str:
        """Orchestrate collaborative competition between agents with different perspectives."""
        self.conversation_context["task"] = task
        self.conversation_context["context"] = context
        
        # Analyze if we need more agents for this task
        suggested_agents = await self.suggest_agents_for_context(context or task)
        
        # If we have suggested agents, add them
        for agent_def in suggested_agents:
            await self.add_agent(agent_def)
        
        # Orchestrate debate and collaboration
        if len(self.agents) > 1:
            debate_result = await self.debate_protocol.initiate_debate(
                list(self.agents.keys()), 
                task
            )
            return await self._synthesize_responses(debate_result)
        
        return "Collaboration result placeholder"

    async def _synthesize_responses(self, debate_result: Dict[str, Any]) -> str:
        """Synthesize responses from multiple agents into final output."""
        # Implementation would synthesize different perspectives
        # based on agent roles, personalities, and political views
        return "Synthesized response placeholder"

    def get_agent_diversity_analysis(self) -> Dict[str, Any]:
        """Analyze diversity of current agent pool."""
        analysis = {
            "total_agents": len(self.agents),
            "role_diversity": set(),
            "personality_diversity": set(),
            "political_diversity": set(),
            "domain_coverage": set()
        }
        
        for agent_state in self.agents.values():
            definition = agent_state.definition
            analysis["role_diversity"].add(definition.role.name)
            analysis["domain_coverage"].add(definition.role.domain)
            
            if definition.personality:
                analysis["personality_diversity"].add(definition.personality.communication_style)
            
            if definition.political_profile and definition.political_profile.political_spectrum:
                analysis["political_diversity"].add(definition.political_profile.political_spectrum.value)
        
        return analysis

    async def remove_agent(self, agent_id: str) -> bool:
        """Remove an agent from the system."""
        if agent_id in self.agents:
            del self.agents[agent_id]
            return True
        return False

    def get_agent_summary(self) -> List[Dict[str, Any]]:
        """Get summary of all agents in the system."""
        summaries = []
        for agent_id, agent_state in self.agents.items():
            definition = agent_state.definition
            summary = {
                "id": agent_id,
                "role": definition.role.name,
                "domain": definition.role.domain,
                "performance_score": agent_state.performance_score,
                "energy_level": agent_state.energy_level,
                "has_personality": definition.personality is not None,
                "has_political_profile": definition.political_profile is not None,
                "context_tags": definition.context_tags
            }
            summaries.append(summary)
        return summaries
