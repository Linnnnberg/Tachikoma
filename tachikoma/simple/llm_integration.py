"""
Language Model Integration for Phase 1.

This module provides real LLM integration for generating
dynamic agent responses instead of pre-defined templates.
"""

from typing import Dict, List, Any, Optional
import json
import asyncio
from .agent import SimpleAgent, AgentRole, PersonalityType


class LLMProvider:
    """Base class for LLM providers."""
    
    async def generate_response(self, prompt: str, **kwargs) -> str:
        """Generate a response using the LLM."""
        raise NotImplementedError


class MockLLMProvider(LLMProvider):
    """Mock LLM provider for testing without actual API calls."""
    
    def __init__(self):
        self.response_templates = {
            "legal": [
                "From a legal perspective, we need to consider compliance requirements and regulatory implications.",
                "I recommend conducting a thorough legal review to identify potential risks and liabilities.",
                "We must ensure all activities comply with applicable laws and regulations.",
                "The legal framework requires careful consideration of contractual obligations and data protection."
            ],
            "marketing": [
                "From a marketing standpoint, this presents an excellent opportunity to enhance our brand positioning.",
                "I suggest we conduct market research to understand customer needs and competitive landscape.",
                "This initiative aligns well with our brand strategy and customer engagement goals.",
                "We should leverage digital channels to maximize market reach and customer acquisition."
            ],
            "technical": [
                "From a technical perspective, this requires careful architecture planning and implementation strategy.",
                "I recommend a phased approach to ensure scalability and maintainability.",
                "We need to consider system integration, security, and performance requirements.",
                "The technical implementation should follow best practices for reliability and efficiency."
            ],
            "general": [
                "I'll analyze this situation comprehensively and provide strategic recommendations.",
                "We need to consider all aspects of this decision and their long-term implications.",
                "I suggest we gather more information and evaluate all available options.",
                "This decision requires careful planning and coordination across all departments."
            ]
        }
    
    async def generate_response(self, prompt: str, **kwargs) -> str:
        """Generate a mock response based on the prompt."""
        # Simple keyword-based response selection
        role = kwargs.get('role', 'general')
        templates = self.response_templates.get(role, self.response_templates['general'])
        
        # Select template based on prompt content
        import random
        selected_template = random.choice(templates)
        
        # Add some variation based on prompt
        if "urgent" in prompt.lower():
            selected_template = f"URGENT: {selected_template}"
        elif "budget" in prompt.lower():
            selected_template = f"Regarding budget considerations: {selected_template}"
        
        return selected_template


class OpenAIProvider(LLMProvider):
    """OpenAI API provider for real LLM integration."""
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key
        self.model = model
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the OpenAI client."""
        try:
            import openai
            self.client = openai.OpenAI(api_key=self.api_key)
        except ImportError:
            raise ImportError("OpenAI library not installed. Run: pip install openai")
    
    async def generate_response(self, prompt: str, **kwargs) -> str:
        """Generate response using OpenAI API."""
        if not self.client:
            raise RuntimeError("OpenAI client not initialized")
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": kwargs.get('system_prompt', 'You are a helpful assistant.')},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=kwargs.get('max_tokens', 200),
                temperature=kwargs.get('temperature', 0.7)
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating response: {str(e)}"


class AgentLLMIntegration:
    """LLM integration for agent responses."""
    
    def __init__(self, llm_provider: LLMProvider):
        self.llm_provider = llm_provider
        self.conversation_history: Dict[str, List[Dict[str, str]]] = {}
    
    def _get_system_prompt(self, agent: SimpleAgent) -> str:
        """Generate system prompt for the agent."""
        return f"""You are {agent.name}, a {agent.role.value} specialist with a {agent.personality.value} personality.

Your expertise includes: {', '.join(agent.expertise)}

Your role: {agent.get_role_description()}
Your personality: {agent.get_personality_description()}

Respond as this character would, considering your role, personality, and expertise. 
Be specific, professional, and provide actionable insights based on your background.
Keep responses concise but informative (2-3 sentences)."""
    
    def _get_conversation_context(self, agent_name: str, max_messages: int = 5) -> str:
        """Get recent conversation context for the agent."""
        if agent_name not in self.conversation_history:
            return ""
        
        recent_messages = self.conversation_history[agent_name][-max_messages:]
        context = "Recent conversation:\n"
        for msg in recent_messages:
            context += f"{msg['role']}: {msg['content']}\n"
        return context
    
    async def generate_agent_response(
        self, 
        agent: SimpleAgent, 
        context: str, 
        conversation_history: List[Dict[str, str]] = None
    ) -> str:
        """Generate a dynamic response for an agent using LLM."""
        
        # Build the prompt
        system_prompt = self._get_system_prompt(agent)
        
        # Add conversation context if available
        if conversation_history:
            context += f"\n\nConversation context:\n"
            for msg in conversation_history[-3:]:  # Last 3 messages
                context += f"{msg.get('from_agent', 'Unknown')}: {msg.get('content', '')}\n"
        
        # Create the user prompt
        user_prompt = f"""Context: {context}

Please provide your professional opinion and recommendations based on your role as a {agent.role.value} specialist."""
        
        # Generate response using LLM
        response = await self.llm_provider.generate_response(
            user_prompt,
            system_prompt=system_prompt,
            role=agent.role.value,
            max_tokens=150,
            temperature=0.7
        )
        
        # Store in conversation history
        if agent.name not in self.conversation_history:
            self.conversation_history[agent.name] = []
        
        self.conversation_history[agent.name].append({
            "role": "assistant",
            "content": response
        })
        
        return response
    
    def add_message_to_history(self, agent_name: str, role: str, content: str):
        """Add a message to conversation history."""
        if agent_name not in self.conversation_history:
            self.conversation_history[agent_name] = []
        
        self.conversation_history[agent_name].append({
            "role": role,
            "content": content
        })


class LLMOrchestrator:
    """Enhanced orchestrator with LLM integration."""
    
    def __init__(self, llm_provider: LLMProvider):
        from .orchestrator import SimpleOrchestrator
        self.orchestrator = SimpleOrchestrator()
        self.llm_integration = AgentLLMIntegration(llm_provider)
        self.debug_mode = True
        self.step_counter = 0
    
    def add_agent(self, agent: SimpleAgent) -> str:
        """Add an agent to the system."""
        return self.orchestrator.add_agent(agent)
    
    async def generate_dynamic_response(self, agent_name: str, context: str) -> str:
        """Generate a dynamic response using LLM."""
        agent = self.orchestrator.get_agent(agent_name)
        if not agent:
            return "Agent not found"
        
        # Get recent conversation history
        recent_messages = self.orchestrator.get_messages(agent_name)[:3]
        
        # Generate response using LLM
        response = await self.llm_integration.generate_agent_response(
            agent, context, recent_messages
        )
        
        return response
    
    async def run_llm_conversation(self, scenario: str, max_turns: int = 6) -> Dict[str, Any]:
        """Run a conversation using LLM-generated responses."""
        results = {
            "scenario": scenario,
            "turns": [],
            "final_state": {}
        }
        
        agents = list(self.orchestrator.agents.values())
        if len(agents) < 2:
            results["error"] = "Not enough agents for conversation"
            return results
        
        # Start with the first agent
        current_agent = agents[0]
        context = scenario
        
        for turn in range(max_turns):
            self.step_counter += 1
            print(f"\n[LLM TURN {turn + 1}] {current_agent.name} responding...")
            
            # Generate dynamic response
            response = await self.generate_dynamic_response(current_agent.name, context)
            
            print(f"  {current_agent.name}: {response}")
            
            # Store the turn
            results["turns"].append({
                "agent": current_agent.name,
                "response": response,
                "turn": turn + 1
            })
            
            # Send message to other agents
            for other_agent in agents:
                if other_agent.name != current_agent.name:
                    self.orchestrator.send_message(
                        current_agent.name, 
                        other_agent.name, 
                        response
                    )
            
            # Move to next agent
            current_agent = agents[(turn + 1) % len(agents)]
            
            # Update context with the response
            context = f"{context}\n\n{current_agent.name} said: {response}"
        
        # Get final system state
        results["final_state"] = self.orchestrator.get_system_status()
        
        return results
