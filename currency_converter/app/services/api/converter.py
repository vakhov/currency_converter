""""""
import asyncio
from decimal import Decimal

import aioredis
from aioredis import Redis

from app.helpers.klasses import Singleton, Environ

env = Environ()


class ConverterApi(metaclass=Singleton):
    """API конвертера валют"""

    def __init__(self) -> None:
        self._redis: Redis = asyncio.run(self.connect())

    async def connect(self) -> Redis:
        return await aioredis.create_redis_pool(
            address=env['REDIS_URL'],
            password=env['REDIS_DEFAULT_PASS']
        )

    async def flush(self) -> None:
        """Удаляет все ключи из текущей базы"""
        await self._redis.flushdb()

    async def get(self, currency: str) -> Decimal:
        """Получение курса"""
        raise NotImplementedError()

    async def update(self, data):
        """Update данных"""
        raise NotImplementedError()
