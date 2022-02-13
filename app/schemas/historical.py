from typing import Dict

from pydantic import BaseModel


class HistoricalCurrency(BaseModel):
    base: str
    requested_date: str
    rates: Dict[str, float]
