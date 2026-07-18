#!/usr/bin/env python3
"""
Hugging Face Integration Test.

This script tests the Hugging Face LLM integration with different models
and demonstrates the capabilities for Tachikoma multi-agent conversations.
"""

import asyncio
import sys
import os
import time

# Add the tachikoma package to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tachikoma'))

from tachikoma.simple.agent import SimpleAgent, AgentRole, PersonalityType
from tachikoma.simple.huggingface_optimized import OptimizedHuggingFaceProvider, ConversationHuggingFaceProvider
from tachikoma.simple.llm_providers import HuggingFaceProvider


async def test_huggingface_models():
    """Test different Hugging Face models for Tachikoma."""
    
    print("Tachikoma Hugging Face Integration Test")
    print("=" * 60)
    print("Testing different Hugging Face models for multi-agent conversations")
    print("=" * 60)
    
    # Test models (from small to larger)
    test_models = [
        "microsoft/DialoGPT-small",      # Small, fast
        "microsoft/DialoGPT-medium",     # Medium, balanced
        # "microsoft/DialoGPT-large",    # Large, high quality (requires more memory)
    ]
    
    # Test scenario
    scenario = "Should we invest in AI technology for customer service automation?"
    system_prompt = "You are a legal consultant with expertise in compliance and risk management. Provide professional advice."
    
    print(f"\n[TEST SCENARIO] {scenario}")
    print(f"[SYSTEM PROMPT] {system_prompt}")
    
    results = {}
    
    for model_name in test_models:
        print(f"\n{'='*60}")
        print(f"TESTING MODEL: {model_name}")
        print(f"{'='*60}")
        
        try:
            # Test basic provider
            print(f"\n[1] Testing Basic Hugging Face Provider...")
            basic_provider = HuggingFaceProvider(model_name)
            
            start_time = time.time()
            response = await basic_provider.generate_response(
                prompt=scenario,
                system_prompt=system_prompt,
                max_tokens=50,
                temperature=0.7
            )
            total_time = time.time() - start_time
            
            print(f"[SUCCESS] Basic Provider")
            print(f"  Model: {response.model}")
            print(f"  Response: {response.content}")
            print(f"  Tokens: {response.tokens_used}")
            print(f"  Time: {response.response_time:.2f}s")
            print(f"  Total Time: {total_time:.2f}s")
            
            results[f"{model_name}_basic"] = True
            
        except Exception as e:
            print(f"[FAILED] Basic Provider: {str(e)}")
            results[f"{model_name}_basic"] = False
        
        try:
            # Test optimized provider
            print(f"\n[2] Testing Optimized Hugging Face Provider...")
            optimized_provider = OptimizedHuggingFaceProvider(model_name)
            
            start_time = time.time()
            response = await optimized_provider.generate_response(
                prompt=scenario,
                system_prompt=system_prompt,
                max_tokens=50,
                temperature=0.7
            )
            total_time = time.time() - start_time
            
            print(f"[SUCCESS] Optimized Provider")
            print(f"  Model: {response.model}")
            print(f"  Response: {response.content}")
            print(f"  Tokens: {response.tokens_used}")
            print(f"  Time: {response.response_time:.2f}s")
            print(f"  Total Time: {total_time:.2f}s")
            
            # Show model info
            model_info = optimized_provider.get_model_info()
            print(f"  Device: {model_info['device']}")
            print(f"  Vocab Size: {model_info['vocab_size']}")
            
            results[f"{model_name}_optimized"] = True
            
        except Exception as e:
            print(f"[FAILED] Optimized Provider: {str(e)}")
            results[f"{model_name}_optimized"] = False
        
        try:
            # Test conversation provider
            print(f"\n[3] Testing Conversation Hugging Face Provider...")
            conversation_provider = ConversationHuggingFaceProvider(model_name)
            
            # Test multiple agents
            agents = ["Alice", "Bob", "Charlie"]
            for agent in agents:
                start_time = time.time()
                response = await conversation_provider.generate_response(
                    prompt=scenario,
                    system_prompt=system_prompt,
                    max_tokens=30,
                    temperature=0.7,
                    agent_name=agent
                )
                total_time = time.time() - start_time
                
                print(f"[SUCCESS] {agent} Response")
                print(f"  Response: {response.content}")
                print(f"  Time: {response.response_time:.2f}s")
            
            # Show conversation stats
            stats = conversation_provider.get_conversation_stats()
            print(f"\n[CONVERSATION STATS]")
            print(f"  Active Agents: {stats['active_agents']}")
            print(f"  Total Messages: {stats['total_messages']}")
            print(f"  Agent Histories: {stats['agent_histories']}")
            
            results[f"{model_name}_conversation"] = True
            
        except Exception as e:
            print(f"[FAILED] Conversation Provider: {str(e)}")
            results[f"{model_name}_conversation"] = False
        
        print(f"\n[INFO] Model {model_name} testing completed")
    
    # ========================================
    # SUMMARY
    # ========================================
    print(f"\n{'='*60}")
    print("TEST RESULTS SUMMARY")
    print(f"{'='*60}")
    
    print(f"\nModel Test Results:")
    for test_name, success in results.items():
        status = "[PASS]" if success else "[FAIL]"
        print(f"  {test_name:30} {status}")
    
    passed_tests = sum(results.values())
    total_tests = len(results)
    
    print(f"\nOverall: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == 0:
        print("\n[WARNING] No tests passed!")
        print("  This might be due to:")
        print("  - Insufficient memory for model loading")
        print("  - Network issues downloading models")
        print("  - Missing dependencies")
    elif passed_tests < total_tests:
        print("\n[PARTIAL] Some tests passed!")
        print("  You can use the working providers for Tachikoma")
    else:
        print("\n[SUCCESS] All tests passed!")
        print("  Hugging Face integration is ready for Tachikoma")
    
    # ========================================
    # RECOMMENDATIONS
    # ========================================
    print(f"\n{'='*60}")
    print("RECOMMENDATIONS")
    print(f"{'='*60}")
    
    print(f"\nFor Tachikoma Multi-Agent Conversations:")
    
    if any("conversation" in test and results[test] for test in results):
        print(f"  [RECOMMENDED] Use ConversationHuggingFaceProvider")
        print(f"    - Maintains conversation history per agent")
        print(f"    - Context-aware responses")
        print(f"    - Best for multi-agent scenarios")
    
    if any("optimized" in test and results[test] for test in results):
        print(f"  [ALTERNATIVE] Use OptimizedHuggingFaceProvider")
        print(f"    - Faster generation")
        print(f"    - Lower memory usage")
        print(f"    - Good for simple conversations")
    
    if any("basic" in test and results[test] for test in results):
        print(f"  [FALLBACK] Use basic HuggingFaceProvider")
        print(f"    - Most compatible")
        print(f"    - Standard implementation")
        print(f"    - Good for testing")
    
    print(f"\nModel Selection:")
    print(f"  - DialoGPT-small: Fast, low memory, basic quality")
    print(f"  - DialoGPT-medium: Balanced speed/quality, moderate memory")
    print(f"  - DialoGPT-large: High quality, high memory requirements")
    
    print(f"\nNext Steps:")
    print(f"  1. Choose the best working provider")
    print(f"  2. Integrate with Tachikoma orchestrator")
    print(f"  3. Test with real multi-agent scenarios")
    print(f"  4. Optimize for your specific use case")
    
    print(f"\nHugging Face Integration Test completed!")


async def test_multi_agent_conversation():
    """Test a full multi-agent conversation using Hugging Face."""
    
    print(f"\n{'='*60}")
    print("MULTI-AGENT CONVERSATION TEST")
    print(f"{'='*60}")
    
    try:
        # Create conversation provider
        provider = ConversationHuggingFaceProvider("microsoft/DialoGPT-small")
        
        # Create test agents
        agents = [
            SimpleAgent("Alice", AgentRole.LEGAL, PersonalityType.ANALYTICAL, ["Compliance", "Risk Management"], 0.85),
            SimpleAgent("Bob", AgentRole.MARKETING, PersonalityType.CREATIVE, ["Brand Strategy", "Customer Engagement"], 0.78),
            SimpleAgent("Charlie", AgentRole.TECHNICAL, PersonalityType.PRACTICAL, ["System Architecture", "AI Implementation"], 0.92)
        ]
        
        scenario = "Should we implement AI-powered customer service chatbots?"
        
        print(f"[SCENARIO] {scenario}")
        print(f"[AGENTS] {', '.join([agent.name for agent in agents])}")
        
        # Run conversation
        for i, agent in enumerate(agents):
            print(f"\n[ROUND {i+1}] {agent.name} ({agent.role.value})")
            
            system_prompt = f"You are {agent.name}, a {agent.role.value} specialist. Respond based on your expertise: {', '.join(agent.expertise)}"
            
            response = await provider.generate_response(
                prompt=scenario,
                system_prompt=system_prompt,
                max_tokens=40,
                temperature=0.7,
                agent_name=agent.name
            )
            
            print(f"  {agent.name}: {response.content}")
            print(f"  [Time: {response.response_time:.2f}s, Tokens: {response.tokens_used}]")
        
        # Show final stats
        stats = provider.get_conversation_stats()
        print(f"\n[FINAL STATS]")
        print(f"  Active Agents: {stats['active_agents']}")
        print(f"  Total Messages: {stats['total_messages']}")
        
        print(f"\n[SUCCESS] Multi-agent conversation completed!")
        
    except Exception as e:
        print(f"[FAILED] Multi-agent conversation: {str(e)}")


if __name__ == "__main__":
    asyncio.run(test_huggingface_models())
    asyncio.run(test_multi_agent_conversation())
