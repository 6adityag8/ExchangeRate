from pydantic import BaseModel


class CurrencyCode(BaseModel):
    currency_code: str
