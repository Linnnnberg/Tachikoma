"""
Unified LLM Integration for Tachikoma Core System.

This module consolidates LLM functionality from the simple/ implementation
into the enhanced core/ architecture, supporting multiple providers and
optimized conversation management.
"""

from typing import Dict, List, Any, Optional
import asyncio
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from .agent import AgentDefinition, AgentState


@dataclass
class LLMResponse:
    """Standardized response from any LLM provider."""
    content: str
    provider: str
    model: str
    tokens_used: int
    response_time: float
    cost: float = 0.0


class BaseLLMProvider(ABC):
    """Base class for all LLM providers."""
    
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.total_tokens = 0
        self.total_cost = 0.0
    
    @abstractmethod
    async def generate_response(
        self, 
        prompt: str, 
        system_prompt: str = "",
        max_tokens: int = 200,
        temperature: float = 0.7,
        **kwargs
    ) -> LLMResponse:
        """Generate a response using the LLM."""
        pass
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """Get usage statistics."""
        return {
            "total_tokens": self.total_tokens,
            "total_cost": self.total_cost,
            "model": self.model_name
        }


class HuggingFaceProvider(BaseLLMProvider):
    """Optimized Hugging Face provider for conversations."""
    
    def __init__(self, model_name: str = "microsoft/DialoGPT-small"):
        super().__init__(model_name)
        self.model = None
        self.tokenizer = None
        self.pipeline = None
        self.device = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the Hugging Face model with optimizations."""
        try:
            import torch
            from transformers import (
                AutoModelForCausalLM, 
                AutoTokenizer, 
                pipeline,
            )
            
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            print(f"Loading Hugging Face model: {self.model_name} on {self.device}")
            
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                device_map="auto" if self.device == "cuda" else None,
                low_cpu_mem_usage=True
            )
            
            self.pipeline = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                device=0 if self.device == "cuda" else -1,
                return_full_text=False
            )
            
            print(f"Model loaded successfully on {self.device}")
            
        except ImportError as e:
            raise ImportError(f"Required libraries not installed: {str(e)}\nRun: pip install transformers torch")
        except Exception as e:
            raise RuntimeError(f"Failed to load Hugging Face model: {str(e)}")
    
    async def generate_response(
        self, 
        prompt: str, 
        system_prompt: str = "",
        max_tokens: int = 100,
        temperature: float = 0.7,
        **kwargs
    ) -> LLMResponse:
        """Generate response using optimized Hugging Face model."""
        if not self.pipeline:
            raise RuntimeError("Hugging Face model not initialized")
        
        start_time = time.time()
        
        try:
            if system_prompt:
                full_prompt = f"{system_prompt}\n\nHuman: {prompt}\nAssistant:"
            else:
                full_prompt = f"Human: {prompt}\nAssistant:"
            
            response = self.pipeline(
                full_prompt,
                max_new_tokens=max_tokens,
                temperature=temperature,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
                **kwargs
            )
            
            response_content = response[0]["generated_text"].strip()
            
            if response_content.startswith("Human:"):
                response_content = response_content.split("Human:")[0].strip()
            
            response_time = time.time() - start_time
            tokens_used = len(response_content.split())
            
            self.total_tokens += tokens_used
            
            return LLMResponse(
                content=response_content,
                provider="Hugging Face",
                model=self.model_name,
                tokens_used=tokens_used,
                response_time=response_time,
                cost=0.0
            )
            
        except Exception as e:
            raise RuntimeError(f"Hugging Face generation error: {str(e)}")


class OpenAIProvider(BaseLLMProvider):
    """OpenAI GPT models provider."""
    
    def __init__(self, api_key: str, model_name: str = "gpt-3.5-turbo"):
        super().__init__(model_name)
        self.api_key = api_key
        self.client = None
        self._initialize_client()
        
        self.pricing = {
            "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002},
            "gpt-4": {"input": 0.03, "output": 0.06},
            "gpt-4-turbo": {"input": 0.01, "output": 0.03}
        }
    
    def _initialize_client(self):
        """Initialize the OpenAI client."""
        try:
            import openai
            self.client = openai.OpenAI(api_key=self.api_key)
        except ImportError:
            raise ImportError("OpenAI library not installed. Run: pip install openai")
    
    async def generate_response(
        self, 
        prompt: str, 
        system_prompt: str = "",
        max_tokens: int = 200,
        temperature: float = 0.7,
        **kwargs
    ) -> LLMResponse:
        """Generate response using OpenAI API."""
        if not self.client:
            raise RuntimeError("OpenAI client not initialized")
        
        start_time = time.time()
        
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                **kwargs
            )
            
            response_time = time.time() - start_time
            content = response.choices[0].message.content
            
            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens
            total_tokens = input_tokens + output_tokens
            
            pricing = self.pricing.get(self.model_name, {"input": 0.0015, "output": 0.002})
            cost = (input_tokens / 1000 * pricing["input"] + 
                   output_tokens / 1000 * pricing["output"])
            
            self.total_tokens += total_tokens
            self.total_cost += cost
            
            return LLMResponse(
                content=content,
                provider="OpenAI",
                model=self.model_name,
                tokens_used=total_tokens,
                response_time=response_time,
                cost=cost
            )
            
        except Exception as e:
            raise RuntimeError(f"OpenAI API error: {str(e)}")


class MockProvider(BaseLLMProvider):
    """Mock provider for testing without actual LLM calls."""
    
    def __init__(self, model_name: str = "mock-model"):
        super().__init__(model_name)
        self.response_templates = {
            "legal": [
                "From a legal perspective, we need to consider compliance requirements and regulatory implications.",
                "I recommend conducting a thorough legal review to identify potential risks and liabilities.",
                "We must ensure all activities comply with applicable laws and regulations."
            ],
            "marketing": [
                "From a marketing standpoint, this presents an excellent opportunity to enhance our brand positioning.",
                "I suggest we conduct market research to understand customer needs and competitive landscape.",
                "This initiative aligns well with our brand strategy and customer engagement goals."
            ],
            "technical": [
                "From a technical perspective, this requires careful architecture planning and implementation strategy.",
                "I recommend a phased approach to ensure scalability and maintainability.",
                "We need to consider system integration, security, and performance requirements."
            ],
            "general": [
                "I'll analyze this situation comprehensively and provide strategic recommendations.",
                "We need to consider all aspects of this decision and their long-term implications.",
                "This decision requires careful planning and coordination across all departments."
            ]
        }
    
    async def generate_response(
        self, 
        prompt: str, 
        system_prompt: str = "",
        max_tokens: int = 200,
        temperature: float = 0.7,
        **kwargs
    ) -> LLMResponse:
        """Generate a mock response."""
        start_time = time.time()
        
        role = "general"
        if "legal" in system_prompt.lower():
            role = "legal"
        elif "marketing" in system_prompt.lower():
            role = "marketing"
        elif "technical" in system_prompt.lower():
            role = "technical"
        
        templates = self.response_templates.get(role, self.response_templates["general"])
        import random
        content = random.choice(templates)
        
        if "urgent" in prompt.lower():
            content = f"URGENT: {content}"
        
        response_time = time.time() - start_time
        tokens_used = len(content.split())
        
        return LLMResponse(
            content=content,
            provider="Mock",
            model=self.model_name,
            tokens_used=tokens_used,
            response_time=response_time,
            cost=0.0
        )


class EnhancedAgentLLM:
    """LLM integration for enhanced multi-dimensional agents."""
    
    def __init__(self, llm_provider: BaseLLMProvider):
        self.llm_provider = llm_provider
        self.conversation_history: Dict[str, List[Dict[str, str]]] = {}
    
    def _build_system_prompt(self, agent_definition: AgentDefinition) -> str:
        """Build comprehensive system prompt from agent definition."""
        role = agent_definition.role
        prompt_parts = [
            f"You are a {role.name}, specializing in {role.domain}.",
            f"Your responsibilities include: {', '.join(role.responsibilities)}.",
            f"Your expertise covers: {', '.join(role.required_expertise)}.",
            f"You have {role.decision_authority} level decision-making authority."
        ]
        
        if agent_definition.personality:
            personality = agent_definition.personality
            prompt_parts.append(f"\nYour communication style is {personality.communication_style}.")
            prompt_parts.append(f"Your risk tolerance is {personality.risk_tolerance}.")
            prompt_parts.append(f"You collaborate in a {personality.collaboration_style} manner.")
            prompt_parts.append(f"Your guiding principles: {', '.join(personality.principles)}.")
        
        if agent_definition.political_profile and agent_definition.political_profile.political_spectrum:
            political = agent_definition.political_profile
            prompt_parts.append(f"\nYour political orientation: {political.political_spectrum.value}.")
            if political.key_issues:
                prompt_parts.append(f"You focus on: {', '.join(political.key_issues)}.")
        
        if agent_definition.correlated_params:
            params = agent_definition.correlated_params
            if params.regulation_preference:
                prompt_parts.append(f"Your stance on regulation: {params.regulation_preference}.")
            if params.technology_approach:
                prompt_parts.append(f"Your technology approach: {params.technology_approach}.")
        
        if agent_definition.custom_instructions:
            prompt_parts.append(f"\nAdditional guidance: {agent_definition.custom_instructions}")
        
        prompt_parts.append("\nRespond authentically based on your role, expertise, and principles. Keep responses concise (2-3 sentences) but insightful.")
        
        return "\n".join(prompt_parts)
    
    def _get_conversation_context(self, agent_id: str, max_messages: int = 5) -> str:
        """Get recent conversation context."""
        if agent_id not in self.conversation_history:
            return ""
        
        recent = self.conversation_history[agent_id][-max_messages:]
        context = "\nRecent conversation:\n"
        for msg in recent:
            context += f"{msg['role']}: {msg['content']}\n"
        return context
    
    async def generate_agent_response(
        self,
        agent_state: AgentState,
        agent_id: str,
        context: str,
        recent_messages: List[Dict[str, Any]] = None
    ) -> str:
        """Generate dynamic response for an agent."""
        system_prompt = self._build_system_prompt(agent_state.definition)
        
        prompt = f"Context: {context}\n"
        
        if recent_messages:
            prompt += "\nRecent discussion:\n"
            for msg in recent_messages[-3:]:
                sender = msg.get('from_agent', 'Unknown')
                content = msg.get('content', '')
                prompt += f"{sender}: {content}\n"
        
        prompt += "\nPlease provide your professional perspective and recommendations."
        
        response = await self.llm_provider.generate_response(
            prompt,
            system_prompt=system_prompt,
            max_tokens=150,
            temperature=0.7
        )
        
        if agent_id not in self.conversation_history:
            self.conversation_history[agent_id] = []
        
        self.conversation_history[agent_id].append({
            "role": "assistant",
            "content": response.content
        })
        
        return response.content
    
    def add_to_history(self, agent_id: str, role: str, content: str):
        """Add message to conversation history."""
        if agent_id not in self.conversation_history:
            self.conversation_history[agent_id] = []
        
        self.conversation_history[agent_id].append({
            "role": role,
            "content": content
        })
    
    def clear_history(self, agent_id: str = None):
        """Clear conversation history."""
        if agent_id:
            self.conversation_history.pop(agent_id, None)
        else:
            self.conversation_history.clear()


class LLMProviderFactory:
    """Factory for creating LLM providers."""
    
    @staticmethod
    def create_huggingface_provider(model: str = "microsoft/DialoGPT-small") -> HuggingFaceProvider:
        """Create a Hugging Face provider."""
        return HuggingFaceProvider(model)
    
    @staticmethod
    def create_openai_provider(api_key: str, model: str = "gpt-3.5-turbo") -> OpenAIProvider:
        """Create an OpenAI provider."""
        return OpenAIProvider(api_key, model)
    
    @staticmethod
    def create_mock_provider() -> MockProvider:
        """Create a mock provider for testing."""
        return MockProvider()
