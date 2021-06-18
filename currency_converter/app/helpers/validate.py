from decimal import Decimal

from pydantic import BaseModel, Field


class DataAcquisitionScheme(BaseModel):
    """Cхема данных"""
    currency_from: str = Field(alias='from')
    to: str
    amount: Decimal
