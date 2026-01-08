import logging
import asyncio
from typing import List, Optional, Set
from app.database import db

logger = logging.getLogger("Gravitas_BADGE_SYSTEM")

class BadgeRegistry:
    """
    Manages 'Badges' assigned to Ghosts. 
    Badges are persisted labels that grant specific capabilities across the system.
    """
    
    def __init__(self):
        self._cache = {} # ghost_id -> set of badges

    async def init_cache(self):
        """Loads all badges into memory."""
        try:
            if not db.is_ready():
                await db.connect()
            
            async with db.pool.acquire() as conn:
                rows = await conn.fetch("SELECT ghost_id, badge_name FROM agent_badges")
                self._cache = {}
                for row in rows:
                    gid = row['ghost_id']
                    if gid not in self._cache:
                        self._cache[gid] = set()
                    self._cache[gid].add(row['badge_name'])
            logger.info(f"Initialized badge cache with {len(self._cache)} agents.")
        except Exception as e:
            logger.error(f"Failed to initialize badge cache: {e}")

    async def grant_badge(self, ghost_id: str, badge_name: str):
        """Grants a badge to a ghost."""
        try:
            if not db.is_ready():
                await db.connect()
                
            async with db.pool.acquire() as conn:
                await conn.execute(
                    "INSERT INTO agent_badges (ghost_id, badge_name) VALUES ($1, $2) ON CONFLICT DO NOTHING",
                    ghost_id, badge_name
                )
            
            if ghost_id not in self._cache:
                self._cache[ghost_id] = set()
            self._cache[ghost_id].add(badge_name)
            logger.info(f"Granted badge '{badge_name}' to '{ghost_id}'")
        except Exception as e:
            logger.error(f"Failed to grant badge: {e}")

    async def revoke_badge(self, ghost_id: str, badge_name: str):
        """Revokes a badge from a ghost."""
        try:
            if not db.is_ready():
                await db.connect()
                
            async with db.pool.acquire() as conn:
                await conn.execute(
                    "DELETE FROM agent_badges WHERE ghost_id = $1 AND badge_name = $2",
                    ghost_id, badge_name
                )
            
            if ghost_id in self._cache:
                self._cache[ghost_id].discard(badge_name)
            logger.info(f"Revoked badge '{badge_name}' from '{ghost_id}'")
        except Exception as e:
            logger.error(f"Failed to revoke badge: {e}")

    def has_badge(self, ghost_id: str, badge_name: str) -> bool:
        """Checks if a ghost has a badge (from cache)."""
        return badge_name in self._cache.get(ghost_id, set())

    def get_badges(self, ghost_id: str) -> List[str]:
        """Returns all badges for a ghost."""
        return list(self._cache.get(ghost_id, set()))

# Singleton instance
badge_system = BadgeRegistry()
