from redis.asyncio import Redis
import json
from typing import Optional, Any


class WeatherCache:
    _instance = None

    def __new__(cls, default_ttl: int = 300):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.redis = Redis(host="local_redis", port=6379, decode_responses=True)
            cls._instance.default_ttl = default_ttl
        return cls._instance

    async def get(self, key: str) -> Optional[Any]:
        data = await self.redis.get(key)
        if data is None:
            return None
        return json.loads(data)

    async def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """Сохранить данные в кеш с TTL"""
        ttl = ttl or self.default_ttl
        await self.redis.set(key, json.dumps(value), ex=ttl)

    async def delete(self, key: str):
        """Удалить данные из кеша"""
        await self.redis.delete(key)

    async def exists(self, key: str) -> bool:
        """Проверка существования ключа в кеше"""
        return await self.redis.exists(key) > 0
