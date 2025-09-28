#!/usr/bin/env python3
"""
LLM Providers Demonstration.

This script demonstrates different LLM providers available for Tachikoma:
- OpenAI (GPT models)
- Hugging Face (open source models)
- Llama (Meta's models)
- Mock (for testing)
- Hybrid (multiple providers with fallbacks)
"""

import asyncio
import sys
import os
import time

# Add the tachikoma package to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tachikoma'))

from tachikoma.simple.agent import SimpleAgent, AgentRole, PersonalityType
from tachikoma.simple.llm_providers import (
    LLMProviderFactory, 
    OpenAIProvider, 
    HuggingFaceProvider, 
    LlamaProvider, 
    MockProvider, 
    HybridProvider
)


async def test_provider(provider, name: str, prompt: str, system_prompt: str = ""):
    """Test a specific LLM provider."""
    print(f"\n{'='*60}")
    print(f"TESTING {name.upper()}")
    print(f"{'='*60}")
    
    try:
        start_time = time.time()
        response = await provider.generate_response(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=100,
            temperature=0.7
        )
        total_time = time.time() - start_time
        
        print(f"[SUCCESS]")
        print(f"Provider: {response.provider}")
        print(f"Model: {response.model}")
        print(f"Response: {response.content}")
        print(f"Tokens Used: {response.tokens_used}")
        print(f"Response Time: {response.response_time:.2f}s")
        print(f"Total Time: {total_time:.2f}s")
        print(f"Cost: ${response.cost:.4f}")
        
        # Show usage stats
        stats = provider.get_usage_stats()
        print(f"Total Tokens: {stats['total_tokens']}")
        print(f"Total Cost: ${stats['total_cost']:.4f}")
        
        return True
        
    except Exception as e:
        print(f"[FAILED] {str(e)}")
        return False


async def demonstrate_llm_providers():
    """Demonstrate all available LLM providers."""
    
    print("Tachikoma LLM Providers Demonstration")
    print("=" * 60)
    print("This demo shows how to use different LLM providers:")
    print("1. Mock Provider (for testing)")
    print("2. OpenAI Provider (GPT models)")
    print("3. Hugging Face Provider (open source)")
    print("4. Llama Provider (Meta's models)")
    print("5. Hybrid Provider (multiple with fallbacks)")
    print("=" * 60)
    
    # Test scenario
    scenario = "Should we invest in AI technology for customer service automation?"
    system_prompt = "You are a legal consultant with expertise in compliance and risk management. Provide professional advice."
    
    print(f"\n[SCENARIO] {scenario}")
    print(f"[SYSTEM PROMPT] {system_prompt}")
    
    # Test results
    results = {}
    
    # ========================================
    # 1. MOCK PROVIDER (Always works)
    # ========================================
    print(f"\n{'='*60}")
    print("1. MOCK PROVIDER (Testing)")
    print(f"{'='*60}")
    
    mock_provider = LLMProviderFactory.create_mock_provider()
    success = await test_provider(mock_provider, "Mock Provider", scenario, system_prompt)
    results["Mock"] = success
    
    # ========================================
    # 2. OPENAI PROVIDER (Requires API key)
    # ========================================
    print(f"\n{'='*60}")
    print("2. OPENAI PROVIDER (Requires API key)")
    print(f"{'='*60}")
    
    # Check if OpenAI API key is available
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        try:
            openai_provider = LLMProviderFactory.create_openai_provider(openai_key, "gpt-3.5-turbo")
            success = await test_provider(openai_provider, "OpenAI GPT-3.5-turbo", scenario, system_prompt)
            results["OpenAI"] = success
        except Exception as e:
            print(f"[FAILED] OpenAI setup failed: {str(e)}")
            results["OpenAI"] = False
    else:
        print("[SKIP] OPENAI_API_KEY not set. Skipping OpenAI test.")
        print("   To test OpenAI, set your API key:")
        print("   export OPENAI_API_KEY='your-api-key-here'")
        results["OpenAI"] = False
    
    # ========================================
    # 3. HUGGING FACE PROVIDER (Requires models)
    # ========================================
    print(f"\n{'='*60}")
    print("3. HUGGING FACE PROVIDER (Requires models)")
    print(f"{'='*60}")
    
    try:
        # Try a small model that should be available
        hf_provider = LLMProviderFactory.create_huggingface_provider("microsoft/DialoGPT-small")
        success = await test_provider(hf_provider, "Hugging Face DialoGPT", scenario, system_prompt)
        results["Hugging Face"] = success
    except Exception as e:
        print(f"[FAILED] Hugging Face setup failed: {str(e)}")
        print("   This might be due to:")
        print("   - Missing transformers library: pip install transformers torch")
        print("   - Insufficient memory for model loading")
        print("   - Network issues downloading model")
        results["Hugging Face"] = False
    
    # ========================================
    # 4. LLAMA PROVIDER (Requires model files)
    # ========================================
    print(f"\n{'='*60}")
    print("4. LLAMA PROVIDER (Requires model files)")
    print(f"{'='*60}")
    
    # Check if Llama model is available
    llama_path = os.getenv("LLAMA_MODEL_PATH")
    if llama_path and os.path.exists(llama_path):
        try:
            llama_provider = LLMProviderFactory.create_llama_provider(llama_path, "llama-2-7b")
            success = await test_provider(llama_provider, "Llama 2 7B", scenario, system_prompt)
            results["Llama"] = success
        except Exception as e:
            print(f"[FAILED] Llama setup failed: {str(e)}")
            results["Llama"] = False
    else:
        print("[SKIP] LLAMA_MODEL_PATH not set or file not found. Skipping Llama test.")
        print("   To test Llama, download a model and set the path:")
        print("   export LLAMA_MODEL_PATH='/path/to/llama-model.gguf'")
        print("   You can download models from: https://huggingface.co/TheBloke")
        results["Llama"] = False
    
    # ========================================
    # 5. HYBRID PROVIDER (Multiple with fallbacks)
    # ========================================
    print(f"\n{'='*60}")
    print("5. HYBRID PROVIDER (Multiple with fallbacks)")
    print(f"{'='*60}")
    
    try:
        # Create hybrid provider with available providers
        hybrid_provider = LLMProviderFactory.create_hybrid_provider(
            openai_key=openai_key,
            huggingface_model="microsoft/DialoGPT-small",
            llama_path=llama_path
        )
        
        success = await test_provider(hybrid_provider, "Hybrid Provider", scenario, system_prompt)
        results["Hybrid"] = success
        
        # Show fallback stats
        fallback_stats = hybrid_provider.get_fallback_stats()
        print(f"\nHybrid Provider Stats:")
        print(f"  Fallback Count: {fallback_stats['fallback_count']}")
        print(f"  Total Providers: {fallback_stats['total_providers']}")
        print(f"  Fallback Rate: {fallback_stats['fallback_rate']:.2%}")
        
    except Exception as e:
        print(f"[FAILED] Hybrid provider setup failed: {str(e)}")
        results["Hybrid"] = False
    
    # ========================================
    # SUMMARY
    # ========================================
    print(f"\n{'='*60}")
    print("TEST RESULTS SUMMARY")
    print(f"{'='*60}")
    
    print(f"\nProvider Status:")
    for provider, success in results.items():
        status = "[WORKING]" if success else "[FAILED]"
        print(f"  {provider:15} {status}")
    
    working_count = sum(results.values())
    total_count = len(results)
    
    print(f"\nOverall: {working_count}/{total_count} providers working")
    
    if working_count == 0:
        print("\n[WARNING] No providers are working!")
        print("   This is normal if you haven't set up any LLM providers yet.")
        print("   The Mock provider should always work for testing.")
    elif working_count == 1:
        print("\n[SUCCESS] At least one provider is working!")
        print("   You can start using Tachikoma with the available provider.")
    else:
        print("\n[SUCCESS] Multiple providers are working!")
        print("   You have good redundancy and can use the hybrid approach.")
    
    # ========================================
    # SETUP INSTRUCTIONS
    # ========================================
    print(f"\n{'='*60}")
    print("SETUP INSTRUCTIONS")
    print(f"{'='*60}")
    
    print(f"\nTo set up different providers:")
    
    print(f"\n1. MOCK PROVIDER (Already working)")
    print(f"   - No setup required")
    print(f"   - Good for testing and development")
    print(f"   - Free but limited quality")
    
    print(f"\n2. OPENAI PROVIDER")
    print(f"   - Install: pip install openai")
    print(f"   - Get API key: https://platform.openai.com/api-keys")
    print(f"   - Set: export OPENAI_API_KEY='your-key'")
    print(f"   - Cost: ~$0.08 per conversation")
    
    print(f"\n3. HUGGING FACE PROVIDER")
    print(f"   - Install: pip install transformers torch")
    print(f"   - Models download automatically")
    print(f"   - Free but requires significant memory")
    print(f"   - Good for: privacy, customization")
    
    print(f"\n4. LLAMA PROVIDER")
    print(f"   - Install: pip install llama-cpp-python")
    print(f"   - Download model: https://huggingface.co/TheBloke")
    print(f"   - Set: export LLAMA_MODEL_PATH='/path/to/model.gguf'")
    print(f"   - Free but requires powerful hardware")
    
    print(f"\n5. HYBRID PROVIDER")
    print(f"   - Combines multiple providers")
    print(f"   - Automatic fallback if one fails")
    print(f"   - Best for production use")
    
    print(f"\n{'='*60}")
    print("RECOMMENDATIONS")
    print(f"{'='*60}")
    
    print(f"\nFor Development:")
    print(f"  - Start with Mock provider")
    print(f"  - Add OpenAI for better quality")
    print(f"  - Use hybrid for production")
    
    print(f"\nFor Production:")
    print(f"  - Use hybrid approach")
    print(f"  - OpenAI as primary (quality)")
    print(f"  - Hugging Face as fallback (cost)")
    print(f"  - Llama for privacy-critical scenarios")
    
    print(f"\nFor Cost Optimization:")
    print(f"  - Use Hugging Face or Llama")
    print(f"  - Self-host models")
    print(f"  - Implement caching")
    
    print(f"\nLLM Providers Demo completed!")


if __name__ == "__main__":
    asyncio.run(demonstrate_llm_providers())
