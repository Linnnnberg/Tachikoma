# Tachikoma Enhanced Multi-Dimensional Agent Architecture

## Overview

Tachikoma now features a sophisticated multi-dimensional agent architecture that separates **functional roles** from **personality traits** and includes **political spectrum** and **correlated parameters** for realistic multi-agent interactions.

## Architecture Layers

### 1. Role Layer (Functional)
Defines what the agent does and their expertise area.

```python
class AgentRole(BaseModel):
    name: str                    # "Legal Consultant", "Marketing Strategist"
    domain: str                  # "Legal", "Marketing", "Technology"
    responsibilities: List[str]  # What they're responsible for
    required_expertise: List[str] # What they need to know
    decision_authority: str      # "Advisory", "Executive", "Operational"
    context_specific: bool       # True if role adapts to context
```

### 2. Personality Layer (Behavioral)
Defines how the agent communicates and behaves.

```python
class AgentPersonality(BaseModel):
    communication_style: str     # "Direct", "Diplomatic", "Analytical", "Creative"
    risk_tolerance: str          # "Conservative", "Moderate", "Aggressive"
    collaboration_style: str     # "Competitive", "Collaborative", "Independent"
    principles: List[str]        # Core values that guide decisions
```

### 3. Political Profile Layer (Ideological)
Defines political and ideological orientation (optional).

```python
class PoliticalProfile(BaseModel):
    political_spectrum: Optional[PoliticalSpectrum]  # LEFT to RIGHT, APOLITICAL
    economic_view: Optional[EconomicView]            # SOCIALIST to LAISSEZ_FAIRE
    social_view: Optional[SocialView]                # PROGRESSIVE to TRADITIONALIST
    key_issues: List[str]                           # Areas of focus
    ideological_principles: List[str]               # Core beliefs
```

### 4. Correlated Parameters Layer
Parameters that correlate with political/ideological views.

```python
class CorrelatedParameters(BaseModel):
    environmental_stance: Optional[str]    # "Environmentalist", "Pragmatic", "Skeptical"
    technology_approach: Optional[str]     # "Tech-optimist", "Cautious", "Skeptical"
    globalization_view: Optional[str]      # "Globalist", "Moderate", "Nationalist"
    regulation_preference: Optional[str]   # "Pro-regulation", "Balanced", "Deregulation"
    social_equality_focus: Optional[str]   # "High", "Moderate", "Low"
    market_trust: Optional[str]            # "High", "Moderate", "Low"
```

## Complete Agent Definition

```python
class AgentDefinition(BaseModel):
    role: AgentRole
    personality: Optional[AgentPersonality] = None
    political_profile: Optional[PoliticalProfile] = None
    correlated_params: Optional[CorrelatedParameters] = None
    custom_instructions: str = ""
    context_tags: List[str] = []  # "startup", "corporate", "academic"
```

## Real-World Examples

### Example 1: Legal Consultant (Functional + Political)
```python
legal_consultant = AgentDefinition(
    role=AgentRole(
        name="Legal Consultant",
        domain="Legal",
        responsibilities=["Compliance", "Risk assessment", "Regulatory guidance"],
        required_expertise=["Corporate law", "Financial regulations", "Singapore law"],
        decision_authority="Advisory",
        context_specific=True
    ),
    political_profile=PoliticalProfile(
        political_spectrum=PoliticalSpectrum.CENTER,
        economic_view=EconomicView.MIXED_ECONOMY,
        social_view=SocialView.MODERATE,
        key_issues=["Regulatory compliance", "Risk mitigation"],
        ideological_principles=["Rule of law", "Client protection"]
    ),
    correlated_params=CorrelatedParameters(
        regulation_preference="Pro-regulation",
        market_trust="Moderate"
    ),
    context_tags=["startup", "fintech", "singapore"]
)
```

### Example 2: Marketing Strategist (Role + Personality + Political)
```python
marketing_strategist = AgentDefinition(
    role=AgentRole(
        name="Marketing Strategist",
        domain="Marketing",
        responsibilities=["Brand strategy", "Customer acquisition", "Market analysis"],
        required_expertise=["Digital marketing", "Consumer psychology", "Analytics"],
        decision_authority="Operational",
        context_specific=False
    ),
    personality=AgentPersonality(
        communication_style="Creative",
        risk_tolerance="Moderate",
        collaboration_style="Collaborative",
        principles=["Data-driven", "Customer-first", "Ethical marketing"]
    ),
    political_profile=PoliticalProfile(
        political_spectrum=PoliticalSpectrum.CENTER_LEFT,
        economic_view=EconomicView.MIXED_ECONOMY,
        social_view=SocialView.PROGRESSIVE,
        key_issues=["Consumer protection", "Digital privacy", "Inclusive marketing"],
        ideological_principles=["Social responsibility", "Ethical marketing"]
    ),
    correlated_params=CorrelatedParameters(
        technology_approach="Tech-optimist",
        social_equality_focus="High",
        regulation_preference="Balanced"
    ),
    context_tags=["startup", "consumer-facing", "tech"]
)
```

### Example 3: Technical Architect (Minimal Political, Strong Technical)
```python
tech_architect = AgentDefinition(
    role=AgentRole(
        name="Technical Architect",
        domain="Technology",
        responsibilities=["System design", "Technology decisions", "Scalability planning"],
        required_expertise=["Software architecture", "Cloud platforms", "Security"],
        decision_authority="Executive",
        context_specific=False
    ),
    personality=AgentPersonality(
        communication_style="Analytical",
        risk_tolerance="Conservative",
        collaboration_style="Independent",
        principles=["Security first", "Scalable solutions", "Clean code"]
    ),
    political_profile=PoliticalProfile(
        political_spectrum=PoliticalSpectrum.APOLITICAL,
        economic_view=EconomicView.APOLITICAL,
        social_view=SocialView.APOLITICAL,
        key_issues=["Open source", "Privacy", "Technical standards"],
        ideological_principles=["Open standards", "Privacy by design"]
    ),
    correlated_params=CorrelatedParameters(
        technology_approach="Tech-optimist",
        regulation_preference="Balanced",
        market_trust="High"
    ),
    context_tags=["startup", "fintech", "technical"]
)
```

## Context-Aware Agent Suggestion

The system analyzes multiple dimensions when suggesting agents:

### 1. Functional Analysis
- What roles are needed for the task?
- What expertise areas are missing?
- What decision-making authority is required?

### 2. Political Diversity Analysis
- What political perspectives are missing?
- What ideological balance is needed?
- What correlated parameters are relevant?

### 3. Personality Balance Analysis
- What communication styles are needed?
- What collaboration approaches are missing?
- What risk tolerance levels are required?

### 4. Context-Specific Analysis
- What context tags apply?
- What regional/industry expertise is needed?
- What regulatory environment is relevant?

## Use Case Examples

### Startup Scenario: "I want to start a sustainable fintech in Germany"

**Suggested Agents:**
1. **Legal Consultant**
   - Role: German/EU financial regulations
   - Political: Pro-regulation, center
   - Personality: Analytical, conservative
   - Context: fintech, germany, eu

2. **Technical Architect**
   - Role: Fintech systems, GDPR compliance
   - Political: Apolitical, tech-focused
   - Personality: Analytical, independent
   - Context: fintech, privacy, technical

3. **Marketing Strategist**
   - Role: Sustainability branding, customer acquisition
   - Political: Progressive, environmental focus
   - Personality: Creative, collaborative
   - Context: sustainability, consumer-facing

4. **Policy Advisor**
   - Role: EU regulatory expertise
   - Political: Pro-regulation, environmental
   - Personality: Diplomatic, collaborative
   - Context: eu, policy, regulatory

5. **Financial Advisor**
   - Role: Sustainable finance, ESG investing
   - Political: Mixed economy, environmental
   - Personality: Analytical, moderate risk
   - Context: sustainability, finance, esg

### Corporate Strategy: "Develop ESG strategy for multinational corporation"

**Suggested Agents:**
1. **Policy Advisor** (Progressive, environmental focus)
2. **Financial Advisor** (ESG investing expertise)
3. **Legal Consultant** (Regulatory compliance)
4. **Marketing Strategist** (Sustainability branding)
5. **Technical Architect** (Sustainability tech solutions)

## Benefits of Enhanced Architecture

### 1. Real-World Accuracy
- Matches how people actually think and work
- Separates functional expertise from personality
- Includes political/ideological dimensions

### 2. Context Sensitivity
- Different projects need different role/personality mixes
- Adapts to industry, region, and regulatory environment
- Considers user preferences and diversity needs

### 3. Diversity Management
- Ensures balanced perspectives in decision-making
- Prevents groupthink and echo chambers
- Promotes constructive debate and collaboration

### 4. Conflict Simulation
- Realistic debates between different ideological positions
- Simulates real-world decision-making processes
- Tests ideas against multiple perspectives

### 5. Flexibility
- All dimensions are optional based on use case
- Easy to add new roles, personalities, and political profiles
- Supports both technical and policy-focused scenarios

## Implementation Status

### ✅ Completed
- Enhanced agent class definitions
- Multi-dimensional architecture design
- Role suggestion engine with context analysis
- Political spectrum and correlated parameters
- Agent diversity analysis
- Context-aware agent creation

### 🔄 In Progress
- Agent template management system
- Agent persistence and state management
- Enhanced UI for agent management
- Testing framework for multi-agent interactions

### 📋 Pending
- Resource scoring with multi-dimensional analysis
- Inter-agent communication protocols
- Debate and consensus building mechanisms
- Performance optimization and caching
- Comprehensive documentation and examples

## Next Steps

1. **Complete Core Implementation** - Finish remaining core modules
2. **Build UI Interface** - Dynamic agent management and visualization
3. **Implement Testing** - Multi-agent interaction testing
4. **Add Examples** - Real-world use case demonstrations
5. **Performance Optimization** - Caching and efficiency improvements

---

*This enhanced architecture makes Tachikoma much more sophisticated and realistic for complex real-world scenarios, supporting everything from technical startups to policy debates.*
