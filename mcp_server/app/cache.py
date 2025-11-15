import asyncio
import time
from typing import Any, Dict, Callable, Awaitable

class TTLCache:
    def __init__(self):
        self._store: Dict[str, Any] = {}
        self._expiry: Dict[str, float] = {}
        self._lock = asyncio.Lock()

    async def get_or_set(
        self,
        key: str,
        fetcher: Callable[[], Awaitable[Any]],
        ttl: int = 5
    ):
        async with self._lock:
            # 1. If exists & not expired → return cached
            if key in self._store and time.time() < self._expiry.get(key, 0):
                return self._store[key]

        # 2. If expired → fetch fresh data
        value = await fetcher()

        async with self._lock:
            self._store[key] = value
            self._expiry[key] = time.time() + ttl
        
        return value


ttl_cache = TTLCache()

