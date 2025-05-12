from functools import wraps
from typing import Optional, Type

import anyio
from loguru import logger

from .base import BaseBackend, BaseKeyMaker
from .cache_tag import CacheTag


class CacheManager:
    def __init__(self):
        self.backend: Optional[BaseBackend] = None
        self.key_maker: Optional[BaseKeyMaker] = None
        self._shutdown_lock = anyio.Lock()

    def init(self, backend: Type[BaseBackend], key_maker: Type[BaseKeyMaker]) -> None:
        self.backend = backend
        self.key_maker = key_maker

    def cached(self, prefix: str = None, tag: CacheTag = None, ttl: int = 60):
        def _cached(function):
            @wraps(function)
            async def __cached(*args, **kwargs):
                if not self.backend or not self.key_maker:
                    raise ValueError("Backend or KeyMaker not initialized")

                key = await self.key_maker.make(
                    function=function,
                    prefix=prefix if prefix else tag.value,
                )
                cached_response = await self.backend.get(key=key)
                if cached_response:
                    return cached_response

                response = await function(*args, **kwargs)
                await self.backend.set(response=response, key=key, ttl=ttl)
                return response

            return __cached

        return _cached

    async def remove_by_tag(self, tag: CacheTag) -> None:
        await self.backend.delete_startswith(value=tag.value)

    async def remove_by_prefix(self, prefix: str) -> None:
        await self.backend.delete_startswith(value=prefix)

    async def shutdown(self) -> None:
        async with self._shutdown_lock:
            if self.backend:
                try:
                    if hasattr(self.backend, "close"):
                        await self.backend.close()
                        logger.info("Cache backend closed successfully")
                    elif hasattr(self.backend, "aclose"):
                        await self.backend.aclose()
                except Exception as e:
                    logger.error(f"Error closing cache backend: {str(e)}")
                finally:
                    self.backend = None
                    self.key_maker = None


Cache = CacheManager()
