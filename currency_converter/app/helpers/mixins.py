from typing import Optional

from aioredis import Redis, create_redis_pool

from app.helpers.klasses import Environ
from app.services.api.currency import CurrencyApi

env = Environ()


class RedisConnectMixin:
    """Миксин добавляющий подключение к БД"""
    _connection: Optional[Redis] = None

    async def connect(self) -> Redis:
        """Коннект к redis"""
        if not self._connection:
            self._connection = await create_redis_pool(
                address=env['REDIS_URL'],
                password=env['REDIS_DEFAULT_PASS']
            )
        return self._connection

    @property
    async def currency_api(self) -> CurrencyApi:
        return CurrencyApi(redis_connection=await self.connect())
