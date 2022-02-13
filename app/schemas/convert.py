from pydantic import BaseModel


class ConvertedValue(BaseModel):
    base: str
    to: str
    base_value: str
    converted_value: str
