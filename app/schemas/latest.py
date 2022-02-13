from typing import Dict

from pydantic import BaseModel


class LatestCurrency(BaseModel):
    base: str
    rates: Dict[str, float]
