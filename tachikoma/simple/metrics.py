"""
Simplified metrics system for Phase 1.

This module contains a simplified metrics system focused on
essential performance measurement.
"""

from typing import Dict, List, Any
from dataclasses import dataclass
from .agent import SimpleAgent, AgentRole, PersonalityType


@dataclass
class SimpleMetrics:
    """Simplified metrics for agent performance."""
    
    response_quality: float = 0.0      # 0-1, quality of responses
    collaboration: float = 0.0         # 0-1, how well they work with others
    task_completion: float = 0.0       # 0-1, success rate on tasks
    communication: float = 0.0         # 0-1, clarity of communication
    
    def get_overall_score(self) -> float:
        """Get overall performance score."""
        return (self.response_quality + self.collaboration + 
                self.task_completion + self.communication) / 4.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metrics to dictionary."""
        return {
            "response_quality": self.response_quality,
            "collaboration": self.collaboration,
            "task_completion": self.task_completion,
            "communication": self.communication,
            "overall_score": self.get_overall_score()
        }


class SimpleScorer:
    """Simplified scoring system for Phase 1."""
    
    def __init__(self):
        """Initialize the simple scorer."""
        self.agent_metrics: Dict[str, SimpleMetrics] = {}
        self.role_weights = {
            AgentRole.LEGAL: {"response_quality": 0.4, "task_completion": 0.3, "communication": 0.2, "collaboration": 0.1},
            AgentRole.MARKETING: {"response_quality": 0.3, "collaboration": 0.3, "communication": 0.3, "task_completion": 0.1},
            AgentRole.TECHNICAL: {"task_completion": 0.4, "response_quality": 0.3, "collaboration": 0.2, "communication": 0.1},
            AgentRole.GENERAL: {"response_quality": 0.25, "collaboration": 0.25, "task_completion": 0.25, "communication": 0.25}
        }
    
    def calculate_agent_score(self, agent: SimpleAgent) -> float:
        """Calculate performance score for an agent."""
        # Get or create metrics for agent
        if agent.name not in self.agent_metrics:
            self.agent_metrics[agent.name] = SimpleMetrics()
        
        metrics = self.agent_metrics[agent.name]
        
        # Get role-specific weights
        weights = self.role_weights.get(agent.role, self.role_weights[AgentRole.GENERAL])
        
        # Calculate weighted score
        score = 0.0
        score += metrics.response_quality * weights["response_quality"]
        score += metrics.collaboration * weights["collaboration"]
        score += metrics.task_completion * weights["task_completion"]
        score += metrics.communication * weights["communication"]
        
        return min(1.0, max(0.0, score))  # Clamp between 0 and 1
    
    def update_metrics(self, agent_name: str, metric_type: str, value: float):
        """Update a specific metric for an agent."""
        if agent_name not in self.agent_metrics:
            self.agent_metrics[agent_name] = SimpleMetrics()
        
        # Clamp value between 0 and 1
        value = min(1.0, max(0.0, value))
        
        if metric_type == "response_quality":
            self.agent_metrics[agent_name].response_quality = value
        elif metric_type == "collaboration":
            self.agent_metrics[agent_name].collaboration = value
        elif metric_type == "task_completion":
            self.agent_metrics[agent_name].task_completion = value
        elif metric_type == "communication":
            self.agent_metrics[agent_name].communication = value
    
    def get_agent_metrics(self, agent_name: str) -> SimpleMetrics:
        """Get metrics for an agent."""
        if agent_name not in self.agent_metrics:
            self.agent_metrics[agent_name] = SimpleMetrics()
        return self.agent_metrics[agent_name]
    
    def allocate_resources(self, agents: List[SimpleAgent], total_resources: float) -> Dict[str, float]:
        """Allocate resources among agents based on performance."""
        if not agents:
            return {}
        
        # Calculate scores for all agents
        agent_scores = {}
        for agent in agents:
            score = self.calculate_agent_score(agent)
            agent_scores[agent.name] = score
        
        # Apply role-based adjustments
        role_adjustments = {
            AgentRole.LEGAL: 1.2,      # Legal gets slight boost
            AgentRole.MARKETING: 1.0,   # Marketing gets standard
            AgentRole.TECHNICAL: 1.3,   # Technical gets boost
            AgentRole.GENERAL: 1.0      # General gets standard
        }
        
        # Calculate final scores
        final_scores = {}
        for agent in agents:
            base_score = agent_scores[agent.name]
            role_multiplier = role_adjustments.get(agent.role, 1.0)
            final_scores[agent.name] = base_score * role_multiplier
        
        # Normalize and allocate resources
        total_score = sum(final_scores.values())
        if total_score == 0:
            # Equal distribution if no scores
            return {agent.name: total_resources / len(agents) for agent in agents}
        
        allocation = {}
        for agent in agents:
            score = final_scores[agent.name]
            allocation[agent.name] = (score / total_score) * total_resources
        
        return allocation
    
    def get_system_summary(self) -> Dict[str, Any]:
        """Get summary of system performance."""
        if not self.agent_metrics:
            return {"total_agents": 0, "average_performance": 0.0}
        
        total_score = 0.0
        agent_count = 0
        
        for metrics in self.agent_metrics.values():
            total_score += metrics.get_overall_score()
            agent_count += 1
        
        return {
            "total_agents": agent_count,
            "average_performance": total_score / agent_count if agent_count > 0 else 0.0,
            "metrics_tracked": len(self.agent_metrics)
        }
