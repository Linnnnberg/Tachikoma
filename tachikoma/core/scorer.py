"""
Enhanced resource scoring system for Tachikoma.

This module handles resource allocation and performance scoring
for agents in the multi-agent system with multi-dimensional analysis.
"""

from typing import Dict, List, Optional, Any, Tuple
import asyncio
import time
from datetime import datetime, timedelta
from .agent import AgentState, AgentDefinition, AgentRole, AgentPersonality, PoliticalProfile
from .metrics import DynamicMetricsSystem


class PerformanceMetrics:
    """Tracks performance metrics for an agent."""
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.response_time = []
        self.quality_scores = []
        self.collaboration_scores = []
        self.consensus_building_scores = []
        self.innovation_scores = []
        self.last_updated = datetime.now()
        
    def add_metric(self, metric_type: str, value: float, timestamp: datetime = None):
        """Add a performance metric."""
        if timestamp is None:
            timestamp = datetime.now()
            
        if metric_type == "response_time":
            self.response_time.append((timestamp, value))
        elif metric_type == "quality":
            self.quality_scores.append((timestamp, value))
        elif metric_type == "collaboration":
            self.collaboration_scores.append((timestamp, value))
        elif metric_type == "consensus":
            self.consensus_building_scores.append((timestamp, value))
        elif metric_type == "innovation":
            self.innovation_scores.append((timestamp, value))
            
        self.last_updated = timestamp
        
    def get_average_score(self, metric_type: str, hours: int = 24) -> float:
        """Get average score for a metric type within the last N hours."""
        cutoff = datetime.now() - timedelta(hours=hours)
        
        if metric_type == "response_time":
            scores = [score for ts, score in self.response_time if ts >= cutoff]
        elif metric_type == "quality":
            scores = [score for ts, score in self.quality_scores if ts >= cutoff]
        elif metric_type == "collaboration":
            scores = [score for ts, score in self.collaboration_scores if ts >= cutoff]
        elif metric_type == "consensus":
            scores = [score for ts, score in self.consensus_building_scores if ts >= cutoff]
        elif metric_type == "innovation":
            scores = [score for ts, score in self.innovation_scores if ts >= cutoff]
        else:
            return 0.0
            
        return sum(scores) / len(scores) if scores else 0.0


class ResourceScorer:
    """Enhanced resource allocation and performance scoring system with dynamic metrics."""

    def __init__(self):
        """Initialize the resource scorer."""
        self.performance_metrics: Dict[str, PerformanceMetrics] = {}
        self.resource_allocation_history: List[Dict[str, float]] = []
        self.dynamic_metrics = DynamicMetricsSystem()
        self.legacy_weights = {
            "quality": 0.3,
            "collaboration": 0.2,
            "consensus": 0.2,
            "innovation": 0.15,
            "response_time": 0.15
        }
        
    def _get_or_create_metrics(self, agent_id: str) -> PerformanceMetrics:
        """Get or create performance metrics for an agent."""
        if agent_id not in self.performance_metrics:
            self.performance_metrics[agent_id] = PerformanceMetrics(agent_id)
        return self.performance_metrics[agent_id]

    async def score_agent_performance(
        self, agent_id: str, context: str, performance_data: Dict[str, Any]
    ) -> float:
        """Score an agent's performance based on context and data."""
        metrics = self._get_or_create_metrics(agent_id)
        
        # Extract performance data
        response_time = performance_data.get("response_time", 0.0)
        quality_score = performance_data.get("quality_score", 0.0)
        collaboration_score = performance_data.get("collaboration_score", 0.0)
        consensus_score = performance_data.get("consensus_score", 0.0)
        innovation_score = performance_data.get("innovation_score", 0.0)
        
        # Add metrics
        metrics.add_metric("response_time", response_time)
        metrics.add_metric("quality", quality_score)
        metrics.add_metric("collaboration", collaboration_score)
        metrics.add_metric("consensus", consensus_score)
        metrics.add_metric("innovation", innovation_score)
        
        # Calculate weighted score
        total_score = 0.0
        total_weight = 0.0
        
        for metric_type, weight in self.legacy_weights.items():
            avg_score = metrics.get_average_score(metric_type)
            
            # Normalize response time (lower is better)
            if metric_type == "response_time":
                # Convert to 0-1 scale where 1 is best (fastest response)
                normalized_score = max(0, 1 - (avg_score / 10.0))  # 10 seconds = 0 score
            else:
                normalized_score = min(1.0, max(0.0, avg_score))
                
            total_score += normalized_score * weight
            total_weight += weight
            
        return total_score / total_weight if total_weight > 0 else 0.0

    async def allocate_resources(
        self, agents: Dict[str, AgentState], total_resources: float
    ) -> Dict[str, float]:
        """Allocate resources among agents based on their performance and roles."""
        if not agents:
            return {}
            
        # Calculate performance scores for all agents
        performance_scores = {}
        for agent_id, agent_state in agents.items():
            # Get recent performance data
            metrics = self._get_or_create_metrics(agent_id)
            recent_data = {
                "response_time": metrics.get_average_score("response_time", 24),
                "quality_score": metrics.get_average_score("quality", 24),
                "collaboration_score": metrics.get_average_score("collaboration", 24),
                "consensus_score": metrics.get_average_score("consensus", 24),
                "innovation_score": metrics.get_average_score("innovation", 24)
            }
            
            score = await self.score_agent_performance(agent_id, "", recent_data)
            performance_scores[agent_id] = score
            
        # Apply role-based adjustments
        role_adjustments = {}
        for agent_id, agent_state in agents.items():
            if hasattr(agent_state, 'definition') and agent_state.definition:
                role = agent_state.definition.role
                if role.decision_authority == "Executive":
                    role_adjustments[agent_id] = 1.5
                elif role.decision_authority == "Advisory":
                    role_adjustments[agent_id] = 1.2
                else:
                    role_adjustments[agent_id] = 1.0
            else:
                role_adjustments[agent_id] = 1.0
                
        # Calculate final allocation scores
        final_scores = {}
        for agent_id in agents:
            base_score = performance_scores.get(agent_id, 0.0)
            role_multiplier = role_adjustments.get(agent_id, 1.0)
            final_scores[agent_id] = base_score * role_multiplier
            
        # Normalize scores to sum to 1.0
        total_score = sum(final_scores.values())
        if total_score == 0:
            # Equal distribution if no scores
            return {agent_id: total_resources / len(agents) for agent_id in agents}
            
        # Allocate resources proportionally
        allocation = {}
        for agent_id, score in final_scores.items():
            allocation[agent_id] = (score / total_score) * total_resources
            
        # Store allocation history
        self.resource_allocation_history.append({
            "timestamp": datetime.now(),
            "allocation": allocation.copy(),
            "total_resources": total_resources
        })
        
        return allocation
        
    async def get_performance_summary(self, agent_id: str) -> Dict[str, Any]:
        """Get a comprehensive performance summary for an agent."""
        metrics = self._get_or_create_metrics(agent_id)
        
        return {
            "agent_id": agent_id,
            "overall_score": await self.score_agent_performance(agent_id, "", {}),
            "quality_score": metrics.get_average_score("quality", 24),
            "collaboration_score": metrics.get_average_score("collaboration", 24),
            "consensus_score": metrics.get_average_score("consensus", 24),
            "innovation_score": metrics.get_average_score("innovation", 24),
            "response_time": metrics.get_average_score("response_time", 24),
            "last_updated": metrics.last_updated.isoformat(),
            "total_metrics": len(metrics.quality_scores) + len(metrics.collaboration_scores) + 
                           len(metrics.consensus_building_scores) + len(metrics.innovation_scores)
        }
        
    async def get_system_performance(self) -> Dict[str, Any]:
        """Get overall system performance metrics."""
        if not self.performance_metrics:
            return {"total_agents": 0, "average_performance": 0.0}
            
        total_score = 0.0
        agent_count = 0
        
        for agent_id, metrics in self.performance_metrics.items():
            score = await self.score_agent_performance(agent_id, "", {})
            total_score += score
            agent_count += 1
            
        return {
            "total_agents": agent_count,
            "average_performance": total_score / agent_count if agent_count > 0 else 0.0,
            "allocation_history_length": len(self.resource_allocation_history)
        }
    
    async def calculate_dynamic_score(
        self, 
        agent_id: str, 
        context: str, 
        role: AgentRole
    ) -> Tuple[float, Dict[str, float]]:
        """Calculate agent score using dynamic metrics system."""
        return await self.dynamic_metrics.calculate_agent_score(agent_id, context, role)
    
    async def allocate_resources_dynamic(
        self, 
        agents: Dict[str, AgentState], 
        total_resources: float,
        context: str = "general"
    ) -> Dict[str, float]:
        """Allocate resources using dynamic metrics system."""
        if not agents:
            return {}
            
        # Calculate dynamic scores for all agents
        agent_scores = {}
        for agent_id, agent_state in agents.items():
            if hasattr(agent_state, 'definition') and agent_state.definition:
                score, metric_values = await self.calculate_dynamic_score(
                    agent_id, context, agent_state.definition.role
                )
                agent_scores[agent_id] = score
            else:
                # Fallback to legacy scoring
                score = await self.score_agent_performance(agent_id, context, {})
                agent_scores[agent_id] = score
        
        # Apply role-based adjustments
        role_adjustments = {}
        for agent_id, agent_state in agents.items():
            if hasattr(agent_state, 'definition') and agent_state.definition:
                role = agent_state.definition.role
                if role.decision_authority == "Executive":
                    role_adjustments[agent_id] = 1.5
                elif role.decision_authority == "Advisory":
                    role_adjustments[agent_id] = 1.2
                else:
                    role_adjustments[agent_id] = 1.0
            else:
                role_adjustments[agent_id] = 1.0
                
        # Calculate final allocation scores
        final_scores = {}
        for agent_id in agents:
            base_score = agent_scores.get(agent_id, 0.0)
            role_multiplier = role_adjustments.get(agent_id, 1.0)
            final_scores[agent_id] = base_score * role_multiplier
            
        # Normalize scores to sum to 1.0
        total_score = sum(final_scores.values())
        if total_score == 0:
            # Equal distribution if no scores
            return {agent_id: total_resources / len(agents) for agent_id in agents}
            
        # Allocate resources proportionally
        allocation = {}
        for agent_id, score in final_scores.items():
            allocation[agent_id] = (score / total_score) * total_resources
            
        # Store allocation history
        self.resource_allocation_history.append({
            "timestamp": datetime.now(),
            "allocation": allocation.copy(),
            "total_resources": total_resources,
            "context": context,
            "method": "dynamic"
        })
        
        return allocation
    
    def set_peer_collector(self, message_passing):
        """Set the peer assessment collector for dynamic metrics."""
        self.dynamic_metrics.set_peer_collector(message_passing)
    
    async def get_metric_analysis(self, agent_id: str, context: str, role: AgentRole) -> Dict[str, Any]:
        """Get detailed metric analysis for an agent."""
        return self.dynamic_metrics.get_metric_summary(agent_id, context, role)