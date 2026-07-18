"""
Agent Management Component for Tachikoma.

Handles creating, viewing, and managing agents in the system.
"""

import streamlit as st
import asyncio
from tachikoma.core.agent import (
    AgentDefinition, AgentRole, AgentPersonality,
    PoliticalProfile, CorrelatedParameters,
    PoliticalSpectrum, EconomicView, SocialView
)


def render_agent_management():
    """Render the agent management interface."""
    st.header("👥 Agent Management")
    
    orchestrator = st.session_state.orchestrator
    
    tab1, tab2, tab3 = st.tabs(["📋 Current Agents", "➕ Add Agent", "💡 Suggest Agents"])
    
    with tab1:
        render_current_agents()
    
    with tab2:
        render_add_agent_form()
    
    with tab3:
        render_agent_suggestions()


def render_current_agents():
    """Display current agents in the system."""
    orchestrator = st.session_state.orchestrator
    
    if len(orchestrator.agents) == 0:
        st.info("No agents in the system. Add some using the **Add Agent** tab!")
        return
    
    st.subheader(f"Active Agents ({len(orchestrator.agents)})")
    
    for agent_id, agent_state in orchestrator.agents.items():
        definition = agent_state.definition
        
        with st.expander(f"🤖 {definition.role.name} - {definition.role.domain}", expanded=False):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**Role:** {definition.role.name}")
                st.markdown(f"**Domain:** {definition.role.domain}")
                st.markdown(f"**Decision Authority:** {definition.role.decision_authority}")
                
                st.markdown("**Responsibilities:**")
                for resp in definition.role.responsibilities:
                    st.markdown(f"- {resp}")
                
                st.markdown("**Expertise:**")
                for exp in definition.role.required_expertise:
                    st.markdown(f"- {exp}")
                
                if definition.personality:
                    st.divider()
                    st.markdown("**Personality:**")
                    st.markdown(f"- Communication: {definition.personality.communication_style}")
                    st.markdown(f"- Risk Tolerance: {definition.personality.risk_tolerance}")
                    st.markdown(f"- Collaboration: {definition.personality.collaboration_style}")
                    st.markdown(f"- Principles: {', '.join(definition.personality.principles)}")
                
                if definition.political_profile and definition.political_profile.political_spectrum:
                    st.divider()
                    st.markdown("**Political Profile:**")
                    st.markdown(f"- Spectrum: {definition.political_profile.political_spectrum.value}")
                    if definition.political_profile.economic_view:
                        st.markdown(f"- Economic: {definition.political_profile.economic_view.value}")
                    if definition.political_profile.social_view:
                        st.markdown(f"- Social: {definition.political_profile.social_view.value}")
                
                if definition.context_tags:
                    st.divider()
                    st.markdown(f"**Tags:** {', '.join(definition.context_tags)}")
            
            with col2:
                st.metric("Performance", f"{agent_state.performance_score:.2f}")
                st.metric("Energy", f"{agent_state.energy_level:.1%}")
                
                if st.button(f"🗑️ Remove", key=f"remove_{agent_id}"):
                    asyncio.run(orchestrator.remove_agent(agent_id))
                    st.success(f"Removed {definition.role.name}")
                    st.rerun()


def render_add_agent_form():
    """Render form for adding new agents."""
    st.subheader("Create New Agent")
    
    template = st.selectbox(
        "Start from Template",
        ["Custom", "Legal Consultant", "Marketing Strategist", "Technical Architect", 
         "Financial Advisor", "Policy Advisor"],
        help="Choose a template or create a custom agent"
    )
    
    if template != "Custom":
        if st.button(f"Add {template}", type="primary"):
            agent_def = create_template_agent(template)
            asyncio.run(st.session_state.orchestrator.add_agent(agent_def))
            st.success(f"Added {template}!")
            st.rerun()
        
        st.info("Or customize the agent below:")
    
    with st.form("add_agent_form"):
        st.subheader("Role Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            role_name = st.text_input("Role Name", "Consultant")
            domain = st.text_input("Domain", "General")
            decision_authority = st.selectbox("Decision Authority", ["Advisory", "Executive", "Operational"])
        
        with col2:
            responsibilities = st.text_area("Responsibilities (one per line)", "Strategic planning\nRisk assessment")
            expertise = st.text_area("Required Expertise (one per line)", "Industry analysis\nMarket research")
        
        st.subheader("Personality (Optional)")
        
        add_personality = st.checkbox("Add Personality", value=True)
        
        personality = None
        if add_personality:
            col1, col2 = st.columns(2)
            
            with col1:
                comm_style = st.selectbox("Communication Style", ["Direct", "Diplomatic", "Analytical", "Creative"])
                risk_tolerance = st.selectbox("Risk Tolerance", ["Conservative", "Moderate", "Aggressive"])
            
            with col2:
                collab_style = st.selectbox("Collaboration Style", ["Competitive", "Collaborative", "Independent"])
                principles = st.text_input("Principles (comma-separated)", "Integrity, Excellence, Innovation")
        
        st.subheader("Political Profile (Optional)")
        
        add_political = st.checkbox("Add Political Profile", value=False)
        
        political_profile = None
        if add_political:
            col1, col2 = st.columns(2)
            
            with col1:
                political_spectrum = st.selectbox(
                    "Political Spectrum",
                    [e.value for e in PoliticalSpectrum]
                )
                economic_view = st.selectbox(
                    "Economic View",
                    [e.value for e in EconomicView]
                )
            
            with col2:
                social_view = st.selectbox(
                    "Social View",
                    [e.value for e in SocialView]
                )
        
        context_tags = st.text_input("Context Tags (comma-separated)", "startup, tech")
        custom_instructions = st.text_area("Custom Instructions (optional)", "")
        
        submit = st.form_submit_button("➕ Add Agent", type="primary")
        
        if submit:
            responsibilities_list = [r.strip() for r in responsibilities.split('\n') if r.strip()]
            expertise_list = [e.strip() for e in expertise.split('\n') if e.strip()]
            
            role = AgentRole(
                name=role_name,
                domain=domain,
                responsibilities=responsibilities_list,
                required_expertise=expertise_list,
                decision_authority=decision_authority,
                context_specific=False
            )
            
            if add_personality:
                principles_list = [p.strip() for p in principles.split(',') if p.strip()]
                personality = AgentPersonality(
                    communication_style=comm_style,
                    risk_tolerance=risk_tolerance,
                    collaboration_style=collab_style,
                    principles=principles_list
                )
            
            if add_political:
                political_profile = PoliticalProfile(
                    political_spectrum=PoliticalSpectrum(political_spectrum),
                    economic_view=EconomicView(economic_view),
                    social_view=SocialView(social_view)
                )
            
            context_tags_list = [t.strip() for t in context_tags.split(',') if t.strip()]
            
            agent_def = AgentDefinition(
                role=role,
                personality=personality,
                political_profile=political_profile,
                custom_instructions=custom_instructions,
                context_tags=context_tags_list
            )
            
            asyncio.run(st.session_state.orchestrator.add_agent(agent_def))
            st.success(f"Added {role_name}!")
            st.rerun()


def render_agent_suggestions():
    """Render AI-powered agent suggestions."""
    st.subheader("AI-Powered Agent Suggestions")
    
    st.markdown("""
    Describe your project or scenario, and Tachikoma will suggest which agents you need.
    """)
    
    with st.form("suggest_agents_form"):
        context = st.text_area(
            "Describe your project or scenario:",
            placeholder="Example: I want to start a sustainable fintech company in Germany",
            height=100
        )
        
        preferences = st.multiselect(
            "Preferences (optional)",
            ["Diverse perspectives", "Technical focus", "Business focus", "Policy expertise", "Innovation focus"]
        )
        
        submit = st.form_submit_button("💡 Get Suggestions", type="primary")
        
        if submit and context:
            with st.spinner("Analyzing your needs..."):
                user_prefs = {"preferences": preferences}
                suggestions = asyncio.run(
                    st.session_state.orchestrator.suggest_agents_for_context(context, user_prefs)
                )
                
                if suggestions:
                    st.success(f"Found {len(suggestions)} suggested agents!")
                    
                    for idx, suggestion in enumerate(suggestions):
                        with st.expander(f"💡 {suggestion.role.name}", expanded=True):
                            st.markdown(f"**Domain:** {suggestion.role.domain}")
                            st.markdown(f"**Why:** This role would help with {', '.join(suggestion.role.responsibilities[:2])}")
                            
                            if st.button(f"Add {suggestion.role.name}", key=f"add_suggested_{idx}"):
                                asyncio.run(st.session_state.orchestrator.add_agent(suggestion))
                                st.success(f"Added {suggestion.role.name}!")
                                st.rerun()
                else:
                    st.info("No specific suggestions. Try adding agents manually.")


def create_template_agent(template_name: str) -> AgentDefinition:
    """Create an agent from a template."""
    templates = {
        "Legal Consultant": AgentDefinition(
            role=AgentRole(
                name="Legal Consultant",
                domain="Legal",
                responsibilities=["Compliance review", "Risk assessment", "Regulatory guidance"],
                required_expertise=["Corporate law", "Financial regulations", "Contract law"],
                decision_authority="Advisory"
            ),
            personality=AgentPersonality(
                communication_style="Analytical",
                risk_tolerance="Conservative",
                collaboration_style="Collaborative",
                principles=["Rule of law", "Client protection", "Due diligence"]
            ),
            context_tags=["legal", "compliance", "advisory"]
        ),
        
        "Marketing Strategist": AgentDefinition(
            role=AgentRole(
                name="Marketing Strategist",
                domain="Marketing",
                responsibilities=["Brand strategy", "Customer acquisition", "Market analysis"],
                required_expertise=["Digital marketing", "Consumer psychology", "Analytics"],
                decision_authority="Operational"
            ),
            personality=AgentPersonality(
                communication_style="Creative",
                risk_tolerance="Moderate",
                collaboration_style="Collaborative",
                principles=["Customer-first", "Data-driven", "Ethical marketing"]
            ),
            context_tags=["marketing", "strategy", "customer"]
        ),
        
        "Technical Architect": AgentDefinition(
            role=AgentRole(
                name="Technical Architect",
                domain="Technology",
                responsibilities=["System design", "Technology decisions", "Scalability planning"],
                required_expertise=["Software architecture", "Cloud platforms", "Security"],
                decision_authority="Executive"
            ),
            personality=AgentPersonality(
                communication_style="Analytical",
                risk_tolerance="Conservative",
                collaboration_style="Independent",
                principles=["Security first", "Scalable solutions", "Clean code"]
            ),
            context_tags=["technical", "architecture", "systems"]
        ),
        
        "Financial Advisor": AgentDefinition(
            role=AgentRole(
                name="Financial Advisor",
                domain="Finance",
                responsibilities=["Financial planning", "Budget management", "Investment strategy"],
                required_expertise=["Financial analysis", "Investment", "Risk management"],
                decision_authority="Advisory"
            ),
            personality=AgentPersonality(
                communication_style="Analytical",
                risk_tolerance="Moderate",
                collaboration_style="Collaborative",
                principles=["Fiscal responsibility", "Transparency", "Long-term value"]
            ),
            context_tags=["finance", "advisory", "strategy"]
        ),
        
        "Policy Advisor": AgentDefinition(
            role=AgentRole(
                name="Policy Advisor",
                domain="Policy",
                responsibilities=["Policy analysis", "Regulatory strategy", "Stakeholder engagement"],
                required_expertise=["Public policy", "Government relations", "Advocacy"],
                decision_authority="Advisory"
            ),
            personality=AgentPersonality(
                communication_style="Diplomatic",
                risk_tolerance="Conservative",
                collaboration_style="Collaborative",
                principles=["Public interest", "Evidence-based policy", "Stakeholder balance"]
            ),
            context_tags=["policy", "government", "advocacy"]
        )
    }
    
    return templates.get(template_name)
