from fastapi import APIRouter, HTTPException, status

from app.api.constants import CURRENCIES_PATH_PARAM
from app.api.utils import request
from app.schemas.currencies import CurrencyCode

router = APIRouter()


@router.get("/")
async def get_all_currencies():
    response = await request(path_param=CURRENCIES_PATH_PARAM)
    return response.json()


@router.get("/{currency_code}", response_model=CurrencyCode)
async def get_currency_from_currency_code(currency_code: str):
    response = await get_all_currencies()
    if currency_code not in response:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid country code.",
        )
    return {currency_code: response[currency_code]}
