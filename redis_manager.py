import redis
import logging
import json
import time
import os
from typing import Dict, Optional, Any
from redis.exceptions import ConnectionError, TimeoutError

logger = logging.getLogger(__name__)

class RedisManager:
    def __init__(self, url: Optional[str] = None):
        self.url = url or os.getenv('REDIS_URL', "redis://localhost:6379")
        self.redis = None
        self.connection_attempts = 0
        self.max_retries = 3
        self.retry_delay = 5  # seconds
        
    def init(self):
        """Initialize Redis connection with retries"""
        while self.connection_attempts < self.max_retries:
            try:
                if not self.redis:
                    self.redis = redis.Redis.from_url(
                        self.url,
                        decode_responses=True,
                        socket_timeout=5,
                        socket_connect_timeout=5,
                        retry_on_timeout=True
                    )
                    self.redis.ping()  # Test connection
                    logger.info("Redis connection initialized successfully")
                    self.connection_attempts = 0  # Reset counter on success
                    return True
            except (ConnectionError, TimeoutError) as e:
                self.connection_attempts += 1
                logger.error(f"Redis connection attempt {self.connection_attempts} failed: {e}")
                if self.connection_attempts < self.max_retries:
                    time.sleep(self.retry_delay)
                    continue
                raise Exception(f"Failed to connect to Redis after {self.max_retries} attempts")
            except Exception as e:
                logger.error(f"Unexpected Redis error: {e}")
                raise
        return False

    def ensure_connection(self):
        """Ensure Redis connection is active"""
        try:
            if not self.redis or not self.ping():
                return self.init()
            return True
        except Exception as e:
            logger.error(f"Failed to ensure Redis connection: {e}")
            return False

    def set_participant_status(self, room_id: str, participant_id: str, status: Dict[str, Any]):
        """Set participant status in Redis"""
        try:
            if not self.ensure_connection():
                return
            
            key = f"participant:{participant_id}"
            self.redis.hmset(key, status)
            self.redis.expire(key, 3600)  # 1 hour expiry
            logger.debug(f"Set status for participant {participant_id}")
        except Exception as e:
            logger.error(f"Error setting participant status: {e}")

    def get_participant_status(self, room_id: Optional[str], participant_id: str) -> Optional[Dict[str, Any]]:
        """Get participant status from Redis"""
        try:
            if not self.ensure_connection():
                return None
                
            key = f"participant:{participant_id}"
            status = self.redis.hgetall(key)
            return status if status else None
        except Exception as e:
            logger.error(f"Error getting participant status: {e}")
            return None

    def update_participant_status(self, room_id: str, participant_id: str, updates: Dict[str, Any]):
        """Update participant status in Redis"""
        try:
            if not self.ensure_connection():
                return
                
            key = f"participant:{participant_id}"
            self.redis.hmset(key, updates)
            logger.debug(f"Updated status for participant {participant_id}")
        except Exception as e:
            logger.error(f"Error updating participant status: {e}")

    def remove_participant_status(self, room_id: str, participant_id: str):
        """Remove participant status from Redis"""
        try:
            if not self.ensure_connection():
                return
                
            key = f"participant:{participant_id}"
            self.redis.delete(key)
            logger.debug(f"Removed status for participant {participant_id}")
        except Exception as e:
            logger.error(f"Error removing participant status: {e}")

    def ping(self) -> bool:
        """Check Redis connection"""
        try:
            return bool(self.redis and self.redis.ping())
        except Exception as e:
            logger.error(f"Redis ping failed: {e}")
            return False

    def close(self):
        """Close Redis connection"""
        try:
            if self.redis:
                self.redis.close()
                self.redis = None
                logger.info("Redis connection closed")
        except Exception as e:
            logger.error(f"Error closing Redis connection: {e}")

# Global Redis Manager instance
redis_manager = RedisManager()
