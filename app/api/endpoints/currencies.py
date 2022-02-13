from typing import Dict

from fastapi import APIRouter, HTTPException, status, Path
from pydantic import Json

from app.api.constants import CURRENCIES_PATH_PARAM
from app.api.utils import request
from app.schemas.currencies import CurrencyCodeDescription

router = APIRouter()


@router.get("/", response_model=CurrencyCodeDescription)
async def get_all_currencies() -> Dict[str, Json]:
    """
    Gets a JSON list of all currency symbols available from
    the Open Exchange Rates API, along with their full names
    """
    response = await request(path_param=CURRENCIES_PATH_PARAM)
    return {
        'codes': response.json()
    }


@router.get("/{currency_code}", response_model=CurrencyCodeDescription)
async def get_currency_description_from_currency_code(
        currency_code: str = Path(
            ...,
            title="Currency Code",
            description="3-letter ISO currency code for which the description is needed.",
            regex="^[A-Z]{3}$",
            example="EUR"
        )
) -> any:
    """
    Gets the currency description for the requested currency symbol.
    """
    response = await get_all_currencies()
    if currency_code not in response['codes']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid currency code.",
        )
    return {
        'codes': {
            currency_code: response['codes'][currency_code]
        }
    }
