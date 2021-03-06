import json
from typing import Optional


class CurrencyError(Exception):
    """Base Currency Exception"""

    def __init__(self, message: Optional[str] = None) -> None:
        self._message = message

    @property
    def message(self) -> str:
        if not self._message:
            return self.__doc__.strip()
        return self._message

    def __str__(self) -> str:
        return self.message

    def __repr__(self) -> str:
        return "{class_name}('{message}')".format(
            class_name=self.__class__.__name__,
            message=self.message
        )

    def to_dict(self):
        return dict(
            error=self.message
        )

    def json(self):
        return json.dumps(self.to_dict())


class CurrencyValueError(CurrencyError):
    """Неверное значение валюты"""


class CurrencyNotFound(CurrencyError):
    """Валюта не найдена"""


class CurrencyInvalidValue(CurrencyError):
    """Неверное значение цены валюты."""
