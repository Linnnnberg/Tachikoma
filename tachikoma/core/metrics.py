"""
Dynamic metrics system for Tachikoma.

This module implements a comprehensive, context-aware metrics system
that can dynamically select and weight metrics based on context, role,
and performance patterns.
"""

from typing import Dict, List, Optional, Any, Tuple
import asyncio
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass
from .agent import AgentRole, AgentState, AgentDefinition


class MetricType(Enum):
    """Types of metrics in the system."""
    CORE_PERFORMANCE = "core_performance"
    COMMUNICATION = "communication"
    COLLABORATION = "collaboration"
    INNOVATION = "innovation"
    ROLE_SPECIFIC = "role_specific"


@dataclass
class MetricDefinition:
    """Definition of a metric."""
    name: str
    metric_type: MetricType
    description: str
    measurement_method: str
    weight_range: Tuple[float, float]  # (min_weight, max_weight)
    role_relevance: List[str]  # Roles this metric is relevant for
    context_relevance: List[str]  # Contexts this metric is relevant for


class MetricCollector:
    """Base class for collecting metric values."""
    
    async def collect_metric(self, agent_id: str, metric: str, context: str) -> float:
        """Collect a metric value for an agent."""
        raise NotImplementedError


class AutomatedMetricsCollector(MetricCollector):
    """Automatically collect metrics from agent interactions."""
    
    def __init__(self):
        self.message_analysis_cache = {}
        self.performance_history = {}
    
    async def collect_metric(self, agent_id: str, metric: str, context: str) -> float:
        """Collect metric value using automated analysis."""
        if metric == "response_quality":
            return await self._measure_response_quality(agent_id, context)
        elif metric == "response_speed":
            return await self._measure_response_speed(agent_id, context)
        elif metric == "collaboration_frequency":
            return await self._measure_collaboration_frequency(agent_id, context)
        elif metric == "consensus_building":
            return await self._measure_consensus_building(agent_id, context)
        elif metric == "idea_generation":
            return await self._measure_idea_generation(agent_id, context)
        elif metric == "task_completion":
            return await self._measure_task_completion(agent_id, context)
        else:
            return 0.0
    
    async def _measure_response_quality(self, agent_id: str, context: str) -> float:
        """Measure response quality using automated analysis."""
        # Simplified implementation - in practice would use NLP models
        # For now, return a mock score based on message length and complexity
        return 0.7  # Placeholder
    
    async def _measure_response_speed(self, agent_id: str, context: str) -> float:
        """Measure response speed."""
        # In practice, would measure actual response times
        return 0.8  # Placeholder
    
    async def _measure_collaboration_frequency(self, agent_id: str, context: str) -> float:
        """Measure how often the agent collaborates."""
        # In practice, would analyze message patterns
        return 0.6  # Placeholder
    
    async def _measure_consensus_building(self, agent_id: str, context: str) -> float:
        """Measure ability to build consensus."""
        # In practice, would analyze debate participation and outcomes
        return 0.5  # Placeholder
    
    async def _measure_idea_generation(self, agent_id: str, context: str) -> float:
        """Measure creativity and idea generation."""
        # In practice, would analyze content for novelty and creativity
        return 0.7  # Placeholder
    
    async def _measure_task_completion(self, agent_id: str, context: str) -> float:
        """Measure task completion success rate."""
        # In practice, would track actual task outcomes
        return 0.8  # Placeholder


class PeerAssessmentCollector(MetricCollector):
    """Collect metrics through peer assessment."""
    
    def __init__(self, message_passing):
        self.message_passing = message_passing
        self.peer_feedback = {}
    
    async def collect_metric(self, agent_id: str, metric: str, context: str) -> float:
        """Collect metric value through peer assessment."""
        # In practice, would ask other agents to rate the agent
        # For now, return mock peer assessment scores
        return 0.6  # Placeholder


class OutcomeBasedCollector(MetricCollector):
    """Collect metrics based on actual outcomes."""
    
    def __init__(self):
        self.outcome_history = {}
    
    async def collect_metric(self, agent_id: str, metric: str, context: str) -> float:
        """Collect metric value based on outcomes."""
        # In practice, would analyze actual task outcomes and results
        return 0.7  # Placeholder


class DynamicMetricsSystem:
    """Dynamic metrics system with context-aware selection and weighting."""
    
    def __init__(self):
        self.metric_definitions = self._initialize_metric_definitions()
        self.collectors = {
            'automated': AutomatedMetricsCollector(),
            'peer': None,  # Will be set when message_passing is available
            'outcome': OutcomeBasedCollector()
        }
        self.performance_history = {}
        self.context_weights = {}
        self.role_weights = {}
    
    def _initialize_metric_definitions(self) -> Dict[str, MetricDefinition]:
        """Initialize all available metric definitions."""
        return {
            # Core Performance Metrics
            "response_quality": MetricDefinition(
                name="response_quality",
                metric_type=MetricType.CORE_PERFORMANCE,
                description="Accuracy and relevance of responses",
                measurement_method="automated",
                weight_range=(0.1, 0.4),
                role_relevance=["all"],
                context_relevance=["all"]
            ),
            "response_speed": MetricDefinition(
                name="response_speed",
                metric_type=MetricType.CORE_PERFORMANCE,
                description="Time to generate response",
                measurement_method="automated",
                weight_range=(0.05, 0.2),
                role_relevance=["all"],
                context_relevance=["all"]
            ),
            "task_completion": MetricDefinition(
                name="task_completion",
                metric_type=MetricType.CORE_PERFORMANCE,
                description="Success rate in assigned tasks",
                measurement_method="outcome",
                weight_range=(0.2, 0.5),
                role_relevance=["all"],
                context_relevance=["all"]
            ),
            
            # Communication Metrics
            "message_clarity": MetricDefinition(
                name="message_clarity",
                metric_type=MetricType.COMMUNICATION,
                description="Clarity and understandability of messages",
                measurement_method="peer",
                weight_range=(0.1, 0.3),
                role_relevance=["all"],
                context_relevance=["communication", "collaboration"]
            ),
            "persuasion_effectiveness": MetricDefinition(
                name="persuasion_effectiveness",
                metric_type=MetricType.COMMUNICATION,
                description="Ability to influence others",
                measurement_method="peer",
                weight_range=(0.1, 0.4),
                role_relevance=["Marketing Strategist", "Executive", "Leader"],
                context_relevance=["negotiation", "decision_making", "persuasion"]
            ),
            
            # Collaboration Metrics
            "collaboration_frequency": MetricDefinition(
                name="collaboration_frequency",
                metric_type=MetricType.COLLABORATION,
                description="How often agent collaborates",
                measurement_method="automated",
                weight_range=(0.1, 0.3),
                role_relevance=["all"],
                context_relevance=["collaboration", "teamwork"]
            ),
            "consensus_building": MetricDefinition(
                name="consensus_building",
                metric_type=MetricType.COLLABORATION,
                description="Ability to build agreement",
                measurement_method="automated",
                weight_range=(0.1, 0.4),
                role_relevance=["all"],
                context_relevance=["decision_making", "debate", "negotiation"]
            ),
            
            # Innovation Metrics
            "idea_generation": MetricDefinition(
                name="idea_generation",
                metric_type=MetricType.INNOVATION,
                description="Novel ideas and solutions",
                measurement_method="automated",
                weight_range=(0.1, 0.4),
                role_relevance=["Creative", "Innovation", "Technical"],
                context_relevance=["brainstorming", "innovation", "creative_work"]
            ),
            "problem_solving": MetricDefinition(
                name="problem_solving",
                metric_type=MetricType.INNOVATION,
                description="Ability to solve complex problems",
                measurement_method="outcome",
                weight_range=(0.1, 0.4),
                role_relevance=["all"],
                context_relevance=["problem_solving", "troubleshooting"]
            ),
            
            # Role-Specific Metrics
            "compliance_accuracy": MetricDefinition(
                name="compliance_accuracy",
                metric_type=MetricType.ROLE_SPECIFIC,
                description="Accuracy in legal compliance",
                measurement_method="outcome",
                weight_range=(0.2, 0.6),
                role_relevance=["Legal Consultant", "Compliance Officer"],
                context_relevance=["legal", "compliance", "regulatory"]
            ),
            "technical_accuracy": MetricDefinition(
                name="technical_accuracy",
                metric_type=MetricType.ROLE_SPECIFIC,
                description="Technical accuracy and soundness",
                measurement_method="peer",
                weight_range=(0.2, 0.6),
                role_relevance=["Technical Architect", "Engineer", "Developer"],
                context_relevance=["technical", "development", "architecture"]
            ),
            "market_analysis": MetricDefinition(
                name="market_analysis",
                metric_type=MetricType.ROLE_SPECIFIC,
                description="Quality of market analysis",
                measurement_method="outcome",
                weight_range=(0.2, 0.6),
                role_relevance=["Marketing Strategist", "Business Analyst"],
                context_relevance=["marketing", "business_analysis", "strategy"]
            )
        }
    
    def get_relevant_metrics(self, context: str, role: AgentRole) -> List[str]:
        """Get metrics relevant to the context and role."""
        relevant_metrics = []
        
        for metric_name, definition in self.metric_definitions.items():
            # Check if metric is relevant to context
            context_relevant = (
                "all" in definition.context_relevance or 
                context.lower() in [c.lower() for c in definition.context_relevance]
            )
            
            # Check if metric is relevant to role
            role_relevant = (
                "all" in definition.role_relevance or 
                role.name in definition.role_relevance or
                role.domain.lower() in [r.lower() for r in definition.role_relevance]
            )
            
            if context_relevant and role_relevant:
                relevant_metrics.append(metric_name)
        
        return relevant_metrics
    
    def calculate_dynamic_weights(
        self, 
        context: str, 
        role: AgentRole, 
        agent_id: str = None
    ) -> Dict[str, float]:
        """Calculate dynamic weights for metrics based on context and role."""
        relevant_metrics = self.get_relevant_metrics(context, role)
        
        # Start with base weights
        weights = {}
        for metric_name in relevant_metrics:
            definition = self.metric_definitions[metric_name]
            # Use middle of weight range as base
            base_weight = (definition.weight_range[0] + definition.weight_range[1]) / 2
            weights[metric_name] = base_weight
        
        # Apply context adjustments
        weights = self._apply_context_adjustments(weights, context)
        
        # Apply role adjustments
        weights = self._apply_role_adjustments(weights, role)
        
        # Apply performance-based adjustments if agent_id provided
        if agent_id:
            weights = self._apply_performance_adjustments(weights, agent_id)
        
        # Normalize weights
        total_weight = sum(weights.values())
        if total_weight > 0:
            weights = {k: v/total_weight for k, v in weights.items()}
        
        return weights
    
    def _apply_context_adjustments(self, weights: Dict[str, float], context: str) -> Dict[str, float]:
        """Apply context-specific weight adjustments."""
        context_multipliers = {
            "brainstorming": {"idea_generation": 1.5, "creativity": 1.5},
            "decision_making": {"consensus_building": 1.5, "persuasion_effectiveness": 1.3},
            "problem_solving": {"problem_solving": 1.5, "technical_accuracy": 1.3},
            "negotiation": {"persuasion_effectiveness": 1.5, "consensus_building": 1.3},
            "legal": {"compliance_accuracy": 1.5, "response_quality": 1.2},
            "technical": {"technical_accuracy": 1.5, "problem_solving": 1.3},
            "marketing": {"market_analysis": 1.5, "persuasion_effectiveness": 1.3}
        }
        
        context_lower = context.lower()
        for metric, multiplier in context_multipliers.get(context_lower, {}).items():
            if metric in weights:
                weights[metric] *= multiplier
        
        return weights
    
    def _apply_role_adjustments(self, weights: Dict[str, float], role: AgentRole) -> Dict[str, float]:
        """Apply role-specific weight adjustments."""
        role_multipliers = {
            "Legal Consultant": {"compliance_accuracy": 1.5, "response_quality": 1.2},
            "Technical Architect": {"technical_accuracy": 1.5, "problem_solving": 1.3},
            "Marketing Strategist": {"market_analysis": 1.5, "persuasion_effectiveness": 1.3},
            "Executive": {"consensus_building": 1.5, "persuasion_effectiveness": 1.3}
        }
        
        for metric, multiplier in role_multipliers.get(role.name, {}).items():
            if metric in weights:
                weights[metric] *= multiplier
        
        return weights
    
    def _apply_performance_adjustments(self, weights: Dict[str, float], agent_id: str) -> Dict[str, float]:
        """Apply performance-based weight adjustments."""
        # In practice, would analyze agent's performance history
        # to identify strengths and weaknesses, then adjust weights accordingly
        return weights
    
    async def calculate_agent_score(
        self, 
        agent_id: str, 
        context: str, 
        role: AgentRole
    ) -> Tuple[float, Dict[str, float]]:
        """Calculate comprehensive agent score using dynamic metrics."""
        relevant_metrics = self.get_relevant_metrics(context, role)
        weights = self.calculate_dynamic_weights(context, role, agent_id)
        
        # Collect metric values
        metric_values = {}
        for metric_name in relevant_metrics:
            definition = self.metric_definitions[metric_name]
            collector = self.collectors.get(definition.measurement_method)
            
            if collector:
                value = await collector.collect_metric(agent_id, metric_name, context)
                metric_values[metric_name] = value
            else:
                metric_values[metric_name] = 0.0
        
        # Calculate weighted score
        total_score = 0.0
        for metric_name, value in metric_values.items():
            weight = weights.get(metric_name, 0.0)
            total_score += value * weight
        
        return total_score, metric_values
    
    def set_peer_collector(self, message_passing):
        """Set the peer assessment collector."""
        self.collectors['peer'] = PeerAssessmentCollector(message_passing)
    
    def get_metric_summary(self, agent_id: str, context: str, role: AgentRole) -> Dict[str, Any]:
        """Get a summary of metrics for an agent."""
        relevant_metrics = self.get_relevant_metrics(context, role)
        weights = self.calculate_dynamic_weights(context, role, agent_id)
        
        return {
            "agent_id": agent_id,
            "context": context,
            "role": role.name,
            "relevant_metrics": relevant_metrics,
            "metric_weights": weights,
            "total_metrics": len(relevant_metrics)
        }
