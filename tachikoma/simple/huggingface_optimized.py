"""
Optimized Hugging Face Provider for Tachikoma.

This module provides an optimized Hugging Face implementation
specifically designed for multi-agent conversations.
"""

from typing import Dict, List, Any, Optional
import asyncio
import time
import torch
from transformers import (
    AutoModelForCausalLM, 
    AutoTokenizer, 
    pipeline,
    set_seed
)
from .llm_providers import BaseLLMProvider, LLMResponse


class OptimizedHuggingFaceProvider(BaseLLMProvider):
    """Optimized Hugging Face provider for conversations."""
    
    def __init__(self, model_name: str = "microsoft/DialoGPT-small"):
        super().__init__(model_name)
        self.model = None
        self.tokenizer = None
        self.pipeline = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the Hugging Face model with optimizations."""
        try:
            print(f"Loading Hugging Face model: {self.model_name}")
            print(f"Device: {self.device}")
            
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            
            # Set pad token
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Load model with optimizations
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                device_map="auto" if self.device == "cuda" else None,
                low_cpu_mem_usage=True
            )
            
            # Create pipeline for easier generation
            self.pipeline = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                device=0 if self.device == "cuda" else -1,
                return_full_text=False
            )
            
            print(f"Model loaded successfully on {self.device}")
            
        except Exception as e:
            print(f"Error loading model: {e}")
            raise ImportError(f"Failed to load Hugging Face model: {str(e)}")
    
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
            # Combine system prompt and user prompt
            if system_prompt:
                full_prompt = f"{system_prompt}\n\nHuman: {prompt}\nAssistant:"
            else:
                full_prompt = f"Human: {prompt}\nAssistant:"
            
            # Generate response using pipeline
            response = self.pipeline(
                full_prompt,
                max_new_tokens=max_tokens,
                temperature=temperature,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
                **kwargs
            )
            
            # Extract response content
            response_content = response[0]["generated_text"].strip()
            
            # Clean up response
            if response_content.startswith("Human:"):
                response_content = response_content.split("Human:")[0].strip()
            
            response_time = time.time() - start_time
            
            # Estimate tokens (rough calculation)
            tokens_used = len(response_content.split())
            
            return LLMResponse(
                content=response_content,
                provider="Hugging Face (Optimized)",
                model=self.model_name,
                tokens_used=tokens_used,
                response_time=response_time,
                cost=0.0  # Free for self-hosted
            )
            
        except Exception as e:
            raise RuntimeError(f"Hugging Face generation error: {str(e)}")
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model."""
        return {
            "model_name": self.model_name,
            "device": self.device,
            "model_type": type(self.model).__name__,
            "tokenizer_type": type(self.tokenizer).__name__,
            "vocab_size": self.tokenizer.vocab_size if self.tokenizer else 0,
            "max_length": self.tokenizer.model_max_length if self.tokenizer else 0
        }


class ConversationHuggingFaceProvider(BaseLLMProvider):
    """Hugging Face provider optimized for multi-agent conversations."""
    
    def __init__(self, model_name: str = "microsoft/DialoGPT-medium"):
        super().__init__(model_name)
        self.model = None
        self.tokenizer = None
        self.conversation_history = {}
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the conversation-optimized model."""
        try:
            print(f"Loading conversation model: {self.model_name}")
            
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                device_map="auto" if self.device == "cuda" else None
            )
            
            print(f"Conversation model loaded on {self.device}")
            
        except Exception as e:
            raise ImportError(f"Failed to load conversation model: {str(e)}")
    
    def _format_conversation(self, agent_name: str, prompt: str, system_prompt: str = "") -> str:
        """Format the conversation for the model."""
        # Get conversation history for this agent
        if agent_name not in self.conversation_history:
            self.conversation_history[agent_name] = []
        
        # Build conversation context
        conversation = []
        if system_prompt:
            conversation.append(f"System: {system_prompt}")
        
        # Add recent history (last 3 exchanges)
        recent_history = self.conversation_history[agent_name][-6:]  # 3 exchanges = 6 messages
        conversation.extend(recent_history)
        
        # Add current prompt
        conversation.append(f"Human: {prompt}")
        conversation.append(f"Assistant: {agent_name}:")
        
        return "\n".join(conversation)
    
    async def generate_response(
        self, 
        prompt: str, 
        system_prompt: str = "",
        max_tokens: int = 100,
        temperature: float = 0.7,
        agent_name: str = "Agent",
        **kwargs
    ) -> LLMResponse:
        """Generate response with conversation context."""
        if not self.model or not self.tokenizer:
            raise RuntimeError("Conversation model not initialized")
        
        start_time = time.time()
        
        try:
            # Format conversation
            formatted_prompt = self._format_conversation(agent_name, prompt, system_prompt)
            
            # Tokenize
            inputs = self.tokenizer.encode(formatted_prompt, return_tensors="pt")
            if self.device == "cuda":
                inputs = inputs.to(self.device)
            
            # Generate
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    max_length=inputs.shape[1] + max_tokens,
                    temperature=temperature,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                    **kwargs
                )
            
            # Decode response
            response_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract only the new response
            response_content = response_text[len(formatted_prompt):].strip()
            
            # Clean up response
            if "Human:" in response_content:
                response_content = response_content.split("Human:")[0].strip()
            
            # Update conversation history
            self.conversation_history[agent_name].extend([
                f"Human: {prompt}",
                f"Assistant: {agent_name}: {response_content}"
            ])
            
            # Keep only recent history (last 10 messages)
            if len(self.conversation_history[agent_name]) > 10:
                self.conversation_history[agent_name] = self.conversation_history[agent_name][-10:]
            
            response_time = time.time() - start_time
            tokens_used = len(response_content.split())
            
            return LLMResponse(
                content=response_content,
                provider="Hugging Face (Conversation)",
                model=self.model_name,
                tokens_used=tokens_used,
                response_time=response_time,
                cost=0.0
            )
            
        except Exception as e:
            raise RuntimeError(f"Conversation generation error: {str(e)}")
    
    def clear_conversation_history(self, agent_name: str = None):
        """Clear conversation history for an agent or all agents."""
        if agent_name:
            self.conversation_history.pop(agent_name, None)
        else:
            self.conversation_history.clear()
    
    def get_conversation_stats(self) -> Dict[str, Any]:
        """Get conversation statistics."""
        total_messages = sum(len(history) for history in self.conversation_history.values())
        return {
            "active_agents": len(self.conversation_history),
            "total_messages": total_messages,
            "agent_histories": {agent: len(history) for agent, history in self.conversation_history.items()}
        }
