#!/usr/bin/env python3
"""
Simple Phase 1 Tachikoma System Demo.

This script demonstrates the simplified Phase 1 system with
basic multi-agent functionality for initial testing.
"""

import asyncio
import sys
import os

# Add the tachikoma package to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tachikoma'))

from tachikoma.simple.agent import SimpleAgent, AgentRole, PersonalityType
from tachikoma.simple.orchestrator import SimpleOrchestrator
from tachikoma.simple.communication import MessageType


def create_simple_team():
    """Create a simple team of agents for testing."""
    
    # Legal Consultant
    legal_agent = SimpleAgent.create_legal_consultant("Alice")
    
    # Marketing Strategist  
    marketing_agent = SimpleAgent.create_marketing_strategist("Bob")
    
    # Technical Architect
    tech_agent = SimpleAgent.create_technical_architect("Charlie")
    
    return [legal_agent, marketing_agent, tech_agent]


def demonstrate_simple_system():
    """Demonstrate the simplified Phase 1 system."""
    
    print("Tachikoma Simple Phase 1 System Demo")
    print("=" * 50)
    
    # Create team
    print("\nCreating simple team...")
    agents = create_simple_team()
    
    # Initialize orchestrator
    orchestrator = SimpleOrchestrator()
    
    # Add agents
    print("\nAdding agents to system...")
    for agent in agents:
        orchestrator.add_agent(agent)
        print(f"  Added {agent.name} ({agent.role.value}) - {agent.personality.value}")
    
    # Show agent details
    print("\nAgent Details:")
    print("-" * 30)
    for agent in agents:
        print(f"\n{agent.name}:")
        print(f"  Role: {agent.get_role_description()}")
        print(f"  Personality: {agent.get_personality_description()}")
        print(f"  Expertise: {', '.join(agent.expertise)}")
        print(f"  Performance Score: {agent.performance_score:.2f}")
    
    # Demonstrate messaging
    print("\n" + "="*50)
    print("MESSAGING SYSTEM")
    print("="*50)
    
    print("\nSending messages...")
    
    # Alice sends message to Bob
    msg1 = orchestrator.send_message("Alice", "Bob", "Hi Bob, I need your input on our marketing compliance requirements.")
    print(f"  Alice -> Bob: Message sent (ID: {msg1})")
    
    # Bob responds
    msg2 = orchestrator.send_message("Bob", "Alice", "Hi Alice, I'll review our marketing materials for compliance issues.")
    print(f"  Bob -> Alice: Message sent (ID: {msg2})")
    
    # Charlie joins the conversation
    msg3 = orchestrator.send_message("Charlie", "Alice", "Alice, I can help with the technical aspects of compliance implementation.")
    print(f"  Charlie -> Alice: Message sent (ID: {msg3})")
    
    # Show messages for Alice
    print("\nMessages for Alice:")
    alice_messages = orchestrator.get_messages("Alice")
    for msg in alice_messages[:3]:  # Show first 3 messages
        print(f"  From {msg['from_agent']}: {msg['content']}")
    
    # Demonstrate debate system
    print("\n" + "="*50)
    print("DEBATE SYSTEM")
    print("="*50)
    
    print("\nStarting a debate...")
    debate_id = orchestrator.start_debate(
        "Should we prioritize speed or security in our new product?",
        ["Alice", "Bob", "Charlie"],
        "Alice"
    )
    print(f"  Debate started (ID: {debate_id})")
    
    # Agents contribute to debate
    print("\nAgents contributing to debate...")
    
    # Alice (Legal) - Security focused
    orchestrator.add_debate_message(debate_id, "Alice", "From a legal perspective, security should be our top priority to avoid compliance issues.")
    print("  Alice: Security should be our top priority")
    
    # Bob (Marketing) - Speed focused
    orchestrator.add_debate_message(debate_id, "Bob", "From a marketing perspective, we need to get to market quickly to capture market share.")
    print("  Bob: We need speed to capture market share")
    
    # Charlie (Technical) - Balanced approach
    orchestrator.add_debate_message(debate_id, "Charlie", "As a technical architect, I believe we can implement both with proper planning and architecture.")
    print("  Charlie: We can implement both with proper planning")
    
    # Cast votes
    print("\nCasting votes...")
    orchestrator.cast_vote(debate_id, "Alice", "Security First")
    orchestrator.cast_vote(debate_id, "Bob", "Speed First") 
    orchestrator.cast_vote(debate_id, "Charlie", "Balanced Approach")
    print("  All agents have voted")
    
    # Get debate results
    debate = orchestrator.get_debate(debate_id)
    if debate:
        print(f"\nDebate Results:")
        print(f"  Topic: {debate.topic}")
        print(f"  Messages: {len(debate.messages)}")
        print(f"  Votes: {debate.votes}")
        print(f"  Consensus: {debate.consensus_reached}")
        if debate.consensus_decision:
            print(f"  Decision: {debate.consensus_decision}")
    
    # Demonstrate performance tracking
    print("\n" + "="*50)
    print("PERFORMANCE TRACKING")
    print("="*50)
    
    print("\nUpdating performance metrics...")
    
    # Update metrics for each agent
    orchestrator.update_agent_performance("Alice", "response_quality", 0.9)
    orchestrator.update_agent_performance("Alice", "collaboration", 0.8)
    orchestrator.update_agent_performance("Alice", "task_completion", 0.85)
    orchestrator.update_agent_performance("Alice", "communication", 0.9)
    
    orchestrator.update_agent_performance("Bob", "response_quality", 0.8)
    orchestrator.update_agent_performance("Bob", "collaboration", 0.9)
    orchestrator.update_agent_performance("Bob", "task_completion", 0.75)
    orchestrator.update_agent_performance("Bob", "communication", 0.85)
    
    orchestrator.update_agent_performance("Charlie", "response_quality", 0.95)
    orchestrator.update_agent_performance("Charlie", "collaboration", 0.7)
    orchestrator.update_agent_performance("Charlie", "task_completion", 0.9)
    orchestrator.update_agent_performance("Charlie", "communication", 0.8)
    
    print("  Performance metrics updated for all agents")
    
    # Show performance for each agent
    print("\nAgent Performance:")
    for agent_name in ["Alice", "Bob", "Charlie"]:
        perf = orchestrator.get_agent_performance(agent_name)
        print(f"\n{agent_name}:")
        print(f"  Overall Score: {perf['performance_score']:.2f}")
        metrics = perf['metrics']
        print(f"  Response Quality: {metrics['response_quality']:.2f}")
        print(f"  Collaboration: {metrics['collaboration']:.2f}")
        print(f"  Task Completion: {metrics['task_completion']:.2f}")
        print(f"  Communication: {metrics['communication']:.2f}")
    
    # Demonstrate resource allocation
    print("\n" + "="*50)
    print("RESOURCE ALLOCATION")
    print("="*50)
    
    print("\nAllocating resources...")
    allocation = orchestrator.allocate_resources(100.0)
    
    print("Resource Allocation Results:")
    for agent_name, resources in allocation.items():
        print(f"  {agent_name}: {resources:.1f} resources")
    
    # Demonstrate scenario simulation
    print("\n" + "="*50)
    print("SCENARIO SIMULATION")
    print("="*50)
    
    print("\nRunning scenario: 'Should we invest in AI technology?'")
    scenario_results = orchestrator.run_simple_scenario("Should we invest in AI technology?")
    
    print("\nScenario Steps:")
    for i, step in enumerate(scenario_results['steps'], 1):
        print(f"  {i}. {step}")
    
    print(f"\nFinal State:")
    final_state = scenario_results['final_state']
    print(f"  Consensus Reached: {final_state.get('consensus_reached', False)}")
    print(f"  Total Messages: {final_state.get('message_count', 0)}")
    
    # System status
    print("\n" + "="*50)
    print("SYSTEM STATUS")
    print("="*50)
    
    status = orchestrator.get_system_status()
    print(f"Total Agents: {status['total_agents']}")
    print(f"Conversation State: {status['conversation_state']}")
    print(f"Active Debates: {status['active_debates']}")
    print(f"Average Performance: {status['system_performance']['average_performance']:.2f}")
    
    print("\nSimple Phase 1 Demo completed successfully!")
    print("\nKey Features Demonstrated:")
    print("+ Basic agent roles and personalities")
    print("+ Simple messaging system")
    print("+ Basic debate and voting")
    print("+ Performance tracking")
    print("+ Resource allocation")
    print("+ Scenario simulation")


if __name__ == "__main__":
    demonstrate_simple_system()
