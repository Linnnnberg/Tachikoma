"""
Simplified orchestrator for Phase 1.

This module contains a simplified orchestrator that coordinates
the basic multi-agent system.
"""

from typing import List, Dict, Any, Optional
from .agent import SimpleAgent, AgentRole, PersonalityType
from .metrics import SimpleScorer
from .communication import SimpleCommunication, MessageType, SimpleDebate


class SimpleOrchestrator:
    """Simplified orchestrator for Phase 1 multi-agent system."""
    
    def __init__(self):
        """Initialize the simple orchestrator."""
        self.agents: Dict[str, SimpleAgent] = {}
        self.scorer = SimpleScorer()
        self.communication = SimpleCommunication()
        self.conversation_state = "idle"
        self.current_topic = None
    
    def add_agent(self, agent: SimpleAgent) -> str:
        """Add an agent to the system."""
        self.agents[agent.name] = agent
        return agent.name
    
    def remove_agent(self, agent_name: str) -> bool:
        """Remove an agent from the system."""
        if agent_name in self.agents:
            del self.agents[agent_name]
            return True
        return False
    
    def get_agent(self, agent_name: str) -> Optional[SimpleAgent]:
        """Get an agent by name."""
        return self.agents.get(agent_name)
    
    def list_agents(self) -> List[SimpleAgent]:
        """Get list of all agents."""
        return list(self.agents.values())
    
    def send_message(self, from_agent: str, to_agent: str, content: str) -> str:
        """Send a message between agents."""
        if from_agent not in self.agents:
            raise ValueError(f"Agent {from_agent} not found")
        if to_agent and to_agent not in self.agents:
            raise ValueError(f"Agent {to_agent} not found")
        
        message_id = self.communication.send_message(from_agent, to_agent, content)
        
        # Update agent message count
        if from_agent in self.agents:
            self.agents[from_agent].message_count += 1
        
        return message_id
    
    def get_messages(self, agent_name: str, unread_only: bool = False) -> List[Dict[str, Any]]:
        """Get messages for an agent."""
        if agent_name not in self.agents:
            return []
        
        messages = self.communication.get_messages(agent_name, unread_only)
        return [msg.to_dict() for msg in messages]
    
    def start_debate(self, topic: str, participants: List[str], initiator: str) -> str:
        """Start a debate on a topic."""
        # Validate participants
        for participant in participants:
            if participant not in self.agents:
                raise ValueError(f"Agent {participant} not found")
        
        if initiator not in self.agents:
            raise ValueError(f"Agent {initiator} not found")
        
        debate_id = self.communication.start_debate(topic, participants, initiator)
        self.conversation_state = "debate"
        self.current_topic = topic
        
        return debate_id
    
    def add_debate_message(self, debate_id: str, from_agent: str, content: str) -> bool:
        """Add a message to an active debate."""
        if from_agent not in self.agents:
            return False
        
        success = self.communication.add_debate_message(debate_id, from_agent, content)
        
        if success:
            # Update agent message count
            self.agents[from_agent].message_count += 1
        
        return success
    
    def cast_vote(self, debate_id: str, agent_name: str, position: str) -> bool:
        """Cast a vote in a debate."""
        if agent_name not in self.agents:
            return False
        
        return self.communication.cast_vote(debate_id, agent_name, position)
    
    def get_debate(self, debate_id: str) -> Optional[SimpleDebate]:
        """Get a debate by ID."""
        return self.communication.get_debate(debate_id)
    
    def get_active_debates(self) -> List[SimpleDebate]:
        """Get all active debates."""
        return self.communication.get_active_debates()
    
    def update_agent_performance(self, agent_name: str, metric_type: str, value: float):
        """Update performance metrics for an agent."""
        if agent_name not in self.agents:
            return
        
        self.scorer.update_metrics(agent_name, metric_type, value)
        
        # Update agent's performance score
        agent = self.agents[agent_name]
        agent.performance_score = self.scorer.calculate_agent_score(agent)
    
    def allocate_resources(self, total_resources: float) -> Dict[str, float]:
        """Allocate resources among all agents."""
        agent_list = list(self.agents.values())
        allocation = self.scorer.allocate_resources(agent_list, total_resources)
        
        # Update agent resource allocations
        for agent_name, resources in allocation.items():
            if agent_name in self.agents:
                self.agents[agent_name].resource_allocation = resources
        
        return allocation
    
    def get_agent_performance(self, agent_name: str) -> Dict[str, Any]:
        """Get performance metrics for an agent."""
        if agent_name not in self.agents:
            return {}
        
        agent = self.agents[agent_name]
        metrics = self.scorer.get_agent_metrics(agent_name)
        
        return {
            "agent": agent.to_dict(),
            "metrics": metrics.to_dict(),
            "performance_score": agent.performance_score
        }
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status."""
        system_summary = self.scorer.get_system_summary()
        
        return {
            "total_agents": len(self.agents),
            "conversation_state": self.conversation_state,
            "current_topic": self.current_topic,
            "active_debates": len(self.communication.get_active_debates()),
            "system_performance": system_summary,
            "agents": [agent.to_dict() for agent in self.agents.values()]
        }
    
    def simulate_agent_interaction(self, agent_name: str, context: str) -> str:
        """Simulate an agent's response to a context."""
        if agent_name not in self.agents:
            return "Agent not found"
        
        agent = self.agents[agent_name]
        
        # Simple response generation based on agent characteristics
        if agent.role == AgentRole.LEGAL:
            if "compliance" in context.lower() or "legal" in context.lower():
                return f"As a legal consultant, I recommend reviewing compliance requirements carefully."
            else:
                return f"From a legal perspective, we should consider potential risks and compliance issues."
        
        elif agent.role == AgentRole.MARKETING:
            if "marketing" in context.lower() or "brand" in context.lower():
                return f"As a marketing strategist, I suggest focusing on brand positioning and market analysis."
            else:
                return f"From a marketing perspective, we should consider customer needs and market trends."
        
        elif agent.role == AgentRole.TECHNICAL:
            if "technical" in context.lower() or "system" in context.lower():
                return f"As a technical architect, I recommend a systematic approach to system design."
            else:
                return f"From a technical perspective, we should consider scalability and maintainability."
        
        else:
            return f"I'll analyze this situation and provide my perspective."
    
    def run_simple_scenario(self, scenario: str) -> Dict[str, Any]:
        """Run a simple scenario with the agents."""
        results = {
            "scenario": scenario,
            "steps": [],
            "final_state": {}
        }
        
        # Step 1: Start a debate
        participants = list(self.agents.keys())
        if len(participants) < 2:
            results["steps"].append("Not enough agents for debate")
            return results
        
        initiator = participants[0]
        debate_id = self.start_debate(scenario, participants, initiator)
        results["steps"].append(f"Started debate: {scenario}")
        
        # Step 2: Agents contribute to debate
        for i, agent_name in enumerate(participants[1:], 1):
            response = self.simulate_agent_interaction(agent_name, scenario)
            self.add_debate_message(debate_id, agent_name, response)
            results["steps"].append(f"{agent_name}: {response}")
        
        # Step 3: Cast votes
        positions = ["Option A", "Option B", "Option C"]
        for i, agent_name in enumerate(participants):
            position = positions[i % len(positions)]
            self.cast_vote(debate_id, agent_name, position)
            results["steps"].append(f"{agent_name} voted: {position}")
        
        # Step 4: Get final state
        debate = self.get_debate(debate_id)
        results["final_state"] = debate.get_summary() if debate else {}
        
        return results
