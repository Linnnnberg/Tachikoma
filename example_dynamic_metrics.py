#!/usr/bin/env python3
"""
Example usage of the enhanced Tachikoma dynamic metrics system.

This script demonstrates the dynamic metrics system with context-aware
metric selection and weighting.
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
from tachikoma.core.metrics import DynamicMetricsSystem


async def create_diverse_team():
    """Create a diverse team with different roles and characteristics."""
    
    # Legal Consultant (Role-focused, compliance-oriented)
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
    
    # Marketing Strategist (Creative, market-focused)
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
    
    # Technical Architect (Technical, innovation-focused)
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


async def demonstrate_dynamic_metrics():
    """Demonstrate the dynamic metrics system."""
    
    print("Tachikoma Dynamic Metrics System Demo")
    print("=" * 50)
    
    # Create team
    print("\nCreating diverse team...")
    agents = await create_diverse_team()
    
    # Initialize system components
    orchestrator = TachikomaOrchestrator()
    scorer = ResourceScorer()
    message_passing = MessagePassing()
    debate_protocol = DebateProtocol(message_passing)
    role_suggester = RoleSuggestionEngine()
    
    # Set up peer collector
    scorer.set_peer_collector(message_passing)
    
    # Add agents to orchestrator
    print("\nAdding agents to system...")
    agent_ids = {}
    for agent_id, agent_def in agents.items():
        actual_id = await orchestrator.add_agent(agent_def)
        agent_ids[actual_id] = agent_def
        print(f"  Added {agent_def.role.name} ({actual_id})")
    
    # Demonstrate different contexts
    contexts = [
        ("legal_compliance", "Legal compliance review"),
        ("technical_architecture", "System architecture design"),
        ("marketing_strategy", "Marketing campaign planning"),
        ("brainstorming", "Creative brainstorming session"),
        ("decision_making", "Strategic decision making")
    ]
    
    print("\n" + "="*60)
    print("DYNAMIC METRICS ANALYSIS")
    print("="*60)
    
    for context, description in contexts:
        print(f"\nContext: {description}")
        print("-" * 40)
        
        # Get relevant metrics for each agent in this context
        for agent_id, agent_def in agent_ids.items():
            role = agent_def.role
            print(f"\n{role.name} ({agent_id}):")
            
            # Get metric analysis
            metric_analysis = await scorer.get_metric_analysis(agent_id, context, role)
            print(f"  Relevant metrics: {len(metric_analysis['relevant_metrics'])}")
            print(f"  Metrics: {', '.join(metric_analysis['relevant_metrics'][:5])}...")
            
            # Show top weighted metrics
            weights = metric_analysis['metric_weights']
            top_metrics = sorted(weights.items(), key=lambda x: x[1], reverse=True)[:3]
            print(f"  Top weighted metrics:")
            for metric, weight in top_metrics:
                print(f"    {metric}: {weight:.3f}")
    
    print("\n" + "="*60)
    print("RESOURCE ALLOCATION COMPARISON")
    print("="*60)
    
    # Create agent states for resource allocation
    agent_states = {agent_id: AgentState(
        definition=agent_def,
        performance_score=0.8,
        resource_allocation=0.0,
        conversation_history=[]
    ) for agent_id, agent_def in agent_ids.items()}
    
    # Compare legacy vs dynamic allocation
    print("\nLegacy Resource Allocation (fixed weights):")
    legacy_allocation = await scorer.allocate_resources(agent_states, 100.0)
    for agent_id, resources in legacy_allocation.items():
        role_name = agent_ids[agent_id].role.name
        print(f"  {role_name}: {resources:.1f} resources")
    
    print("\nDynamic Resource Allocation (context-aware):")
    for context, description in contexts[:3]:  # Test first 3 contexts
        print(f"\n  Context: {description}")
        dynamic_allocation = await scorer.allocate_resources_dynamic(
            agent_states, 100.0, context
        )
        for agent_id, resources in dynamic_allocation.items():
            role_name = agent_ids[agent_id].role.name
            print(f"    {role_name}: {resources:.1f} resources")
    
    print("\n" + "="*60)
    print("METRIC EVOLUTION DEMONSTRATION")
    print("="*60)
    
    # Show how metrics change based on context
    print("\nMetric Weight Changes by Context:")
    print("-" * 40)
    
    # Get a sample agent for analysis
    sample_agent_id = list(agent_ids.keys())[0]
    sample_role = agent_ids[sample_agent_id].role
    
    for context, description in contexts:
        analysis = await scorer.get_metric_analysis(sample_agent_id, context, sample_role)
        weights = analysis['metric_weights']
        
        print(f"\n{description}:")
        # Show how weights change for key metrics
        key_metrics = ["response_quality", "consensus_building", "idea_generation", "compliance_accuracy"]
        for metric in key_metrics:
            if metric in weights:
                print(f"  {metric}: {weights[metric]:.3f}")
    
    print("\n" + "="*60)
    print("ROLE-SPECIFIC METRIC ANALYSIS")
    print("="*60)
    
    # Show role-specific metrics
    for agent_id, agent_def in agent_ids.items():
        role = agent_def.role
        print(f"\n{role.name} Role-Specific Metrics:")
        
        # Get metrics for a role-relevant context
        if role.domain.lower() == "legal":
            context = "legal_compliance"
        elif role.domain.lower() == "technology":
            context = "technical_architecture"
        elif role.domain.lower() == "marketing":
            context = "marketing_strategy"
        else:
            context = "general"
        
        analysis = await scorer.get_metric_analysis(agent_id, context, role)
        role_metrics = [m for m in analysis['relevant_metrics'] if 'compliance' in m or 'technical' in m or 'market' in m]
        
        if role_metrics:
            print(f"  Role-specific metrics: {', '.join(role_metrics)}")
        else:
            print(f"  General metrics: {', '.join(analysis['relevant_metrics'][:3])}...")
    
    print("\n" + "="*60)
    print("SYSTEM PERFORMANCE SUMMARY")
    print("="*60)
    
    # Get overall system performance
    performance = await scorer.get_system_performance()
    print(f"Total agents: {performance['total_agents']}")
    print(f"Average performance: {performance['average_performance']:.2f}")
    print(f"Allocation history entries: {performance['allocation_history_length']}")
    
    print("\nDynamic Metrics System Demo completed successfully!")
    print("\nKey Benefits Demonstrated:")
    print("+ Context-aware metric selection")
    print("+ Role-specific metric weighting")
    print("+ Dynamic resource allocation")
    print("+ Multiple measurement methods")
    print("+ Adaptive performance evaluation")


if __name__ == "__main__":
    asyncio.run(demonstrate_dynamic_metrics())
