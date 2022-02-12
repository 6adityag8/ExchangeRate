from fastapi import APIRouter, HTTPException, status

from app.api.constants import CURRENCIES_PATH_PARAM
from app.api.utils import request

router = APIRouter()


@router.get("/")
async def get_all_currencies():
    response = await request(path_param=CURRENCIES_PATH_PARAM)
    return response.json()


@router.get("/{currency_code}")
async def get_currency_from_currency_code(currency_code: str):
    response = await get_all_currencies()
    if currency_code in response:
        return {currency_code: response[currency_code]}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="No information is available for this country code.",
    )
