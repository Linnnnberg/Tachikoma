"""
Chat Interface Component for Tachikoma.

Handles the conversation interface where users interact with multiple agents.
"""

import streamlit as st
import asyncio
from datetime import datetime


def render_chat_interface():
    """Render the main chat interface."""
    st.header("💬 Multi-Agent Conversation")
    
    orchestrator = st.session_state.orchestrator
    agent_llm = st.session_state.agent_llm
    
    if len(orchestrator.agents) == 0:
        st.info("👈 Add agents in the **Agents** tab to start a conversation")
        return
    
    col1, col2 = st.columns([3, 1])
    
    with col2:
        st.subheader("Controls")
        max_turns = st.slider("Max Turns", 2, 10, 4, help="Number of conversation rounds")
        
        if st.button("🔄 Clear History"):
            st.session_state.conversation_history = []
            agent_llm.clear_history()
            st.success("Conversation cleared!")
            st.rerun()
    
    with col1:
        st.subheader("Start New Topic")
        
        with st.form("chat_input_form"):
            user_input = st.text_area(
                "Enter a topic or question for the agents to discuss:",
                placeholder="Example: Should we invest in AI technology for our company?",
                height=100
            )
            
            submit = st.form_submit_button("🚀 Start Conversation", type="primary", use_container_width=True)
            
            if submit and user_input:
                with st.spinner("Agents are discussing..."):
                    result = asyncio.run(run_conversation(user_input, max_turns))
                    
                    if "error" in result:
                        st.error(result["error"])
                    else:
                        st.session_state.conversation_history.append({
                            "timestamp": datetime.now(),
                            "topic": user_input,
                            "turns": result["turns"]
                        })
                        st.success(f"Conversation completed with {len(result['turns'])} turns!")
                        st.rerun()
    
    st.divider()
    
    st.subheader("Conversation History")
    
    if not st.session_state.conversation_history:
        st.info("No conversations yet. Start one above!")
    else:
        for idx, conversation in enumerate(reversed(st.session_state.conversation_history)):
            with st.expander(
                f"📝 {conversation['topic'][:60]}... ({conversation['timestamp'].strftime('%H:%M:%S')})",
                expanded=(idx == 0)
            ):
                st.markdown(f"**Topic:** {conversation['topic']}")
                st.markdown(f"**Time:** {conversation['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
                st.markdown(f"**Turns:** {len(conversation['turns'])}")
                
                st.divider()
                
                for turn in conversation['turns']:
                    agent_id = turn['agent_id']
                    agent_state = st.session_state.orchestrator.agents.get(agent_id)
                    
                    if agent_state:
                        agent_name = agent_state.definition.role.name
                        domain = agent_state.definition.role.domain
                        
                        with st.chat_message("assistant", avatar="🤖"):
                            st.markdown(f"**{agent_name}** ({domain})")
                            st.markdown(turn['response'])
                            
                            if agent_state.definition.personality:
                                st.caption(f"Style: {agent_state.definition.personality.communication_style}")


async def run_conversation(topic: str, max_turns: int = 4):
    """Run a multi-agent conversation."""
    orchestrator = st.session_state.orchestrator
    agent_llm = st.session_state.agent_llm
    
    agents_list = list(orchestrator.agents.items())
    
    if len(agents_list) < 1:
        return {"error": "Need at least 1 agent for conversation"}
    
    results = {
        "topic": topic,
        "turns": []
    }
    
    context = topic
    
    for turn in range(max_turns):
        agent_idx = turn % len(agents_list)
        agent_id, agent_state = agents_list[agent_idx]
        
        try:
            recent_messages = []
            if len(results["turns"]) > 0:
                recent_messages = [
                    {
                        "from_agent": st.session_state.orchestrator.agents[t["agent_id"]].definition.role.name,
                        "content": t["response"]
                    }
                    for t in results["turns"][-3:]
                ]
            
            response = await agent_llm.generate_agent_response(
                agent_state,
                agent_id,
                context,
                recent_messages
            )
            
            results["turns"].append({
                "agent_id": agent_id,
                "turn": turn + 1,
                "response": response
            })
            
            context = f"{context}\n\n{agent_state.definition.role.name}: {response}"
            
        except Exception as e:
            return {"error": f"Error generating response: {str(e)}"}
    
    return results


def render_conversation_stats():
    """Render conversation statistics."""
    if not st.session_state.conversation_history:
        return
    
    st.subheader("📊 Conversation Stats")
    
    total_conversations = len(st.session_state.conversation_history)
    total_turns = sum(len(conv['turns']) for conv in st.session_state.conversation_history)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Conversations", total_conversations)
    
    with col2:
        st.metric("Total Turns", total_turns)
    
    with col3:
        avg_turns = total_turns / total_conversations if total_conversations > 0 else 0
        st.metric("Avg Turns/Conversation", f"{avg_turns:.1f}")
