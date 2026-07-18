"""
Enhanced communication system for Tachikoma.

This module handles inter-agent communication, message passing,
debate protocols, and consensus building in the multi-agent system.
"""

from typing import Dict, List, Optional, Any, Tuple
import asyncio
import uuid
from datetime import datetime, timedelta
from enum import Enum
from .agent import AgentState, AgentDefinition, AgentRole, AgentPersonality, PoliticalProfile


class MessageType(Enum):
    """Types of messages in the system."""
    REQUEST = "request"
    RESPONSE = "response"
    PROPOSAL = "proposal"
    DEBATE = "debate"
    CONSENSUS = "consensus"
    BROADCAST = "broadcast"
    PRIVATE = "private"
    URGENT = "urgent"


class MessagePriority(Enum):
    """Message priority levels."""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    URGENT = 4
    CRITICAL = 5


class Message:
    """Represents a message in the system."""
    
    def __init__(
        self,
        message_id: str,
        from_agent: str,
        to_agent: str,
        content: str,
        message_type: MessageType,
        priority: MessagePriority = MessagePriority.NORMAL,
        context: Dict[str, Any] = None,
        timestamp: datetime = None,
        response_to: str = None
    ):
        self.message_id = message_id
        self.from_agent = from_agent
        self.to_agent = to_agent
        self.content = content
        self.message_type = message_type
        self.priority = priority
        self.context = context or {}
        self.timestamp = timestamp or datetime.now()
        self.delivered = False
        self.read = False
        self.response_to = response_to
        self.thread_id = None
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary."""
        return {
            "message_id": self.message_id,
            "from_agent": self.from_agent,
            "to_agent": self.to_agent,
            "content": self.content,
            "message_type": self.message_type.value,
            "priority": self.priority.value,
            "context": self.context,
            "timestamp": self.timestamp.isoformat(),
            "delivered": self.delivered,
            "read": self.read,
            "response_to": self.response_to,
            "thread_id": self.thread_id
        }


class DebateSession:
    """Represents a debate session between agents."""
    
    def __init__(self, session_id: str, topic: str, participants: List[str]):
        self.session_id = session_id
        self.topic = topic
        self.participants = participants
        self.messages: List[Message] = []
        self.start_time = datetime.now()
        self.end_time = None
        self.consensus_reached = False
        self.consensus_decision = None
        self.votes: Dict[str, str] = {}  # agent_id -> position
        
    def add_message(self, message: Message):
        """Add a message to the debate session."""
        message.thread_id = self.session_id
        self.messages.append(message)
        
    def cast_vote(self, agent_id: str, position: str):
        """Cast a vote in the debate."""
        if agent_id in self.participants:
            self.votes[agent_id] = position
            
    def check_consensus(self) -> Tuple[bool, Optional[str]]:
        """Check if consensus has been reached."""
        if len(self.votes) < len(self.participants):
            return False, None
            
        # Count votes
        vote_counts = {}
        for position in self.votes.values():
            vote_counts[position] = vote_counts.get(position, 0) + 1
            
        # Check for majority
        total_votes = len(self.votes)
        for position, count in vote_counts.items():
            if count > total_votes / 2:
                self.consensus_reached = True
                self.consensus_decision = position
                self.end_time = datetime.now()
                return True, position
                
        return False, None


class MessagePassing:
    """Enhanced message passing system with debate and consensus capabilities."""

    def __init__(self):
        """Initialize the message passing system."""
        self.message_queue: List[Message] = []
        self.message_history: Dict[str, List[Message]] = {}
        self.active_debates: Dict[str, DebateSession] = {}
        self.agent_subscriptions: Dict[str, List[str]] = {}  # agent_id -> topics
        self.message_handlers: Dict[MessageType, callable] = {}
        
    def _generate_message_id(self) -> str:
        """Generate a unique message ID."""
        return str(uuid.uuid4())
        
    def _get_or_create_history(self, agent_id: str) -> List[Message]:
        """Get or create message history for an agent."""
        if agent_id not in self.message_history:
            self.message_history[agent_id] = []
        return self.message_history[agent_id]

    async def send_message(
        self, 
        from_agent: str, 
        to_agent: str, 
        content: str,
        message_type: MessageType = MessageType.PRIVATE,
        priority: MessagePriority = MessagePriority.NORMAL,
        context: Dict[str, Any] = None,
        response_to: str = None
    ) -> str:
        """Send a message from one agent to another."""
        message_id = self._generate_message_id()
        message = Message(
            message_id=message_id,
            from_agent=from_agent,
            to_agent=to_agent,
            content=content,
            message_type=message_type,
            priority=priority,
            context=context or {},
            response_to=response_to
        )
        
        # Add to queue
        self.message_queue.append(message)
        
        # Add to recipient's history
        recipient_history = self._get_or_create_history(to_agent)
        recipient_history.append(message)
        
        # Add to sender's history
        sender_history = self._get_or_create_history(from_agent)
        sender_history.append(message)
        
        # Mark as delivered
        message.delivered = True
        
        return message_id

    async def broadcast_message(
        self, 
        from_agent: str, 
        content: str,
        message_type: MessageType = MessageType.BROADCAST,
        priority: MessagePriority = MessagePriority.NORMAL,
        context: Dict[str, Any] = None,
        target_agents: List[str] = None
    ) -> List[str]:
        """Broadcast a message to multiple agents."""
        message_ids = []
        
        if target_agents:
            for agent_id in target_agents:
                msg_id = await self.send_message(
                    from_agent, agent_id, content, message_type, priority, context
                )
                message_ids.append(msg_id)
        else:
            # Broadcast to all agents with history
            for agent_id in self.message_history.keys():
                if agent_id != from_agent:
                    msg_id = await self.send_message(
                        from_agent, agent_id, content, message_type, priority, context
                    )
                    message_ids.append(msg_id)
                    
        return message_ids

    async def start_debate(
        self, 
        topic: str, 
        participants: List[str],
        initiator: str
    ) -> str:
        """Start a debate session on a topic."""
        session_id = str(uuid.uuid4())
        debate = DebateSession(session_id, topic, participants)
        self.active_debates[session_id] = debate
        
        # Notify all participants
        await self.broadcast_message(
            from_agent=initiator,
            content=f"Debate started on topic: {topic}",
            message_type=MessageType.DEBATE,
            priority=MessagePriority.HIGH,
            target_agents=participants
        )
        
        return session_id

    async def add_debate_message(
        self, 
        session_id: str, 
        from_agent: str, 
        content: str,
        position: str = None
    ) -> str:
        """Add a message to an active debate."""
        if session_id not in self.active_debates:
            raise ValueError(f"Debate session {session_id} not found")
            
        debate = self.active_debates[session_id]
        
        if from_agent not in debate.participants:
            raise ValueError(f"Agent {from_agent} not in debate participants")
            
        # Create message
        message_id = self._generate_message_id()
        message = Message(
            message_id=message_id,
            from_agent=from_agent,
            to_agent="",  # Broadcast to all participants
            content=content,
            message_type=MessageType.DEBATE,
            priority=MessagePriority.HIGH,
            context={"position": position} if position else {}
        )
        
        # Add to debate
        debate.add_message(message)
        
        # Broadcast to all participants
        await self.broadcast_message(
            from_agent=from_agent,
            content=f"[{position}] {content}" if position else content,
            message_type=MessageType.DEBATE,
            priority=MessagePriority.HIGH,
            target_agents=debate.participants
        )
        
        return message_id

    async def cast_vote(
        self, 
        session_id: str, 
        agent_id: str, 
        position: str
    ) -> bool:
        """Cast a vote in a debate session."""
        if session_id not in self.active_debates:
            return False
            
        debate = self.active_debates[session_id]
        debate.cast_vote(agent_id, position)
        
        # Check for consensus
        consensus_reached, decision = debate.check_consensus()
        
        if consensus_reached:
            # Notify all participants
            await self.broadcast_message(
                from_agent="system",
                content=f"Consensus reached: {decision}",
                message_type=MessageType.CONSENSUS,
                priority=MessagePriority.HIGH,
                target_agents=debate.participants
            )
            
        return consensus_reached

    async def get_messages(
        self, 
        agent_id: str, 
        message_type: MessageType = None,
        unread_only: bool = False,
        limit: int = 100
    ) -> List[Message]:
        """Get messages for an agent."""
        history = self._get_or_create_history(agent_id)
        
        # Filter messages
        filtered_messages = []
        for message in history:
            if message_type and message.message_type != message_type:
                continue
            if unread_only and message.read:
                continue
            filtered_messages.append(message)
            
        # Sort by timestamp (newest first)
        filtered_messages.sort(key=lambda x: x.timestamp, reverse=True)
        
        return filtered_messages[:limit]

    async def mark_message_read(self, message_id: str, agent_id: str) -> bool:
        """Mark a message as read."""
        history = self._get_or_create_history(agent_id)
        
        for message in history:
            if message.message_id == message_id:
                message.read = True
        return True
                
        return False

    async def get_debate_summary(self, session_id: str) -> Dict[str, Any]:
        """Get a summary of a debate session."""
        if session_id not in self.active_debates:
            return {}
            
        debate = self.active_debates[session_id]
        
        return {
            "session_id": session_id,
            "topic": debate.topic,
            "participants": debate.participants,
            "message_count": len(debate.messages),
            "start_time": debate.start_time.isoformat(),
            "end_time": debate.end_time.isoformat() if debate.end_time else None,
            "consensus_reached": debate.consensus_reached,
            "consensus_decision": debate.consensus_decision,
            "votes": debate.votes
        }

    async def get_agent_communication_stats(self, agent_id: str) -> Dict[str, Any]:
        """Get communication statistics for an agent."""
        history = self._get_or_create_history(agent_id)
        
        # Count messages by type
        type_counts = {}
        for message in history:
            msg_type = message.message_type.value
            type_counts[msg_type] = type_counts.get(msg_type, 0) + 1
            
        # Count unread messages
        unread_count = sum(1 for msg in history if not msg.read)
        
        return {
            "total_messages": len(history),
            "unread_messages": unread_count,
            "messages_by_type": type_counts,
            "last_activity": max((msg.timestamp for msg in history), default=None)
        }


class DebateProtocol:
    """Enhanced debate and negotiation protocols between agents."""

    def __init__(self, message_passing: MessagePassing):
        """Initialize the debate protocol."""
        self.message_passing = message_passing
        self.negotiation_strategies = {
            "collaborative": self._collaborative_strategy,
            "competitive": self._competitive_strategy,
            "accommodating": self._accommodating_strategy,
            "compromising": self._compromising_strategy
        }
        
    async def _collaborative_strategy(self, agent_id: str, topic: str, context: Dict[str, Any]) -> str:
        """Collaborative negotiation strategy."""
        return f"I'm open to finding a solution that benefits everyone. Let's work together on {topic}."
        
    async def _competitive_strategy(self, agent_id: str, topic: str, context: Dict[str, Any]) -> str:
        """Competitive negotiation strategy."""
        return f"I have strong views on {topic} and will advocate for my position."
        
    async def _accommodating_strategy(self, agent_id: str, topic: str, context: Dict[str, Any]) -> str:
        """Accommodating negotiation strategy."""
        return f"I'm willing to be flexible on {topic} to reach an agreement."
        
    async def _compromising_strategy(self, agent_id: str, topic: str, context: Dict[str, Any]) -> str:
        """Compromising negotiation strategy."""
        return f"I'm ready to find a middle ground on {topic}."

    async def initiate_debate(
        self, 
        agents: List[str], 
        topic: str,
        initiator: str,
        strategy: str = "collaborative"
    ) -> Dict[str, Any]:
        """Initiate a debate between agents on a topic."""
        # Start debate session
        session_id = await self.message_passing.start_debate(topic, agents, initiator)
        
        # Get initial positions from each agent
        initial_positions = {}
        for agent_id in agents:
            if strategy in self.negotiation_strategies:
                position = await self.negotiation_strategies[strategy](agent_id, topic, {})
                initial_positions[agent_id] = position
                
                # Add to debate
                await self.message_passing.add_debate_message(
                    session_id, agent_id, position, f"Initial Position"
                )
        
        return {
            "session_id": session_id,
            "topic": topic,
            "participants": agents,
            "initial_positions": initial_positions,
            "strategy": strategy
        }

    async def facilitate_negotiation(
        self, 
        session_id: str, 
        agent_id: str, 
        message: str,
        position: str = None
    ) -> Dict[str, Any]:
        """Facilitate negotiation by adding a message to the debate."""
        # Add message to debate
        message_id = await self.message_passing.add_debate_message(
            session_id, agent_id, message, position
        )
        
        # Get updated debate summary
        summary = await self.message_passing.get_debate_summary(session_id)
        
        return {
            "message_id": message_id,
            "debate_summary": summary
        }

    async def conclude_debate(
        self, 
        session_id: str, 
        final_decision: str = None
    ) -> Dict[str, Any]:
        """Conclude a debate session."""
        if session_id not in self.message_passing.active_debates:
            return {"error": "Debate session not found"}
            
        debate = self.message_passing.active_debates[session_id]
        
        if final_decision:
            debate.consensus_decision = final_decision
            debate.consensus_reached = True
            debate.end_time = datetime.now()
            
            # Notify participants
            await self.message_passing.broadcast_message(
                from_agent="system",
                content=f"Debate concluded with decision: {final_decision}",
                message_type=MessageType.CONSENSUS,
                priority=MessagePriority.HIGH,
                target_agents=debate.participants
            )
        
        return await self.message_passing.get_debate_summary(session_id)