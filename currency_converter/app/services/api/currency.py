""""""
import asyncio
import re
from decimal import Decimal

import aioredis
from aioredis import Redis

from app.helpers.klasses import Singleton, Environ
from app.services.api.exceptions import CurrencyValueError, CurrencyNotFound

env = Environ()

english_check = re.compile(r'[a-zA-Z]]')


class CurrencyApi(metaclass=Singleton):
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
        """
        Получение курса валюты
        :param currency: строковое представление валюты
        :return: курс
        """
        if not isinstance(currency, str) or not english_check.match(currency):
            raise CurrencyValueError(f'Неверно заданное значение валюты `{currency}`.')
        value = await self._redis.lindex(key=currency, index=-1)
        if value is None:
            raise CurrencyNotFound(f'Валюта {currency} не была найдена.')
        return value

    async def update(self, data):
        """Update данных"""
        raise NotImplementedError()
