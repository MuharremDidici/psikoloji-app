import aioredis
import json
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class RedisManager:
    def __init__(self, url: str = "redis://localhost"):
        self.redis = aioredis.from_url(url, decode_responses=True)
        
    async def init(self):
        try:
            await self.redis.ping()
            logger.info("Redis connection established")
        except Exception as e:
            logger.error(f"Redis connection failed: {e}")
            raise

    async def set_room_data(self, room_id: str, data: Dict[str, Any], expire_seconds: int = 3600):
        """Store room data with expiration"""
        key = f"room:{room_id}"
        try:
            await self.redis.setex(
                key,
                expire_seconds,
                json.dumps(data)
            )
        except Exception as e:
            logger.error(f"Error setting room data: {e}")
            raise

    async def get_room_data(self, room_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve room data"""
        key = f"room:{room_id}"
        try:
            data = await self.redis.get(key)
            return json.loads(data) if data else None
        except Exception as e:
            logger.error(f"Error getting room data: {e}")
            return None

    async def set_participant_status(self, room_id: str, participant_id: str, status: Dict[str, Any]):
        """Update participant status"""
        key = f"participant:{room_id}:{participant_id}"
        try:
            status["last_updated"] = datetime.utcnow().isoformat()
            await self.redis.setex(
                key,
                300,  # 5 minutes expiration
                json.dumps(status)
            )
        except Exception as e:
            logger.error(f"Error setting participant status: {e}")
            raise

    async def get_participant_status(self, room_id: str, participant_id: str) -> Optional[Dict[str, Any]]:
        """Get participant status"""
        key = f"participant:{room_id}:{participant_id}"
        try:
            data = await self.redis.get(key)
            return json.loads(data) if data else None
        except Exception as e:
            logger.error(f"Error getting participant status: {e}")
            return None

    async def get_room_participants(self, room_id: str) -> Dict[str, Any]:
        """Get all participants in a room"""
        try:
            pattern = f"participant:{room_id}:*"
            keys = await self.redis.keys(pattern)
            
            participants = {}
            for key in keys:
                participant_id = key.split(":")[-1]
                status = await self.get_participant_status(room_id, participant_id)
                if status:
                    participants[participant_id] = status
                    
            return participants
        except Exception as e:
            logger.error(f"Error getting room participants: {e}")
            return {}

    async def cleanup_inactive_participants(self, max_inactive_time: int = 300):
        """Remove inactive participants"""
        try:
            pattern = "participant:*"
            keys = await self.redis.keys(pattern)
            
            now = datetime.utcnow()
            for key in keys:
                data = await self.redis.get(key)
                if data:
                    status = json.loads(data)
                    last_updated = datetime.fromisoformat(status["last_updated"])
                    
                    if (now - last_updated) > timedelta(seconds=max_inactive_time):
                        await self.redis.delete(key)
                        
        except Exception as e:
            logger.error(f"Error cleaning up inactive participants: {e}")

    async def close(self):
        """Close Redis connection"""
        try:
            await self.redis.close()
            logger.info("Redis connection closed")
        except Exception as e:
            logger.error(f"Error closing Redis connection: {e}")

# Global Redis Manager instance
redis_manager = RedisManager()
