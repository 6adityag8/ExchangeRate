from typing import Dict

from pydantic import BaseModel


class CurrencyCode(BaseModel):
    codes: Dict[str, str]
