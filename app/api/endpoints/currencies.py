from fastapi import APIRouter, HTTPException, status

from app.api.constants import CURRENCIES_PATH_PARAM
from app.api.utils import request
from app.schemas.currencies import CurrencyCode

router = APIRouter()


@router.get("/", response_model=CurrencyCode)
async def get_all_currencies():
    response = await request(path_param=CURRENCIES_PATH_PARAM)
    return {
        'codes': response.json()
    }


@router.get("/{currency_code}", response_model=CurrencyCode)
async def get_currency_from_currency_code(currency_code: str):
    response = await get_all_currencies()
    if currency_code not in response['codes']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid country code.",
        )
    return {
        'codes': {
            currency_code: response['codes'][currency_code]
        }
    }
