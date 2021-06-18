from aioredis import Redis, create_redis_pool

from app.helpers.klasses import Environ
from app.services.api.currency import CurrencyApi

env = Environ()


class ConnectMixin:
    async def connect(self) -> Redis:
        """коннект к redis"""
        return await create_redis_pool(
            address=env['REDIS_URL'],
            password=env['REDIS_DEFAULT_PASS']
        )

    @property
    async def currency_api(self) -> CurrencyApi:
        return CurrencyApi(redis_connection=await self.connect())
