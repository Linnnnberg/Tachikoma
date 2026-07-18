#!/usr/bin/env python3
"""
Example usage of the enhanced Tachikoma multi-agent system.

This script demonstrates the enhanced multi-dimensional agent architecture
with roles, personalities, political spectrum, and correlated parameters.
"""

import asyncio
import sys
import os

# Add the tachikoma package to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tachikoma'))

from tachikoma.core.agent import (
    AgentDefinition, AgentRole, AgentPersonality, PoliticalProfile, 
    CorrelatedParameters, AgentState, PoliticalSpectrum, EconomicView, SocialView
)
from tachikoma.core.orchestrator import TachikomaOrchestrator
from tachikoma.core.scorer import ResourceScorer
from tachikoma.core.communication import MessagePassing, DebateProtocol, MessageType, MessagePriority
from tachikoma.core.suggester import RoleSuggestionEngine


async def create_startup_team():
    """Create a startup team with diverse agents."""
    
    # Legal Consultant (Role-focused, no strong personality needed)
    legal_role = AgentRole(
        name="Legal Consultant",
        domain="Legal",
        responsibilities=[
            "Ensure company compliance with local laws",
            "Review contracts and legal documents",
            "Provide legal advice on business decisions"
        ],
        required_expertise=["Corporate Law", "Contract Law", "Compliance"],
        decision_authority="Advisory",
        context_specific=True
    )
    
    legal_agent = AgentDefinition(
        role=legal_role,
        personality=None,  # Role-focused, no personality needed
        political_profile=None,  # Apolitical role
        correlated_parameters=None
    )
    
    # Marketing Strategist (Role + Personality)
    marketing_role = AgentRole(
        name="Marketing Strategist",
        domain="Marketing",
        responsibilities=[
            "Develop marketing strategies",
            "Analyze market trends",
            "Create brand positioning"
        ],
        required_expertise=["Digital Marketing", "Brand Management", "Market Research"],
        decision_authority="Operational",
        context_specific=True
    )
    
    marketing_personality = AgentPersonality(
        communication_style="Creative",
        risk_tolerance="Moderate",
        collaboration_style="Collaborative",
        principles=["Innovation", "Customer Focus", "Data-Driven Decisions"]
    )
    
    marketing_political = PoliticalProfile(
        political_spectrum=PoliticalSpectrum.CENTER,
        economic_view=EconomicView.MIXED_ECONOMY,
        social_view=SocialView.PROGRESSIVE,
        cultural_background="urban_tech"
    )
    
    marketing_agent = AgentDefinition(
        role=marketing_role,
        personality=marketing_personality,
        political_profile=marketing_political,
        correlated_parameters=CorrelatedParameters(
            risk_tolerance=0.7,
            innovation_preference=0.8,
            collaboration_level=0.9
        )
    )
    
    # Technical Architect (Role + Personality + Political views)
    tech_role = AgentRole(
        name="Technical Architect",
        domain="Technology",
        responsibilities=[
            "Design system architecture",
            "Make technical decisions",
            "Lead development team"
        ],
        required_expertise=["Software Architecture", "Cloud Computing", "DevOps"],
        decision_authority="Executive",
        context_specific=True
    )
    
    tech_personality = AgentPersonality(
        communication_style="Analytical",
        risk_tolerance="Moderate",
        collaboration_style="Independent",
        principles=["Technical Excellence", "Innovation", "Efficiency"]
    )
    
    tech_political = PoliticalProfile(
        political_spectrum=PoliticalSpectrum.CENTER_LEFT,
        economic_view=EconomicView.MIXED_ECONOMY,
        social_view=SocialView.PROGRESSIVE,
        cultural_background="tech_industry"
    )
    
    tech_agent = AgentDefinition(
        role=tech_role,
        personality=tech_personality,
        political_profile=tech_political,
        correlated_parameters=CorrelatedParameters(
            risk_tolerance=0.6,
            innovation_preference=0.9,
            collaboration_level=0.7
        )
    )
    
    return {
        "legal": legal_agent,
        "marketing": marketing_agent,
        "tech": tech_agent
    }


async def demonstrate_system():
    """Demonstrate the enhanced multi-agent system."""
    
    print("Tachikoma Enhanced Multi-Agent System Demo")
    print("=" * 50)
    
    # Create startup team
    print("\nCreating startup team...")
    agents = await create_startup_team()
    
    # Initialize system components
    orchestrator = TachikomaOrchestrator()
    scorer = ResourceScorer()
    message_passing = MessagePassing()
    debate_protocol = DebateProtocol(message_passing)
    role_suggester = RoleSuggestionEngine()
    
    # Add agents to orchestrator
    print("\nAdding agents to system...")
    agent_ids = {}
    for agent_id, agent_def in agents.items():
        actual_id = await orchestrator.add_agent(agent_def)
        agent_ids[actual_id] = agent_def
        print(f"  Added {agent_def.role.name} ({actual_id})")
    
    # Demonstrate resource allocation
    print("\nDemonstrating resource allocation...")
    agent_states = {agent_id: AgentState(
        definition=agent_def,
        performance_score=0.8,
        resource_allocation=0.0,
        conversation_history=[]
    ) for agent_id, agent_def in agent_ids.items()}
    
    allocation = await scorer.allocate_resources(agent_states, 100.0)
    for agent_id, resources in allocation.items():
        print(f"  {agent_id}: {resources:.1f} resources")
    
    # Demonstrate communication
    print("\nDemonstrating communication system...")
    
    # Send a message
    message_id = await message_passing.send_message(
        from_agent="tech",
        to_agent="marketing",
        content="We need to discuss the technical requirements for the new feature.",
        message_type=MessageType.REQUEST,
        priority=MessagePriority.HIGH
    )
    print(f"  Sent message: {message_id}")
    
    # Start a debate
    print("\nStarting a debate session...")
    debate_participants = list(agent_ids.keys())
    debate_result = await debate_protocol.initiate_debate(
        agents=debate_participants,
        topic="Should we prioritize speed or security in our MVP?",
        initiator=debate_participants[0],  # Use first agent as initiator
        strategy="collaborative"
    )
    print(f"  Debate started: {debate_result['session_id']}")
    print(f"  Topic: {debate_result['topic']}")
    print(f"  Participants: {debate_result['participants']}")
    
    # Add debate messages
    participant_list = list(agent_ids.keys())
    await debate_protocol.facilitate_negotiation(
        debate_result['session_id'],
        participant_list[0],  # First agent
        "Security should be our top priority to avoid legal issues later.",
        "Security First"
    )
    
    await debate_protocol.facilitate_negotiation(
        debate_result['session_id'],
        participant_list[1] if len(participant_list) > 1 else participant_list[0],  # Second agent
        "We need to get to market quickly to capture market share.",
        "Speed First"
    )
    
    await debate_protocol.facilitate_negotiation(
        debate_result['session_id'],
        participant_list[2] if len(participant_list) > 2 else participant_list[0],  # Third agent
        "We can implement both with proper architecture planning.",
        "Balanced Approach"
    )
    
    # Cast votes
    await message_passing.cast_vote(debate_result['session_id'], participant_list[0], "Security First")
    if len(participant_list) > 1:
        await message_passing.cast_vote(debate_result['session_id'], participant_list[1], "Speed First")
    if len(participant_list) > 2:
        await message_passing.cast_vote(debate_result['session_id'], participant_list[2], "Balanced Approach")
    
    # Get debate summary
    debate_summary = await message_passing.get_debate_summary(debate_result['session_id'])
    print(f"\nDebate Summary:")
    print(f"  Messages: {debate_summary['message_count']}")
    print(f"  Votes: {debate_summary['votes']}")
    print(f"  Consensus: {debate_summary['consensus_reached']}")
    
    # Demonstrate role suggestion
    print("\nDemonstrating role suggestion...")
    context = "We need someone to handle customer support and user experience"
    # Convert agent_ids to AgentState objects for the suggester
    agent_states = {agent_id: AgentState(
        definition=agent_def,
        performance_score=0.8,
        resource_allocation=0.0,
        conversation_history=[]
    ) for agent_id, agent_def in agent_ids.items()}
    
    suggestions = await role_suggester.suggest_agents_for_context(context, agent_states)
    if suggestions:
        print(f"  Suggested agents: {len(suggestions)} new agents suggested")
        for i, suggestion in enumerate(suggestions[:3]):  # Show first 3 suggestions
            print(f"    {i+1}. {suggestion.role.name} - {suggestion.role.domain}")
    
    # Get system performance
    print("\nSystem Performance:")
    performance = await scorer.get_system_performance()
    print(f"  Total agents: {performance['total_agents']}")
    print(f"  Average performance: {performance['average_performance']:.2f}")
    
    print("\nDemo completed successfully!")


if __name__ == "__main__":
    asyncio.run(demonstrate_system())
