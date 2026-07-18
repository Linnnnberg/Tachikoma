#!/usr/bin/env python3
"""
Detailed Phase 1 Tachikoma System Demo with Extended Conversation.

This script demonstrates the simplified Phase 1 system with
a comprehensive 500+ word conversation and detailed debugging information.
"""

import asyncio
import sys
import os
import time
from datetime import datetime

# Add the tachikoma package to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tachikoma'))

from tachikoma.simple.agent import SimpleAgent, AgentRole, PersonalityType
from tachikoma.simple.orchestrator import SimpleOrchestrator
from tachikoma.simple.communication import MessageType


class DebugOrchestrator(SimpleOrchestrator):
    """Enhanced orchestrator with debugging capabilities."""
    
    def __init__(self):
        super().__init__()
        self.debug_mode = True
        self.conversation_log = []
        self.step_counter = 0
    
    def debug_log(self, message: str, data: dict = None):
        """Log debug information."""
        if self.debug_mode:
            self.step_counter += 1
            timestamp = datetime.now().strftime("%H:%M:%S")
            log_entry = {
                "step": self.step_counter,
                "timestamp": timestamp,
                "message": message,
                "data": data or {}
            }
            self.conversation_log.append(log_entry)
            print(f"\n[DEBUG {self.step_counter:02d}] {timestamp} - {message}")
            if data:
                for key, value in data.items():
                    print(f"         {key}: {value}")
    
    def send_message(self, from_agent: str, to_agent: str, content: str) -> str:
        """Send message with debugging."""
        self.debug_log(f"Sending message from {from_agent} to {to_agent}", {
            "content": content[:50] + "..." if len(content) > 50 else content,
            "message_length": len(content)
        })
        
        result = super().send_message(from_agent, to_agent, content)
        
        # Update agent message count
        if from_agent in self.agents:
            self.agents[from_agent].message_count += 1
            self.debug_log(f"Updated message count for {from_agent}", {
                "new_count": self.agents[from_agent].message_count
            })
        
        return result
    
    def simulate_agent_interaction(self, agent_name: str, context: str) -> str:
        """Simulate agent interaction with detailed debugging."""
        if agent_name not in self.agents:
            return "Agent not found"
        
        agent = self.agents[agent_name]
        
        self.debug_log(f"Simulating interaction for {agent_name}", {
            "agent_role": agent.role.value,
            "agent_personality": agent.personality.value,
            "context": context[:50] + "..." if len(context) > 50 else context,
            "current_performance": agent.performance_score
        })
        
        # Generate response based on agent characteristics
        response = self._generate_detailed_response(agent, context)
        
        self.debug_log(f"Generated response for {agent_name}", {
            "response_length": len(response),
            "response_preview": response[:100] + "..." if len(response) > 100 else response
        })
        
        return response
    
    def _generate_detailed_response(self, agent: SimpleAgent, context: str) -> str:
        """Generate detailed responses based on agent characteristics."""
        
        if agent.role == AgentRole.LEGAL:
            if "compliance" in context.lower() or "legal" in context.lower():
                return ("As a legal consultant, I need to emphasize the critical importance of compliance in this decision. "
                       "We must conduct a thorough risk assessment and ensure all regulatory requirements are met. "
                       "I recommend we review the relevant legal frameworks, identify potential liabilities, "
                       "and establish clear compliance protocols before proceeding. This is not just about avoiding "
                       "penalties, but about protecting our company's reputation and ensuring long-term sustainability.")
            elif "investment" in context.lower() or "budget" in context.lower():
                return ("From a legal perspective, any investment decision must be evaluated through the lens of regulatory compliance. "
                       "I need to review the legal implications, potential contractual obligations, and regulatory requirements. "
                       "We should also consider intellectual property rights, data protection laws, and any industry-specific regulations. "
                       "I recommend we conduct a comprehensive legal due diligence process before making any commitments.")
            else:
                return ("As your legal advisor, I must highlight the importance of considering all legal implications in this decision. "
                       "We need to evaluate potential risks, compliance requirements, and regulatory considerations. "
                       "I suggest we conduct a thorough legal analysis to identify any potential issues and ensure we're "
                       "operating within all applicable legal frameworks. This proactive approach will help us avoid "
                       "costly legal problems down the road.")
        
        elif agent.role == AgentRole.MARKETING:
            if "marketing" in context.lower() or "brand" in context.lower():
                return ("From a marketing strategy perspective, this is an exciting opportunity to strengthen our brand positioning. "
                       "I recommend we conduct comprehensive market research to understand customer needs, competitive landscape, "
                       "and market trends. We should develop a multi-channel marketing approach that leverages digital platforms, "
                       "content marketing, and strategic partnerships. The key is to create compelling value propositions that "
                       "resonate with our target audience and differentiate us from competitors.")
            elif "investment" in context.lower() or "budget" in context.lower():
                return ("This investment decision has significant marketing implications that we need to carefully consider. "
                       "I suggest we analyze the market opportunity, customer demand, and competitive positioning. "
                       "We should evaluate how this investment aligns with our brand strategy and customer acquisition goals. "
                       "I recommend developing a comprehensive go-to-market strategy that includes customer segmentation, "
                       "pricing strategy, and marketing channel optimization.")
            else:
                return ("As a marketing strategist, I see this as an opportunity to enhance our market position and customer engagement. "
                       "We need to consider how this decision impacts our brand perception, customer experience, and market competitiveness. "
                       "I recommend we conduct customer research to understand their needs and preferences, then develop "
                       "a strategic marketing plan that aligns with our business objectives and market opportunities.")
        
        elif agent.role == AgentRole.TECHNICAL:
            if "technical" in context.lower() or "system" in context.lower():
                return ("From a technical architecture perspective, this requires a systematic approach to ensure scalability and maintainability. "
                       "I recommend we design a robust system architecture that follows best practices for security, performance, and reliability. "
                       "We need to consider data architecture, API design, integration patterns, and deployment strategies. "
                       "I suggest we implement proper monitoring, logging, and error handling mechanisms. "
                       "The technical implementation should be modular, testable, and well-documented for long-term maintainability.")
            elif "investment" in context.lower() or "budget" in context.lower():
                return ("This investment decision has significant technical implications that require careful analysis. "
                       "I need to evaluate the technical feasibility, resource requirements, and implementation timeline. "
                       "We should consider the technology stack, infrastructure needs, and integration requirements. "
                       "I recommend conducting a technical proof-of-concept to validate our approach and identify potential challenges. "
                       "We also need to plan for scalability, security, and maintenance considerations.")
            else:
                return ("As a technical architect, I need to ensure this decision is technically sound and implementable. "
                       "We should evaluate the technical requirements, assess the feasibility of implementation, "
                       "and plan for proper system integration. I recommend we consider the technical architecture, "
                       "data flow, security requirements, and performance implications. "
                       "We need to ensure the solution is scalable, maintainable, and follows industry best practices.")
        
        else:
            return ("I'll analyze this situation from a comprehensive perspective and provide my recommendations. "
                   "We need to consider all aspects of this decision, including business impact, technical feasibility, "
                   "and strategic alignment. I suggest we gather more information, evaluate the options, "
                   "and develop a well-informed recommendation that serves our long-term objectives.")


def create_detailed_team():
    """Create a detailed team of agents for comprehensive testing."""
    
    # Legal Consultant with detailed expertise
    legal_agent = SimpleAgent(
        name="Alice",
        role=AgentRole.LEGAL,
        personality=PersonalityType.ANALYTICAL,
        expertise=["Corporate Law", "Compliance Management", "Risk Assessment", "Contract Negotiation", "Regulatory Affairs"],
        performance_score=0.85
    )
    
    # Marketing Strategist with creative focus
    marketing_agent = SimpleAgent(
        name="Bob",
        role=AgentRole.MARKETING,
        personality=PersonalityType.CREATIVE,
        expertise=["Digital Marketing", "Brand Strategy", "Market Research", "Customer Analytics", "Content Marketing"],
        performance_score=0.78
    )
    
    # Technical Architect with practical approach
    tech_agent = SimpleAgent(
        name="Charlie",
        role=AgentRole.TECHNICAL,
        personality=PersonalityType.PRACTICAL,
        expertise=["System Architecture", "Software Development", "Cloud Computing", "DevOps", "Security"],
        performance_score=0.92
    )
    
    # General Manager for coordination
    general_agent = SimpleAgent(
        name="Diana",
        role=AgentRole.GENERAL,
        personality=PersonalityType.COLLABORATIVE,
        expertise=["Project Management", "Strategic Planning", "Team Leadership", "Budget Management"],
        performance_score=0.80
    )
    
    return [legal_agent, marketing_agent, tech_agent, general_agent]


def demonstrate_detailed_system():
    """Demonstrate the system with detailed debugging and extended conversation."""
    
    print("Tachikoma Detailed Phase 1 System Demo")
    print("=" * 60)
    print("This demo includes:")
    print("- Extended 500+ word conversation")
    print("- Detailed debugging information")
    print("- Step-by-step process tracking")
    print("- Performance monitoring")
    print("=" * 60)
    
    # Create team
    print("\n[INITIALIZATION] Creating detailed team...")
    agents = create_detailed_team()
    
    # Initialize orchestrator with debugging
    orchestrator = DebugOrchestrator()
    
    # Add agents
    print("\n[INITIALIZATION] Adding agents to system...")
    for agent in agents:
        orchestrator.add_agent(agent)
        orchestrator.debug_log(f"Added agent {agent.name}", {
            "role": agent.role.value,
            "personality": agent.personality.value,
            "expertise_count": len(agent.expertise),
            "performance_score": agent.performance_score
        })
    
    # Show detailed agent information
    print("\n" + "="*60)
    print("AGENT DETAILS")
    print("="*60)
    
    for agent in agents:
        print(f"\n{agent.name} ({agent.role.value.upper()}):")
        print(f"  Personality: {agent.get_personality_description()}")
        print(f"  Role: {agent.get_role_description()}")
        print(f"  Expertise: {', '.join(agent.expertise)}")
        print(f"  Performance Score: {agent.performance_score:.2f}")
        print(f"  Resource Allocation: {agent.resource_allocation:.1f}")
    
    # Start extended conversation
    print("\n" + "="*60)
    print("EXTENDED CONVERSATION SIMULATION")
    print("="*60)
    
    # Scenario: Should we invest in AI technology for customer service?
    scenario = "Should we invest in AI technology for customer service automation?"
    
    print(f"\n[SCENARIO] {scenario}")
    print("\n[CONVERSATION] Starting extended multi-agent discussion...")
    
    # Step 1: Diana (General Manager) initiates the discussion
    orchestrator.debug_log("Diana initiates the discussion")
    diana_opening = ("I'd like to discuss a significant investment opportunity that could transform our customer service operations. "
                    "We're considering implementing AI-powered customer service automation to improve efficiency and customer satisfaction. "
                    "This would involve chatbots, automated ticket routing, and intelligent response systems. "
                    "I need input from all departments to make an informed decision.")
    
    orchestrator.send_message("Diana", "", diana_opening)
    
    # Step 2: Alice (Legal) responds with compliance concerns
    time.sleep(0.5)  # Simulate thinking time
    alice_response = orchestrator.simulate_agent_interaction("Alice", scenario)
    orchestrator.send_message("Alice", "Diana", alice_response)
    
    # Step 3: Bob (Marketing) provides market perspective
    time.sleep(0.5)
    bob_response = orchestrator.simulate_agent_interaction("Bob", scenario)
    orchestrator.send_message("Bob", "Diana", bob_response)
    
    # Step 4: Charlie (Technical) gives technical analysis
    time.sleep(0.5)
    charlie_response = orchestrator.simulate_agent_interaction("Charlie", scenario)
    orchestrator.send_message("Charlie", "Diana", charlie_response)
    
    # Step 5: Diana asks follow-up questions
    time.sleep(0.5)
    diana_followup = ("Thank you for your initial thoughts. I have some follow-up questions: "
                     "Alice, what specific legal risks should we be most concerned about? "
                     "Bob, how do you see this impacting our customer experience and brand perception? "
                     "Charlie, what would be the technical implementation timeline and resource requirements?")
    
    orchestrator.send_message("Diana", "", diana_followup)
    
    # Step 6: Detailed responses from each agent
    time.sleep(0.5)
    alice_detailed = ("The primary legal risks include data privacy compliance, particularly with GDPR and CCPA regulations. "
                     "We need to ensure customer data is handled properly, consent is obtained, and data retention policies are followed. "
                     "There are also liability concerns if the AI system makes incorrect decisions that harm customers. "
                     "I recommend we conduct a comprehensive legal audit and establish clear liability frameworks.")
    
    orchestrator.send_message("Alice", "Diana", alice_detailed)
    
    time.sleep(0.5)
    bob_detailed = ("From a marketing perspective, AI customer service can significantly enhance our brand perception if implemented correctly. "
                   "Customers expect fast, accurate responses, and AI can provide 24/7 availability. However, we need to ensure the AI maintains "
                   "our brand voice and can handle complex queries appropriately. I suggest we develop a phased rollout with extensive testing "
                   "and customer feedback integration to maintain quality standards.")
    
    orchestrator.send_message("Bob", "Diana", bob_detailed)
    
    time.sleep(0.5)
    charlie_detailed = ("The technical implementation would require approximately 6-8 months for full deployment. We'd need to integrate with "
                       "our existing CRM system, develop natural language processing capabilities, and create a robust training pipeline. "
                       "The infrastructure requirements include cloud computing resources, data storage, and real-time processing capabilities. "
                       "I estimate we'd need 3-4 additional developers and a data scientist for the implementation phase.")
    
    orchestrator.send_message("Charlie", "Diana", charlie_detailed)
    
    # Step 7: Start formal debate
    print("\n" + "="*60)
    print("FORMAL DEBATE SESSION")
    print("="*60)
    
    orchestrator.debug_log("Starting formal debate session")
    debate_id = orchestrator.start_debate(
        "Should we proceed with AI customer service investment?",
        ["Alice", "Bob", "Charlie", "Diana"],
        "Diana"
    )
    
    # Step 8: Agents present their positions
    time.sleep(0.5)
    alice_position = ("I recommend proceeding with caution. The legal risks are manageable with proper planning, but we must prioritize "
                     "compliance and customer protection. I suggest a limited pilot program with clear legal frameworks before full deployment.")
    
    orchestrator.add_debate_message(debate_id, "Alice", alice_position)
    
    time.sleep(0.5)
    bob_position = ("I strongly support this investment. The market opportunity is significant, and our competitors are already implementing "
                   "similar solutions. We risk falling behind if we don't act quickly. I recommend a bold, comprehensive implementation "
                   "that positions us as an industry leader in customer service innovation.")
    
    orchestrator.add_debate_message(debate_id, "Bob", bob_position)
    
    time.sleep(0.5)
    charlie_position = ("I support the investment but recommend a phased approach. The technical complexity requires careful planning and "
                       "testing. I suggest starting with a pilot program to validate our approach, then scaling based on results. "
                       "This reduces technical risk while allowing us to learn and improve the system.")
    
    orchestrator.add_debate_message(debate_id, "Charlie", charlie_position)
    
    time.sleep(0.5)
    diana_position = ("I appreciate all your perspectives. Based on the analysis, I believe we should proceed with a balanced approach that "
                     "addresses legal concerns, leverages market opportunities, and manages technical risks. I propose a phased implementation "
                     "with strong legal oversight and continuous market feedback.")
    
    orchestrator.add_debate_message(debate_id, "Diana", diana_position)
    
    # Step 9: Cast votes
    print("\n[VOTING] Agents casting their votes...")
    orchestrator.cast_vote(debate_id, "Alice", "Proceed with Caution")
    orchestrator.cast_vote(debate_id, "Bob", "Full Investment")
    orchestrator.cast_vote(debate_id, "Charlie", "Phased Approach")
    orchestrator.cast_vote(debate_id, "Diana", "Balanced Approach")
    
    # Step 10: Get debate results
    debate = orchestrator.get_debate(debate_id)
    if debate:
        print(f"\n[DEBATE RESULTS]")
        print(f"  Topic: {debate.topic}")
        print(f"  Total Messages: {len(debate.messages)}")
        print(f"  Votes: {debate.votes}")
        print(f"  Consensus Reached: {debate.consensus_reached}")
        if debate.consensus_decision:
            print(f"  Final Decision: {debate.consensus_decision}")
    
    # Step 11: Performance tracking and updates
    print("\n" + "="*60)
    print("PERFORMANCE TRACKING")
    print("="*60)
    
    # Update performance metrics based on conversation
    orchestrator.debug_log("Updating performance metrics based on conversation quality")
    
    # Alice performed well in legal analysis
    orchestrator.update_agent_performance("Alice", "response_quality", 0.95)
    orchestrator.update_agent_performance("Alice", "collaboration", 0.85)
    orchestrator.update_agent_performance("Alice", "communication", 0.90)
    
    # Bob showed good market insight
    orchestrator.update_agent_performance("Bob", "response_quality", 0.88)
    orchestrator.update_agent_performance("Bob", "collaboration", 0.92)
    orchestrator.update_agent_performance("Bob", "communication", 0.87)
    
    # Charlie provided solid technical analysis
    orchestrator.update_agent_performance("Charlie", "response_quality", 0.92)
    orchestrator.update_agent_performance("Charlie", "collaboration", 0.88)
    orchestrator.update_agent_performance("Charlie", "communication", 0.89)
    
    # Diana coordinated well
    orchestrator.update_agent_performance("Diana", "response_quality", 0.90)
    orchestrator.update_agent_performance("Diana", "collaboration", 0.95)
    orchestrator.update_agent_performance("Diana", "communication", 0.93)
    
    # Show updated performance
    print("\n[PERFORMANCE UPDATE] Agent performance after conversation:")
    for agent_name in ["Alice", "Bob", "Charlie", "Diana"]:
        perf = orchestrator.get_agent_performance(agent_name)
        print(f"\n{agent_name}:")
        print(f"  Overall Score: {perf['performance_score']:.2f}")
        metrics = perf['metrics']
        print(f"  Response Quality: {metrics['response_quality']:.2f}")
        print(f"  Collaboration: {metrics['collaboration']:.2f}")
        print(f"  Communication: {metrics['communication']:.2f}")
        print(f"  Task Completion: {metrics['task_completion']:.2f}")
    
    # Step 12: Resource allocation
    print("\n" + "="*60)
    print("RESOURCE ALLOCATION")
    print("="*60)
    
    orchestrator.debug_log("Calculating resource allocation based on performance")
    allocation = orchestrator.allocate_resources(100.0)
    
    print("\n[RESOURCE ALLOCATION] Resources distributed based on performance:")
    for agent_name, resources in allocation.items():
        print(f"  {agent_name}: {resources:.1f} resources")
    
    # Step 13: System status and conversation summary
    print("\n" + "="*60)
    print("SYSTEM STATUS & CONVERSATION SUMMARY")
    print("="*60)
    
    status = orchestrator.get_system_status()
    print(f"\n[SYSTEM STATUS]")
    print(f"  Total Agents: {status['total_agents']}")
    print(f"  Conversation State: {status['conversation_state']}")
    print(f"  Active Debates: {status['active_debates']}")
    print(f"  Average Performance: {status['system_performance']['average_performance']:.2f}")
    
    # Conversation word count
    total_words = 0
    for log_entry in orchestrator.conversation_log:
        if 'data' in log_entry and 'content' in log_entry['data']:
            content = log_entry['data']['content']
            if isinstance(content, str):
                total_words += len(content.split())
    
    print(f"\n[CONVERSATION SUMMARY]")
    print(f"  Total Debug Steps: {len(orchestrator.conversation_log)}")
    print(f"  Estimated Word Count: {total_words}+ words")
    print(f"  Messages Exchanged: {sum(agent.message_count for agent in orchestrator.agents.values())}")
    
    print("\n[DEBUG LOG SUMMARY]")
    for i, log_entry in enumerate(orchestrator.conversation_log[-10:], 1):  # Show last 10 steps
        print(f"  {i:2d}. {log_entry['message']}")
    
    print("\n" + "="*60)
    print("DETAILED PHASE 1 DEMO COMPLETED SUCCESSFULLY!")
    print("="*60)
    print("Key Features Demonstrated:")
    print("+ Extended 500+ word conversation")
    print("+ Detailed debugging and step tracking")
    print("+ Multi-agent collaboration and debate")
    print("+ Performance tracking and updates")
    print("+ Resource allocation based on performance")
    print("+ Comprehensive system monitoring")


if __name__ == "__main__":
    demonstrate_detailed_system()
