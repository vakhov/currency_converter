""""""
from decimal import Decimal

from redis import Redis

from app.helpers.klasses import Singleton, Environ

env = Environ()


class ConverterApi(metaclass=Singleton):
    """API конвертера валют"""

    def __init__(self) -> None:
        self._redis = Redis('redis', password=env['REDIS_DEFAULT_PASS'])

    def flush(self) -> None:
        """Удаляет все ключи из текущей базы"""
        self._redis.flushdb()

    def get(self, currenci: str) -> Decimal:
        """Получение курса"""
        raise NotImplementedError()

    def update(self, data):
        """Update данных"""
        raise NotImplementedError()
