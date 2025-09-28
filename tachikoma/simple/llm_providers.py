"""
Multiple LLM Provider Implementations for Tachikoma.

This module provides implementations for different LLM providers:
- OpenAI (GPT models)
- Hugging Face (open source models)
- Llama (Meta's models)
- Hybrid approach
"""

from typing import Dict, List, Any, Optional, Union
import asyncio
import json
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass


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


class OpenAIProvider(BaseLLMProvider):
    """OpenAI GPT models provider."""
    
    def __init__(self, api_key: str, model_name: str = "gpt-3.5-turbo"):
        super().__init__(model_name)
        self.api_key = api_key
        self.client = None
        self._initialize_client()
        
        # Pricing per 1k tokens (as of 2024)
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
            
            # Calculate tokens and cost
            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens
            total_tokens = input_tokens + output_tokens
            
            pricing = self.pricing.get(self.model_name, {"input": 0.0015, "output": 0.002})
            cost = (input_tokens / 1000 * pricing["input"] + 
                   output_tokens / 1000 * pricing["output"])
            
            # Update stats
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


class HuggingFaceProvider(BaseLLMProvider):
    """Hugging Face models provider."""
    
    def __init__(self, model_name: str = "microsoft/DialoGPT-medium"):
        super().__init__(model_name)
        self.model = None
        self.tokenizer = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the Hugging Face model."""
        try:
            from transformers import AutoModelForCausalLM, AutoTokenizer
            import torch
            
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                device_map="auto" if torch.cuda.is_available() else None
            )
            
            # Set pad token
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
                
        except ImportError:
            raise ImportError("Transformers library not installed. Run: pip install transformers torch")
    
    async def generate_response(
        self, 
        prompt: str, 
        system_prompt: str = "",
        max_tokens: int = 200,
        temperature: float = 0.7,
        **kwargs
    ) -> LLMResponse:
        """Generate response using Hugging Face model."""
        if not self.model or not self.tokenizer:
            raise RuntimeError("Hugging Face model not initialized")
        
        start_time = time.time()
        
        try:
            # Combine system prompt and user prompt
            full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
            
            # Tokenize input
            inputs = self.tokenizer.encode(full_prompt, return_tensors="pt")
            
            # Generate response
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    max_length=inputs.shape[1] + max_tokens,
                    temperature=temperature,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                    **kwargs
                )
            
            # Decode response
            response_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Remove input from response
            response_content = response_text[len(full_prompt):].strip()
            
            response_time = time.time() - start_time
            tokens_used = outputs.shape[1] - inputs.shape[1]
            
            return LLMResponse(
                content=response_content,
                provider="Hugging Face",
                model=self.model_name,
                tokens_used=tokens_used,
                response_time=response_time,
                cost=0.0  # Free for self-hosted
            )
            
        except Exception as e:
            raise RuntimeError(f"Hugging Face model error: {str(e)}")


class LlamaProvider(BaseLLMProvider):
    """Llama models provider using llama-cpp-python."""
    
    def __init__(self, model_path: str, model_name: str = "llama-2-7b"):
        super().__init__(model_name)
        self.model_path = model_path
        self.llm = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the Llama model."""
        try:
            from llama_cpp import Llama
            
            self.llm = Llama(
                model_path=self.model_path,
                n_ctx=2048,  # Context window
                n_threads=4,  # Number of threads
                verbose=False
            )
        except ImportError:
            raise ImportError("llama-cpp-python not installed. Run: pip install llama-cpp-python")
    
    async def generate_response(
        self, 
        prompt: str, 
        system_prompt: str = "",
        max_tokens: int = 200,
        temperature: float = 0.7,
        **kwargs
    ) -> LLMResponse:
        """Generate response using Llama model."""
        if not self.llm:
            raise RuntimeError("Llama model not initialized")
        
        start_time = time.time()
        
        try:
            # Combine system prompt and user prompt
            full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
            
            # Generate response
            response = self.llm(
                full_prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                stop=["Human:", "Assistant:", "\n\n"],
                **kwargs
            )
            
            response_content = response["choices"][0]["text"].strip()
            response_time = time.time() - start_time
            tokens_used = response["usage"]["completion_tokens"]
            
            return LLMResponse(
                content=response_content,
                provider="Llama",
                model=self.model_name,
                tokens_used=tokens_used,
                response_time=response_time,
                cost=0.0  # Free for self-hosted
            )
            
        except Exception as e:
            raise RuntimeError(f"Llama model error: {str(e)}")


class MockProvider(BaseLLMProvider):
    """Mock provider for testing without actual LLM calls."""
    
    def __init__(self, model_name: str = "mock-model"):
        super().__init__(model_name)
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
        
        # Determine role from system prompt
        role = "general"
        if "legal" in system_prompt.lower():
            role = "legal"
        elif "marketing" in system_prompt.lower():
            role = "marketing"
        elif "technical" in system_prompt.lower():
            role = "technical"
        
        # Select template
        templates = self.response_templates.get(role, self.response_templates["general"])
        import random
        content = random.choice(templates)
        
        # Add some variation based on prompt
        if "urgent" in prompt.lower():
            content = f"URGENT: {content}"
        elif "budget" in prompt.lower():
            content = f"Regarding budget considerations: {content}"
        
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


class HybridProvider(BaseLLMProvider):
    """Hybrid provider that tries multiple providers in order."""
    
    def __init__(self, providers: List[BaseLLMProvider], model_name: str = "hybrid"):
        super().__init__(model_name)
        self.providers = providers
        self.fallback_count = 0
    
    async def generate_response(
        self, 
        prompt: str, 
        system_prompt: str = "",
        max_tokens: int = 200,
        temperature: float = 0.7,
        **kwargs
    ) -> LLMResponse:
        """Generate response using the first available provider."""
        last_error = None
        
        for i, provider in enumerate(self.providers):
            try:
                response = await provider.generate_response(
                    prompt, system_prompt, max_tokens, temperature, **kwargs
                )
                
                if i > 0:  # Used fallback
                    self.fallback_count += 1
                    response.provider = f"{response.provider} (fallback)"
                
                return response
                
            except Exception as e:
                last_error = e
                continue
        
        raise RuntimeError(f"All providers failed. Last error: {last_error}")
    
    def get_fallback_stats(self) -> Dict[str, Any]:
        """Get fallback usage statistics."""
        return {
            "fallback_count": self.fallback_count,
            "total_providers": len(self.providers),
            "fallback_rate": self.fallback_count / max(1, self.total_tokens)
        }


class LLMProviderFactory:
    """Factory for creating LLM providers."""
    
    @staticmethod
    def create_openai_provider(api_key: str, model: str = "gpt-3.5-turbo") -> OpenAIProvider:
        """Create an OpenAI provider."""
        return OpenAIProvider(api_key, model)
    
    @staticmethod
    def create_huggingface_provider(model: str = "microsoft/DialoGPT-medium") -> HuggingFaceProvider:
        """Create a Hugging Face provider."""
        return HuggingFaceProvider(model)
    
    @staticmethod
    def create_llama_provider(model_path: str, model_name: str = "llama-2-7b") -> LlamaProvider:
        """Create a Llama provider."""
        return LlamaProvider(model_path, model_name)
    
    @staticmethod
    def create_mock_provider() -> MockProvider:
        """Create a mock provider for testing."""
        return MockProvider()
    
    @staticmethod
    def create_hybrid_provider(
        openai_key: str = None,
        huggingface_model: str = None,
        llama_path: str = None
    ) -> HybridProvider:
        """Create a hybrid provider with multiple fallbacks."""
        providers = []
        
        # Add mock provider as ultimate fallback
        providers.append(MockProvider())
        
        # Add Llama if available
        if llama_path:
            try:
                providers.insert(0, LlamaProvider(llama_path))
            except Exception:
                pass
        
        # Add Hugging Face if available
        if huggingface_model:
            try:
                providers.insert(0, HuggingFaceProvider(huggingface_model))
            except Exception:
                pass
        
        # Add OpenAI if available
        if openai_key:
            try:
                providers.insert(0, OpenAIProvider(openai_key))
            except Exception:
                pass
        
        return HybridProvider(providers)
