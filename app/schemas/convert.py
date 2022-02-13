from pydantic import BaseModel


class ConvertedValue(BaseModel):
    base: str
    to: str
    base_value: float
    converted_value: float
