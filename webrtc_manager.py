import logging
import time
from typing import Dict, Optional, List
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

@dataclass
class Participant:
    id: str
    is_publisher: bool = False
    last_ping: float = field(default_factory=time.time)
    
@dataclass
class Room:
    id: str
    participants: Dict[str, Participant] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)
    
    def is_publisher(self, participant_id: str) -> bool:
        """Check if participant is publisher"""
        return self.participants.get(participant_id, Participant(id=participant_id)).is_publisher
        
    def set_publisher(self, participant_id: str, is_publisher: bool):
        """Set participant publisher status"""
        if participant_id in self.participants:
            self.participants[participant_id].is_publisher = is_publisher

class WebRTCManager:
    def __init__(self):
        self.rooms: Dict[str, Room] = {}
        
    def create_room(self, room_id: str) -> Room:
        """Create a new room"""
        if room_id in self.rooms:
            logger.warning(f"Room {room_id} already exists")
            return self.rooms[room_id]
            
        room = Room(id=room_id)
        self.rooms[room_id] = room
        logger.info(f"Created room {room_id}")
        return room
        
    def get_room(self, room_id: str) -> Optional[Room]:
        """Get room by ID"""
        return self.rooms.get(room_id)
        
    def add_participant(self, room_id: str, participant_id: str, is_publisher: bool = False) -> Participant:
        """Add participant to room"""
        room = self.get_room(room_id)
        if not room:
            room = self.create_room(room_id)
            
        participant = Participant(id=participant_id, is_publisher=is_publisher)
        room.participants[participant_id] = participant
        logger.info(f"Added participant {participant_id} to room {room_id}")
        return participant
        
    def remove_participant(self, room_id: str, participant_id: str):
        """Remove participant from room"""
        room = self.get_room(room_id)
        if room and participant_id in room.participants:
            del room.participants[participant_id]
            logger.info(f"Removed participant {participant_id} from room {room_id}")
            
            # Clean up empty room
            if not room.participants:
                del self.rooms[room_id]
                logger.info(f"Removed empty room {room_id}")
                
    def get_room_participants(self, room_id: str) -> Dict[str, Participant]:
        """Get all participants in a room"""
        room = self.get_room(room_id)
        return room.participants if room else {}
        
    def update_participant_ping(self, room_id: str, participant_id: str):
        """Update participant's last ping time"""
        room = self.get_room(room_id)
        if room and participant_id in room.participants:
            room.participants[participant_id].last_ping = time.time()
            
    def cleanup_inactive_rooms(self, max_inactive_time: int = 300):
        """Remove inactive rooms and participants"""
        current_time = time.time()
        rooms_to_remove = []
        
        for room_id, room in self.rooms.items():
            # Remove inactive participants
            inactive_participants = [
                p_id for p_id, p in room.participants.items()
                if current_time - p.last_ping > max_inactive_time
            ]
            
            for p_id in inactive_participants:
                self.remove_participant(room_id, p_id)
                
            # Mark empty rooms for removal
            if not room.participants:
                rooms_to_remove.append(room_id)
                
        # Remove marked rooms
        for room_id in rooms_to_remove:
            if room_id in self.rooms:
                del self.rooms[room_id]
                logger.info(f"Cleaned up inactive room {room_id}")
                
    def get_stats(self) -> Dict:
        """Get WebRTC manager statistics"""
        total_participants = sum(len(room.participants) for room in self.rooms.values())
        return {
            'total_rooms': len(self.rooms),
            'total_participants': total_participants
        }

# Global WebRTC Manager instance
webrtc_manager = WebRTCManager()
