import redis
import logging
import json
import time
from typing import Dict, Optional, Any

logger = logging.getLogger(__name__)

class RedisManager:
    def __init__(self, url: Optional[str] = None):
        self.url = url or "redis://localhost:6379"
        self.redis = None
        
    def init(self):
        """Initialize Redis connection"""
        try:
            self.redis = redis.Redis.from_url(self.url, decode_responses=True)
            logger.info("Redis connection initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Redis: {e}")
            raise

    def set_participant_status(self, room_id: str, participant_id: str, status: Dict[str, Any]):
        """Set participant status in Redis"""
        try:
            key = f"participant:{participant_id}"
            self.redis.hmset(key, status)
            self.redis.expire(key, 3600)  # 1 hour expiry
        except Exception as e:
            logger.error(f"Error setting participant status: {e}")

    def get_participant_status(self, room_id: Optional[str], participant_id: str) -> Optional[Dict[str, Any]]:
        """Get participant status from Redis"""
        try:
            key = f"participant:{participant_id}"
            status = self.redis.hgetall(key)
            return status if status else None
        except Exception as e:
            logger.error(f"Error getting participant status: {e}")
            return None

    def update_participant_status(self, room_id: str, participant_id: str, updates: Dict[str, Any]):
        """Update participant status in Redis"""
        try:
            key = f"participant:{participant_id}"
            self.redis.hmset(key, updates)
        except Exception as e:
            logger.error(f"Error updating participant status: {e}")

    def remove_participant_status(self, room_id: str, participant_id: str):
        """Remove participant status from Redis"""
        try:
            key = f"participant:{participant_id}"
            self.redis.delete(key)
        except Exception as e:
            logger.error(f"Error removing participant status: {e}")

    def ping(self) -> bool:
        """Check Redis connection"""
        try:
            return bool(self.redis.ping())
        except Exception as e:
            logger.error(f"Redis ping failed: {e}")
            return False

    def close(self):
        """Close Redis connection"""
        try:
            if self.redis:
                self.redis.close()
                logger.info("Redis connection closed")
        except Exception as e:
            logger.error(f"Error closing Redis connection: {e}")

# Global Redis Manager instance
redis_manager = RedisManager()
