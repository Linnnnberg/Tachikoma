"""
Simplified communication system for Phase 1.

This module contains a simplified communication system focused on
essential message passing and basic debate functionality.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class MessageType(Enum):
    """Simplified message types."""
    REQUEST = "request"
    RESPONSE = "response"
    DEBATE = "debate"
    GENERAL = "general"


@dataclass
class SimpleMessage:
    """Simplified message for Phase 1."""
    
    id: str
    from_agent: str
    to_agent: str
    content: str
    message_type: MessageType
    timestamp: datetime
    read: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary."""
        return {
            "id": self.id,
            "from_agent": self.from_agent,
            "to_agent": self.to_agent,
            "content": self.content,
            "message_type": self.message_type.value,
            "timestamp": self.timestamp.isoformat(),
            "read": self.read
        }


@dataclass
class SimpleDebate:
    """Simplified debate for Phase 1."""
    
    id: str
    topic: str
    participants: List[str]
    messages: List[SimpleMessage]
    votes: Dict[str, str]  # agent_name -> position
    start_time: datetime
    consensus_reached: bool = False
    consensus_decision: Optional[str] = None
    
    def add_message(self, message: SimpleMessage):
        """Add a message to the debate."""
        message.message_type = MessageType.DEBATE
        self.messages.append(message)
    
    def cast_vote(self, agent_name: str, position: str) -> bool:
        """Cast a vote in the debate."""
        if agent_name in self.participants:
            self.votes[agent_name] = position
            return True
        return False
    
    def check_consensus(self) -> bool:
        """Check if consensus has been reached."""
        if len(self.votes) < len(self.participants):
            return False
        
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
                return True
        
        return False
    
    def get_summary(self) -> Dict[str, Any]:
        """Get debate summary."""
        return {
            "id": self.id,
            "topic": self.topic,
            "participants": self.participants,
            "message_count": len(self.messages),
            "votes": self.votes,
            "consensus_reached": self.consensus_reached,
            "consensus_decision": self.consensus_decision,
            "start_time": self.start_time.isoformat()
        }


class SimpleCommunication:
    """Simplified communication system for Phase 1."""
    
    def __init__(self):
        """Initialize the simple communication system."""
        self.messages: List[SimpleMessage] = []
        self.agent_messages: Dict[str, List[SimpleMessage]] = {}
        self.active_debates: Dict[str, SimpleDebate] = {}
        self.message_counter = 0
    
    def _generate_message_id(self) -> str:
        """Generate a unique message ID."""
        self.message_counter += 1
        return f"msg_{self.message_counter}"
    
    def _generate_debate_id(self) -> str:
        """Generate a unique debate ID."""
        return f"debate_{len(self.active_debates) + 1}"
    
    def send_message(self, from_agent: str, to_agent: str, content: str, 
                    message_type: MessageType = MessageType.GENERAL) -> str:
        """Send a message between agents."""
        message_id = self._generate_message_id()
        message = SimpleMessage(
            id=message_id,
            from_agent=from_agent,
            to_agent=to_agent,
            content=content,
            message_type=message_type,
            timestamp=datetime.now()
        )
        
        # Add to global messages
        self.messages.append(message)
        
        # Add to agent-specific messages
        if from_agent not in self.agent_messages:
            self.agent_messages[from_agent] = []
        if to_agent not in self.agent_messages:
            self.agent_messages[to_agent] = []
        
        self.agent_messages[from_agent].append(message)
        self.agent_messages[to_agent].append(message)
        
        return message_id
    
    def get_messages(self, agent_name: str, unread_only: bool = False) -> List[SimpleMessage]:
        """Get messages for an agent."""
        messages = self.agent_messages.get(agent_name, [])
        
        if unread_only:
            messages = [msg for msg in messages if not msg.read]
        
        # Sort by timestamp (newest first)
        messages.sort(key=lambda x: x.timestamp, reverse=True)
        return messages
    
    def mark_message_read(self, message_id: str, agent_name: str) -> bool:
        """Mark a message as read."""
        for message in self.agent_messages.get(agent_name, []):
            if message.id == message_id:
                message.read = True
                return True
        return False
    
    def start_debate(self, topic: str, participants: List[str], initiator: str) -> str:
        """Start a debate on a topic."""
        debate_id = self._generate_debate_id()
        debate = SimpleDebate(
            id=debate_id,
            topic=topic,
            participants=participants,
            messages=[],
            votes={},
            start_time=datetime.now()
        )
        
        self.active_debates[debate_id] = debate
        
        # Send initial message to all participants
        self.send_message(
            from_agent=initiator,
            to_agent="",  # Broadcast
            content=f"Debate started: {topic}",
            message_type=MessageType.DEBATE
        )
        
        return debate_id
    
    def add_debate_message(self, debate_id: str, from_agent: str, content: str) -> bool:
        """Add a message to an active debate."""
        if debate_id not in self.active_debates:
            return False
        
        debate = self.active_debates[debate_id]
        if from_agent not in debate.participants:
            return False
        
        message_id = self._generate_message_id()
        message = SimpleMessage(
            id=message_id,
            from_agent=from_agent,
            to_agent="",  # Broadcast to all participants
            content=content,
            message_type=MessageType.DEBATE,
            timestamp=datetime.now()
        )
        
        debate.add_message(message)
        
        # Also add to agent messages
        for participant in debate.participants:
            if participant not in self.agent_messages:
                self.agent_messages[participant] = []
            self.agent_messages[participant].append(message)
        
        return True
    
    def cast_vote(self, debate_id: str, agent_name: str, position: str) -> bool:
        """Cast a vote in a debate."""
        if debate_id not in self.active_debates:
            return False
        
        debate = self.active_debates[debate_id]
        success = debate.cast_vote(agent_name, position)
        
        if success:
            # Check for consensus
            consensus_reached = debate.check_consensus()
            if consensus_reached:
                # Notify all participants
                self.send_message(
                    from_agent="system",
                    to_agent="",
                    content=f"Consensus reached: {debate.consensus_decision}",
                    message_type=MessageType.DEBATE
                )
        
        return success
    
    def get_debate(self, debate_id: str) -> Optional[SimpleDebate]:
        """Get a debate by ID."""
        return self.active_debates.get(debate_id)
    
    def get_active_debates(self) -> List[SimpleDebate]:
        """Get all active debates."""
        return list(self.active_debates.values())
    
    def get_agent_stats(self, agent_name: str) -> Dict[str, Any]:
        """Get communication statistics for an agent."""
        messages = self.agent_messages.get(agent_name, [])
        
        # Count messages by type
        type_counts = {}
        for message in messages:
            msg_type = message.message_type.value
            type_counts[msg_type] = type_counts.get(msg_type, 0) + 1
        
        # Count unread messages
        unread_count = sum(1 for msg in messages if not msg.read)
        
        return {
            "total_messages": len(messages),
            "unread_messages": unread_count,
            "messages_by_type": type_counts,
            "last_activity": max((msg.timestamp for msg in messages), default=None)
        }
