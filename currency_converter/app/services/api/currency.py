"""API по получению курса и его обновлению"""
import re
from decimal import Decimal
from typing import Dict

import aioredis
from aioredis import Redis

from app.helpers.klasses import Singleton, Environ
from app.services.api.exceptions import CurrencyValueError, CurrencyNotFound

env = Environ()

english_check = re.compile(r'[a-zA-Z]]')


class CurrencyApi(metaclass=Singleton):
    """API конвертера валют"""

    def __init__(self, redis_connection) -> None:
        self._redis: redis_connection = redis_connection

    async def flush(self) -> None:
        """Удаляет все ключи из текущей базы"""
        await self._redis.flushdb()

    async def get(self, currency: str) -> Decimal:
        """
        Получение курса валюты

        :param currency: строковое представление валюты
        :return: курс
        """
        if not isinstance(currency, str) and not english_check.match(currency):
            raise CurrencyValueError(f'Неверно заданное значение валюты `{currency}`.')
        if currency.upper() == 'RUB':
            return Decimal(1.0)
        rate: bytes = await self._redis.lindex(key=currency.upper(), index=-1)
        if rate is None:
            raise CurrencyNotFound(f'Валюта {currency} не была найдена.')
        return Decimal(rate.decode())

    async def update(self, data: Dict[str, Decimal], merge=True):
        """
        Update данных

        :param data: Словарь содержащий в качестве ключа наименование валюты, а значение стоимость.
        :param merge: True то старые данные инвалидируются,
                      False то новые данные перетирают старые, но старые все еще акутальны, если не перетерты.
        """
        if not merge:
            await self.flush()
        currency: str
        rate: Decimal
        for currency, rate in data.items():
            await self._redis.rpush(currency.upper(), rate)
