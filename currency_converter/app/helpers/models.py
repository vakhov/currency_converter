from decimal import Decimal

from pydantic import BaseModel, Field


class DataAcquisitionScheme(BaseModel):
    """Cхема данных"""
    cur_from: str = Field(alias='from')
    cur_to: str = Field(alias='to')
    amount: Decimal
