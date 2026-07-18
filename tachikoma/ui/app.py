"""
Tachikoma Streamlit UI - Main Application.

This is the main entry point for the Tachikoma Streamlit web interface.
"""

import streamlit as st
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from tachikoma.core.orchestrator import TachikomaOrchestrator
from tachikoma.core.llm import LLMProviderFactory, EnhancedAgentLLM
from tachikoma.config.settings import load_settings
from tachikoma.ui.components import chat, agents, visualization


def init_session_state():
    """Initialize Streamlit session state."""
    if 'orchestrator' not in st.session_state:
        settings = load_settings()
        st.session_state.orchestrator = TachikomaOrchestrator(settings)
    
    if 'llm_provider' not in st.session_state:
        st.session_state.llm_provider = LLMProviderFactory.create_mock_provider()
    
    if 'agent_llm' not in st.session_state:
        st.session_state.agent_llm = EnhancedAgentLLM(st.session_state.llm_provider)
    
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    
    if 'current_task' not in st.session_state:
        st.session_state.current_task = ""


def main():
    """Main Streamlit application."""
    st.set_page_config(
        page_title="Tachikoma Multi-Agent System",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    init_session_state()
    
    st.title("🤖 Tachikoma Multi-Agent AI System")
    st.markdown("*Dynamic, character-driven agents that collaborate while maintaining their principles*")
    
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        st.subheader("LLM Provider")
        provider_type = st.selectbox(
            "Select Provider",
            ["Mock (Testing)", "Hugging Face", "OpenAI"],
            help="Choose the LLM provider for agent responses"
        )
        
        if provider_type == "Hugging Face":
            model_name = st.selectbox(
                "Model",
                ["microsoft/DialoGPT-small", "microsoft/DialoGPT-medium", "microsoft/DialoGPT-large"],
                help="Choose Hugging Face model size"
            )
            if st.button("Load Hugging Face Model"):
                with st.spinner("Loading model..."):
                    try:
                        st.session_state.llm_provider = LLMProviderFactory.create_huggingface_provider(model_name)
                        st.session_state.agent_llm = EnhancedAgentLLM(st.session_state.llm_provider)
                        st.success(f"Loaded {model_name}")
                    except Exception as e:
                        st.error(f"Error loading model: {str(e)}")
        
        elif provider_type == "OpenAI":
            api_key = st.text_input("API Key", type="password", help="Enter your OpenAI API key")
            model_name = st.selectbox("Model", ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"])
            if st.button("Configure OpenAI") and api_key:
                try:
                    st.session_state.llm_provider = LLMProviderFactory.create_openai_provider(api_key, model_name)
                    st.session_state.agent_llm = EnhancedAgentLLM(st.session_state.llm_provider)
                    st.success(f"Configured {model_name}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        
        st.divider()
        
        st.subheader("📊 System Status")
        orchestrator = st.session_state.orchestrator
        st.metric("Active Agents", len(orchestrator.agents))
        st.metric("Conversations", len(st.session_state.conversation_history))
        
        if st.button("🔄 Reset System", type="secondary"):
            st.session_state.orchestrator = TachikomaOrchestrator(load_settings())
            st.session_state.conversation_history = []
            st.session_state.agent_llm.clear_history()
            st.success("System reset!")
            st.rerun()
    
    tabs = st.tabs(["💬 Chat", "👥 Agents", "📈 Visualization"])
    
    with tabs[0]:
        chat.render_chat_interface()
    
    with tabs[1]:
        agents.render_agent_management()
    
    with tabs[2]:
        visualization.render_visualizations()
    
    with st.expander("ℹ️ About Tachikoma"):
        st.markdown("""
        **Tachikoma** is an advanced multi-agent AI system featuring:
        
        - **Dynamic Agent Management**: Create agents with distinct roles, personalities, and political views
        - **Multi-Dimensional Architecture**: Agents with functional roles, personalities, and ideological positions
        - **Collaborative Competition**: Agents debate and collaborate while maintaining their principles
        - **Real-time Conversations**: Watch agents discuss and reach consensus on complex topics
        - **Performance Tracking**: Monitor agent contributions and resource allocation
        
        **How to use:**
        1. Go to the **Agents** tab to create your team
        2. Switch to the **Chat** tab to start a conversation
        3. View analytics in the **Visualization** tab
        """)


if __name__ == "__main__":
    main()
