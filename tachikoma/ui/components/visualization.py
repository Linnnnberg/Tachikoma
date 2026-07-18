"""
Visualization Component for Tachikoma.

Handles charts, graphs, and visual analytics for the multi-agent system.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from collections import Counter


def render_visualizations():
    """Render the visualization dashboard."""
    st.header("📈 System Visualizations")
    
    orchestrator = st.session_state.orchestrator
    
    if len(orchestrator.agents) == 0:
        st.info("Add agents to see visualizations")
        return
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎯 Agent Overview", 
        "🌐 Agent Network", 
        "📊 Performance", 
        "🏛️ Diversity Analysis"
    ])
    
    with tab1:
        render_agent_overview()
    
    with tab2:
        render_agent_network()
    
    with tab3:
        render_performance_metrics()
    
    with tab4:
        render_diversity_analysis()


def render_agent_overview():
    """Render overview statistics and metrics."""
    st.subheader("Agent Overview")
    
    orchestrator = st.session_state.orchestrator
    agents = orchestrator.agents
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Agents", len(agents))
    
    with col2:
        avg_performance = sum(a.performance_score for a in agents.values()) / len(agents)
        st.metric("Avg Performance", f"{avg_performance:.2f}")
    
    with col3:
        avg_energy = sum(a.energy_level for a in agents.values()) / len(agents)
        st.metric("Avg Energy", f"{avg_energy:.1%}")
    
    with col4:
        domains = set(a.definition.role.domain for a in agents.values())
        st.metric("Unique Domains", len(domains))
    
    st.divider()
    
    domain_counts = Counter(a.definition.role.domain for a in agents.values())
    
    fig = go.Figure(data=[
        go.Bar(
            x=list(domain_counts.keys()),
            y=list(domain_counts.values()),
            marker_color='lightblue'
        )
    ])
    
    fig.update_layout(
        title="Agents by Domain",
        xaxis_title="Domain",
        yaxis_title="Count",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_agent_network():
    """Render agent relationship network."""
    st.subheader("Agent Relationship Network")
    
    orchestrator = st.session_state.orchestrator
    agents = orchestrator.agents
    
    if len(agents) < 2:
        st.info("Add more agents to see the network")
        return
    
    try:
        import networkx as nx
        
        G = nx.Graph()
        
        for agent_id, agent_state in agents.items():
            role_name = agent_state.definition.role.name
            domain = agent_state.definition.role.domain
            G.add_node(agent_id, label=role_name, domain=domain)
        
        agent_ids = list(agents.keys())
        for i, agent_id_1 in enumerate(agent_ids):
            for agent_id_2 in agent_ids[i+1:]:
                domain_1 = agents[agent_id_1].definition.role.domain
                domain_2 = agents[agent_id_2].definition.role.domain
                
                if domain_1 != domain_2:
                    G.add_edge(agent_id_1, agent_id_2, weight=0.5)
                else:
                    G.add_edge(agent_id_1, agent_id_2, weight=0.2)
        
        pos = nx.spring_layout(G, k=1, iterations=50)
        
        edge_trace = []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_trace.append(
                go.Scatter(
                    x=[x0, x1, None],
                    y=[y0, y1, None],
                    mode='lines',
                    line=dict(width=1, color='lightgray'),
                    hoverinfo='none',
                    showlegend=False
                )
            )
        
        node_trace = go.Scatter(
            x=[pos[node][0] for node in G.nodes()],
            y=[pos[node][1] for node in G.nodes()],
            mode='markers+text',
            hoverinfo='text',
            marker=dict(
                size=20,
                color=[agents[node].performance_score for node in G.nodes()],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Performance"),
                line=dict(width=2, color='white')
            ),
            text=[G.nodes[node]['label'] for node in G.nodes()],
            textposition="top center",
            hovertext=[
                f"{G.nodes[node]['label']}<br>"
                f"Domain: {G.nodes[node]['domain']}<br>"
                f"Performance: {agents[node].performance_score:.2f}"
                for node in G.nodes()
            ]
        )
        
        fig = go.Figure(data=edge_trace + [node_trace])
        
        fig.update_layout(
            title="Agent Collaboration Network",
            showlegend=False,
            hovermode='closest',
            margin=dict(b=0, l=0, r=0, t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.info("Node size reflects agent connections. Color indicates performance score.")
    
    except ImportError:
        st.warning("NetworkX not installed. Run: pip install networkx")
        
        st.markdown("**Agent Connections:**")
        for agent_id, agent_state in agents.items():
            st.markdown(f"- {agent_state.definition.role.name} ({agent_state.definition.role.domain})")


def render_performance_metrics():
    """Render performance analytics."""
    st.subheader("Performance Metrics")
    
    orchestrator = st.session_state.orchestrator
    agents = orchestrator.agents
    
    agent_names = [a.definition.role.name for a in agents.values()]
    performance_scores = [a.performance_score for a in agents.values()]
    energy_levels = [a.energy_level for a in agents.values()]
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_perf = go.Figure(data=[
            go.Bar(
                x=agent_names,
                y=performance_scores,
                marker_color='lightblue',
                text=[f"{score:.2f}" for score in performance_scores],
                textposition='auto',
            )
        ])
        
        fig_perf.update_layout(
            title="Agent Performance Scores",
            xaxis_title="Agent",
            yaxis_title="Score",
            height=400
        )
        
        st.plotly_chart(fig_perf, use_container_width=True)
    
    with col2:
        fig_energy = go.Figure(data=[
            go.Bar(
                x=agent_names,
                y=energy_levels,
                marker_color='lightgreen',
                text=[f"{energy:.0%}" for energy in energy_levels],
                textposition='auto',
            )
        ])
        
        fig_energy.update_layout(
            title="Agent Energy Levels",
            xaxis_title="Agent",
            yaxis_title="Energy",
            yaxis_tickformat='.0%',
            height=400
        )
        
        st.plotly_chart(fig_energy, use_container_width=True)
    
    fig_combined = go.Figure()
    
    fig_combined.add_trace(go.Scatterpolar(
        r=performance_scores + [performance_scores[0]],
        theta=agent_names + [agent_names[0]],
        fill='toself',
        name='Performance'
    ))
    
    fig_combined.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, max(performance_scores + [1])])
        ),
        title="Agent Performance Radar",
        height=500
    )
    
    st.plotly_chart(fig_combined, use_container_width=True)


def render_diversity_analysis():
    """Render diversity and balance analysis."""
    st.subheader("Diversity Analysis")
    
    orchestrator = st.session_state.orchestrator
    diversity = orchestrator.get_agent_diversity_analysis()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Role Diversity", len(diversity['role_diversity']))
        st.metric("Domain Coverage", len(diversity['domain_coverage']))
    
    with col2:
        st.metric("Personality Diversity", len(diversity['personality_diversity']))
        st.metric("Political Diversity", len(diversity['political_diversity']))
    
    st.divider()
    
    if diversity['domain_coverage']:
        st.markdown("**Domains Covered:**")
        for domain in diversity['domain_coverage']:
            st.markdown(f"- {domain}")
    
    if diversity['role_diversity']:
        st.markdown("**Unique Roles:**")
        for role in diversity['role_diversity']:
            st.markdown(f"- {role}")
    
    if diversity['political_diversity']:
        st.divider()
        st.markdown("**Political Spectrum Distribution:**")
        
        political_counts = Counter()
        for agent_state in orchestrator.agents.values():
            if agent_state.definition.political_profile and agent_state.definition.political_profile.political_spectrum:
                spectrum = agent_state.definition.political_profile.political_spectrum.value
                political_counts[spectrum] += 1
        
        if political_counts:
            fig = go.Figure(data=[
                go.Pie(
                    labels=list(political_counts.keys()),
                    values=list(political_counts.values()),
                    hole=0.3
                )
            ])
            
            fig.update_layout(
                title="Political Spectrum Balance",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    personalities = []
    for agent_state in orchestrator.agents.values():
        if agent_state.definition.personality:
            personalities.append(agent_state.definition.personality.communication_style)
    
    if personalities:
        st.markdown("**Communication Styles:**")
        style_counts = Counter(personalities)
        
        fig = go.Figure(data=[
            go.Bar(
                x=list(style_counts.keys()),
                y=list(style_counts.values()),
                marker_color='lightcoral'
            )
        ])
        
        fig.update_layout(
            title="Communication Style Distribution",
            xaxis_title="Style",
            yaxis_title="Count",
            height=350
        )
        
        st.plotly_chart(fig, use_container_width=True)
