"""
Quick integration test for Tachikoma reorganization.

This script tests that all major components can be imported and
basic functionality works.
"""

import sys
import asyncio
from pathlib import Path

# Add project to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print("=" * 60)
print("Tachikoma Integration Test")
print("=" * 60)

# Test 1: Core imports
print("\n[1/6] Testing core imports...")
try:
    from tachikoma.core.orchestrator import TachikomaOrchestrator
    from tachikoma.core.agent import AgentDefinition, AgentRole, AgentPersonality
    from tachikoma.core.llm import LLMProviderFactory, EnhancedAgentLLM
    print("  [OK] Core imports successful")
except Exception as e:
    print(f"  [FAIL] Core imports: {e}")
    sys.exit(1)

# Test 2: UI imports
print("\n[2/6] Testing UI imports...")
try:
    from tachikoma.ui.components import chat, agents, visualization
    print("  [OK] UI components import successful")
except ImportError as e:
    if "streamlit" in str(e) or "plotly" in str(e):
        print(f"  [SKIP] UI imports (dependencies not installed: {e})")
        print("         Install with: pip install streamlit plotly networkx")
    else:
        print(f"  [FAIL] UI imports: {e}")
        sys.exit(1)
except Exception as e:
    print(f"  [FAIL] UI imports: {e}")
    sys.exit(1)

# Test 3: Create orchestrator
print("\n[3/6] Testing orchestrator creation...")
try:
    orchestrator = TachikomaOrchestrator()
    print(f"  [OK] Orchestrator created with {len(orchestrator.agents)} agents")
except Exception as e:
    print(f"  [FAIL] Orchestrator creation: {e}")
    sys.exit(1)

# Test 4: Create agent
print("\n[4/6] Testing agent creation...")
try:
    agent_role = AgentRole(
        name="Test Consultant",
        domain="Testing",
        responsibilities=["Testing", "Validation"],
        required_expertise=["QA", "Testing"],
        decision_authority="Advisory"
    )
    
    agent_personality = AgentPersonality(
        communication_style="Analytical",
        risk_tolerance="Conservative",
        collaboration_style="Collaborative",
        principles=["Quality", "Thoroughness"]
    )
    
    agent_def = AgentDefinition(
        role=agent_role,
        personality=agent_personality,
        context_tags=["test"]
    )
    
    async def add_agent():
        agent_id = await orchestrator.add_agent(agent_def)
        return agent_id
    
    agent_id = asyncio.run(add_agent())
    print(f"  [OK] Agent created with ID: {agent_id}")
except Exception as e:
    print(f"  [FAIL] Agent creation: {e}")
    sys.exit(1)

# Test 5: LLM provider
print("\n[5/6] Testing LLM provider...")
try:
    mock_provider = LLMProviderFactory.create_mock_provider()
    agent_llm = EnhancedAgentLLM(mock_provider)
    print(f"  [OK] LLM provider created: {mock_provider.model_name}")
except Exception as e:
    print(f"  [FAIL] LLM provider: {e}")
    sys.exit(1)

# Test 6: Agent diversity analysis
print("\n[6/6] Testing agent diversity analysis...")
try:
    diversity = orchestrator.get_agent_diversity_analysis()
    print(f"  [OK] Diversity analysis: {diversity['total_agents']} agents")
    print(f"       Roles: {len(diversity['role_diversity'])}")
    print(f"       Domains: {len(diversity['domain_coverage'])}")
except Exception as e:
    print(f"  [FAIL] Diversity analysis: {e}")
    sys.exit(1)

# All tests passed
print("\n" + "=" * 60)
print("ALL TESTS PASSED!")
print("=" * 60)
print("\nProject reorganization successful!")
print("\nNext steps:")
print("  1. Install dependencies: pip install -r requirements.txt")
print("  2. Launch UI: streamlit run tachikoma/ui/app.py")
print("  3. Or use: python tachikoma/main.py --ui")
print()
