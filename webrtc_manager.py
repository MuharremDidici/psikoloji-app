import asyncio
import logging
import uuid
from typing import Dict, Optional, Set
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from datetime import datetime
from aiortc import RTCPeerConnection, RTCSessionDescription, MediaStreamTrack
from aiortc.contrib.media import MediaRelay
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
    peer_connection: RTCPeerConnection
    room_id: str
    tracks: Set[MediaStreamTrack] = field(default_factory=set)
    relay: MediaRelay = field(default_factory=MediaRelay)
    last_ping: datetime = field(default_factory=datetime.utcnow)

class WebRTCManager:
    def __init__(self):
        self.rooms: Dict[str, Room] = {}
        self.relay = MediaRelay()
        self._cleanup_task = None
        self.start_cleanup_task()

    def start_cleanup_task(self):
        if self._cleanup_task is None:
            self._cleanup_task = asyncio.create_task(self._periodic_cleanup())

    async def _periodic_cleanup(self):
        while True:
            try:
                await self._cleanup_inactive_rooms()
                await asyncio.sleep(60)  # Her dakika kontrol et
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

    async def add_participant(self, room_id: str, participant_id: str) -> Participant:
        room = await self.get_room(room_id)
        if not room:
            raise ValueError("Room not found")
            
        if len(room.participants) >= room.max_participants:
            raise ValueError("Room is full")
            
        if participant_id in room.participants:
            raise ValueError("Participant already in room")
            
        pc = RTCPeerConnection()
        participant = Participant(
            id=participant_id,
            peer_connection=pc,
            room_id=room_id
        )
        
        room.participants[participant_id] = participant
        logger.info(f"Added participant {participant_id} to room {room_id}")
        return participant

    async def remove_participant(self, room_id: str, participant_id: str):
        room = await self.get_room(room_id)
        if not room:
            return
            
        participant = room.participants.get(participant_id)
        if not participant:
            return
            
        # Cleanup participant resources
        for track in participant.tracks:
            track.stop()
        
        await participant.peer_connection.close()
        del room.participants[participant_id]
        
        logger.info(f"Removed participant {participant_id} from room {room_id}")
        
        if not room.participants:
            await self.close_room(room_id)

    async def close_room(self, room_id: str):
        room = self.rooms.pop(room_id, None)
        if room:
            room.active = False
            for participant_id in list(room.participants.keys()):
                await self.remove_participant(room_id, participant_id)
            logger.info(f"Closed room: {room_id}")

    async def update_participant_ping(self, room_id: str, participant_id: str):
        room = await self.get_room(room_id)
        if room and participant_id in room.participants:
            room.participants[participant_id].last_ping = datetime.utcnow()

    async def process_offer(self, room_id: str, participant_id: str, offer: RTCSessionDescription) -> RTCSessionDescription:
        room = await self.get_room(room_id)
        if not room:
            raise ValueError("Room not found")
            
        participant = room.participants.get(participant_id)
        if not participant:
            raise ValueError("Participant not found")
            
        pc = participant.peer_connection
        
        @pc.on("track")
        async def on_track(track):
            logger.info(f"Track received from {participant_id}")
            participant.tracks.add(track)
            
            relayed_track = participant.relay.subscribe(track)
            
            for other_id, other in room.participants.items():
                if other_id != participant_id:
                    pc = other.peer_connection
                    sender = pc.addTrack(relayed_track)
                    other.tracks.add(sender)
        
        await pc.setRemoteDescription(offer)
        answer = await pc.createAnswer()
        await pc.setLocalDescription(answer)
        
        return pc.localDescription

# Global WebRTC Manager instance
webrtc_manager = WebRTCManager()
