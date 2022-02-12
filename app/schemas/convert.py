from pydantic import BaseModel


class ConvertedValue(BaseModel):
    converted_value: str
