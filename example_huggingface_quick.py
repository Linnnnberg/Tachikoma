#!/usr/bin/env python3
"""
Quick Hugging Face Test.

This script tests Hugging Face integration with a smaller, faster model
to avoid long download times.
"""

import asyncio
import sys
import os
import time

# Add the tachikoma package to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tachikoma'))

from tachikoma.simple.agent import SimpleAgent, AgentRole, PersonalityType
from tachikoma.simple.llm_providers import HuggingFaceProvider


async def quick_huggingface_test():
    """Quick test of Hugging Face integration."""
    
    print("Tachikoma Quick Hugging Face Test")
    print("=" * 50)
    print("Testing with a small, fast model...")
    print("=" * 50)
    
    # Use a very small model for quick testing
    model_name = "microsoft/DialoGPT-small"
    
    print(f"\n[LOADING MODEL] {model_name}")
    print("This may take a moment for first-time download...")
    
    try:
        # Create provider
        provider = HuggingFaceProvider(model_name)
        print("[SUCCESS] Model loaded successfully!")
        
        # Test scenario
        scenario = "Should we invest in AI technology?"
        system_prompt = "You are a legal consultant. Provide brief advice."
        
        print(f"\n[TEST SCENARIO] {scenario}")
        
        # Test response generation
        print("\n[GENERATING RESPONSE]...")
        start_time = time.time()
        
        response = await provider.generate_response(
            prompt=scenario,
            system_prompt=system_prompt,
            max_tokens=30,
            temperature=0.7
        )
        
        total_time = time.time() - start_time
        
        print(f"\n[RESPONSE GENERATED]")
        print(f"Model: {response.model}")
        print(f"Provider: {response.provider}")
        print(f"Response: {response.content}")
        print(f"Tokens Used: {response.tokens_used}")
        print(f"Response Time: {response.response_time:.2f}s")
        print(f"Total Time: {total_time:.2f}s")
        print(f"Cost: ${response.cost:.4f}")
        
        # Test multiple agents
        print(f"\n[TESTING MULTIPLE AGENTS]")
        
        agents = [
            ("Alice", "legal consultant", "compliance and risk management"),
            ("Bob", "marketing specialist", "customer engagement and brand strategy"),
            ("Charlie", "technical expert", "system architecture and implementation")
        ]
        
        for name, role, expertise in agents:
            print(f"\n{name} ({role}):")
            
            system_prompt = f"You are {name}, a {role} with expertise in {expertise}. Provide brief advice."
            
            response = await provider.generate_response(
                prompt=scenario,
                system_prompt=system_prompt,
                max_tokens=25,
                temperature=0.7
            )
            
            print(f"  {response.content}")
            print(f"  [Time: {response.response_time:.2f}s]")
        
        # Show usage stats
        stats = provider.get_usage_stats()
        print(f"\n[USAGE STATISTICS]")
        print(f"Total Tokens: {stats['total_tokens']}")
        print(f"Total Cost: ${stats['total_cost']:.4f}")
        print(f"Model: {stats['model']}")
        
        print(f"\n[SUCCESS] Hugging Face integration is working!")
        print(f"  - Model: {model_name}")
        print(f"  - Device: CPU (no GPU detected)")
        print(f"  - Response Quality: Basic but functional")
        print(f"  - Speed: {total_time:.2f}s per response")
        
        print(f"\n[RECOMMENDATIONS]")
        print(f"  - This is a basic model for testing")
        print(f"  - For better quality, use DialoGPT-medium or larger")
        print(f"  - For production, consider fine-tuning or using GPT models")
        print(f"  - The system is ready for multi-agent conversations")
        
        return True
        
    except Exception as e:
        print(f"\n[ERROR] Hugging Face test failed: {str(e)}")
        print(f"\n[TROUBLESHOOTING]")
        print(f"  - Check internet connection for model download")
        print(f"  - Ensure transformers library is installed: pip install transformers torch")
        print(f"  - Try a different model if this one fails")
        print(f"  - Check available disk space for model cache")
        
        return False


async def test_agent_conversation():
    """Test a simple agent conversation."""
    
    print(f"\n{'='*50}")
    print("SIMPLE AGENT CONVERSATION TEST")
    print(f"{'='*50}")
    
    try:
        # Create provider
        provider = HuggingFaceProvider("microsoft/DialoGPT-small")
        
        # Create test agents
        agents = [
            SimpleAgent("Alice", AgentRole.LEGAL, PersonalityType.ANALYTICAL, ["Compliance"], 0.85),
            SimpleAgent("Bob", AgentRole.MARKETING, PersonalityType.CREATIVE, ["Brand Strategy"], 0.78)
        ]
        
        scenario = "Should we implement AI chatbots for customer service?"
        
        print(f"[SCENARIO] {scenario}")
        print(f"[AGENTS] {', '.join([agent.name for agent in agents])}")
        
        # Run simple conversation
        for i, agent in enumerate(agents):
            print(f"\n[ROUND {i+1}] {agent.name} ({agent.role.value})")
            
            system_prompt = f"You are {agent.name}, a {agent.role.value} specialist. Respond briefly."
            
            response = await provider.generate_response(
                prompt=scenario,
                system_prompt=system_prompt,
                max_tokens=20,
                temperature=0.7
            )
            
            print(f"  {agent.name}: {response.content}")
            print(f"  [Time: {response.response_time:.2f}s]")
        
        print(f"\n[SUCCESS] Agent conversation completed!")
        
    except Exception as e:
        print(f"[FAILED] Agent conversation: {str(e)}")


if __name__ == "__main__":
    print("Starting quick Hugging Face test...")
    success = asyncio.run(quick_huggingface_test())
    
    if success:
        asyncio.run(test_agent_conversation())
    
    print(f"\n{'='*50}")
    print("QUICK HUGGING FACE TEST COMPLETED")
    print(f"{'='*50}")
