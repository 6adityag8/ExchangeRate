from typing import Dict

from pydantic import BaseModel


class CurrencyCodeDescription(BaseModel):
    codes: Dict[str, str]
