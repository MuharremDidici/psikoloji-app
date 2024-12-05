import redis
import logging
import json
import time
import os
from typing import Dict, Optional, Any
from redis.exceptions import ConnectionError, TimeoutError
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

class RedisManager:
    def __init__(self, url: Optional[str] = None):
        self.url = url or os.getenv('REDIS_URL')
        if not self.url:
            raise ValueError("Redis URL not provided and REDIS_URL environment variable not set")
            
        # Parse Redis URL for logging
        parsed_url = urlparse(self.url)
        self.host = parsed_url.hostname
        self.port = parsed_url.port
        
        logger.info(f"Initializing Redis connection to {self.host}:{self.port}")
        
        self.redis = None
        self.connection_attempts = 0
        self.max_retries = 3
        self.retry_delay = 5  # seconds
        
    def init(self):
        """Initialize Redis connection with retries"""
        while self.connection_attempts < self.max_retries:
            try:
                if not self.redis:
                    logger.info(f"Attempting to connect to Redis at {self.host}:{self.port}")
                    self.redis = redis.Redis.from_url(
                        self.url,
                        decode_responses=True,
                        socket_timeout=5,
                        socket_connect_timeout=5,
                        retry_on_timeout=True,
                        health_check_interval=30
                    )
                    self.redis.ping()  # Test connection
                    logger.info(f"Successfully connected to Redis at {self.host}:{self.port}")
                    self.connection_attempts = 0  # Reset counter on success
                    return True
            except (ConnectionError, TimeoutError) as e:
                self.connection_attempts += 1
                logger.error(f"Redis connection attempt {self.connection_attempts} failed: {str(e)}")
                if self.connection_attempts < self.max_retries:
                    logger.info(f"Retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
                    continue
                logger.error(f"Failed to connect to Redis at {self.host}:{self.port} after {self.max_retries} attempts")
                raise Exception(f"Failed to connect to Redis after {self.max_retries} attempts: {str(e)}")
            except Exception as e:
                logger.error(f"Unexpected Redis error: {str(e)}")
                raise
        return False

    def ensure_connection(self):
        """Ensure Redis connection is active"""
        try:
            if not self.redis or not self.ping():
                logger.info("Redis connection lost, attempting to reconnect...")
                return self.init()
            return True
        except Exception as e:
            logger.error(f"Failed to ensure Redis connection: {str(e)}")
            return False

    def set_participant_status(self, room_id: str, participant_id: str, status: Dict[str, Any]):
        """Set participant status in Redis"""
        try:
            if not self.ensure_connection():
                logger.error("Cannot set participant status: Redis connection not available")
                return
            
            key = f"participant:{participant_id}"
            self.redis.hmset(key, status)
            self.redis.expire(key, 3600)  # 1 hour expiry
            logger.debug(f"Set status for participant {participant_id}")
        except Exception as e:
            logger.error(f"Error setting participant status: {str(e)}")

    def get_participant_status(self, room_id: Optional[str], participant_id: str) -> Optional[Dict[str, Any]]:
        """Get participant status from Redis"""
        try:
            if not self.ensure_connection():
                logger.error("Cannot get participant status: Redis connection not available")
                return None
                
            key = f"participant:{participant_id}"
            status = self.redis.hgetall(key)
            return status if status else None
        except Exception as e:
            logger.error(f"Error getting participant status: {str(e)}")
            return None

    def update_participant_status(self, room_id: str, participant_id: str, updates: Dict[str, Any]):
        """Update participant status in Redis"""
        try:
            if not self.ensure_connection():
                logger.error("Cannot update participant status: Redis connection not available")
                return
                
            key = f"participant:{participant_id}"
            self.redis.hmset(key, updates)
            logger.debug(f"Updated status for participant {participant_id}")
        except Exception as e:
            logger.error(f"Error updating participant status: {str(e)}")

    def remove_participant_status(self, room_id: str, participant_id: str):
        """Remove participant status from Redis"""
        try:
            if not self.ensure_connection():
                logger.error("Cannot remove participant status: Redis connection not available")
                return
                
            key = f"participant:{participant_id}"
            self.redis.delete(key)
            logger.debug(f"Removed status for participant {participant_id}")
        except Exception as e:
            logger.error(f"Error removing participant status: {str(e)}")

    def ping(self) -> bool:
        """Check Redis connection"""
        try:
            return bool(self.redis and self.redis.ping())
        except Exception as e:
            logger.error(f"Redis ping failed: {str(e)}")
            return False

    def close(self):
        """Close Redis connection"""
        try:
            if self.redis:
                self.redis.close()
                self.redis = None
                logger.info(f"Redis connection to {self.host}:{self.port} closed")
        except Exception as e:
            logger.error(f"Error closing Redis connection: {str(e)}")

# Global Redis Manager instance
redis_manager = RedisManager()
