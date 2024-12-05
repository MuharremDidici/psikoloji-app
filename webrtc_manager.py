import asyncio
import logging
import uuid
from typing import Dict, Optional, Set
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from datetime import datetime
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)

@dataclass_json
@dataclass
class Room:
    room_id: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    max_participants: int = 2
    participants: Dict[str, 'Participant'] = field(default_factory=dict)
    active: bool = True

@dataclass
class Participant:
    id: str
    room_id: str
    last_ping: datetime = field(default_factory=datetime.utcnow)
    is_publisher: bool = False
    
class WebRTCManager:
    def __init__(self):
        self.rooms: Dict[str, Room] = {}
        self._cleanup_task = None
        self.start_cleanup_task()

    def start_cleanup_task(self):
        if self._cleanup_task is None:
            self._cleanup_task = asyncio.create_task(self._periodic_cleanup())

    async def _periodic_cleanup(self):
        while True:
            try:
                await self._cleanup_inactive_rooms()
                await asyncio.sleep(60)
            except Exception as e:
                logger.error(f"Cleanup error: {e}")

    async def _cleanup_inactive_rooms(self):
        now = datetime.utcnow()
        inactive_rooms = []
        
        for room_id, room in self.rooms.items():
            if not room.active or not room.participants:
                inactive_rooms.append(room_id)
                continue
                
            inactive_participants = []
            for participant_id, participant in room.participants.items():
                if (now - participant.last_ping).total_seconds() > 30:
                    inactive_participants.append(participant_id)
                    
            for participant_id in inactive_participants:
                await self.remove_participant(room_id, participant_id)
                
        for room_id in inactive_rooms:
            await self.close_room(room_id)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def create_room(self, room_id: Optional[str] = None) -> Room:
        room_id = room_id or str(uuid.uuid4())
        if room_id in self.rooms:
            raise ValueError("Room already exists")
            
        room = Room(room_id=room_id)
        self.rooms[room_id] = room
        logger.info(f"Created room: {room_id}")
        return room

    async def get_room(self, room_id: str) -> Optional[Room]:
        return self.rooms.get(room_id)

    async def add_participant(self, room_id: str, participant_id: str, is_publisher: bool = False) -> Participant:
        room = await self.get_room(room_id)
        if not room:
            raise ValueError("Room not found")
            
        if len(room.participants) >= room.max_participants:
            raise ValueError("Room is full")
            
        if participant_id in room.participants:
            raise ValueError("Participant already in room")
            
        participant = Participant(
            id=participant_id,
            room_id=room_id,
            is_publisher=is_publisher
        )
        
        room.participants[participant_id] = participant
        logger.info(f"Added participant {participant_id} to room {room_id}")
        return participant

    async def remove_participant(self, room_id: str, participant_id: str):
        room = await self.get_room(room_id)
        if not room:
            return
            
        if participant_id in room.participants:
            del room.participants[participant_id]
            logger.info(f"Removed participant {participant_id} from room {room_id}")
        
        if not room.participants:
            await self.close_room(room_id)

    async def close_room(self, room_id: str):
        room = self.rooms.pop(room_id, None)
        if room:
            room.active = False
            logger.info(f"Closed room: {room_id}")

    async def update_participant_ping(self, room_id: str, participant_id: str):
        room = await self.get_room(room_id)
        if room and participant_id in room.participants:
            room.participants[participant_id].last_ping = datetime.utcnow()

    async def get_room_participants(self, room_id: str) -> Dict[str, Participant]:
        room = await self.get_room(room_id)
        return room.participants if room else {}

    async def get_publisher(self, room_id: str) -> Optional[Participant]:
        room = await self.get_room(room_id)
        if room:
            for participant in room.participants.values():
                if participant.is_publisher:
                    return participant
        return None

# Global WebRTC Manager instance
webrtc_manager = WebRTCManager()
