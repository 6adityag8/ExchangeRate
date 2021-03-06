from fastapi import APIRouter, HTTPException, status, Path, Query

from app.api.constants import LATEST_PATH_PARAM
from app.api.utils import request, get_base_currency_dict
from app.core.config import settings
from app.schemas.convert import ConvertedValue

router = APIRouter()


@router.get("/{base}/{to}", response_model=ConvertedValue)
async def convert_currency(
        value: float = Query(
            ...,
            title="Value to be Converted",
            description="The value to be converted from base currency to the required currency.",
            gt=0,
            example=23.6
        ),
        base: str = Path(
            ...,
            title="Base Currency Code",
            description="3-letter ISO currency code of the base currency.",
            regex="^[A-Z]{3}$",
            example="EUR"
        ),
        to: str = Path(
            ...,
            title="Converted Currency Code",
            description="3-letter ISO currency code of the converted currency.",
            regex="^[A-Z]{3}$",
            example="INR"
        )
) -> any:
    """
    Converts any money value from one currency to another at the latest API rates.
    """
    query_parameter = {
        'app_id': settings.OPEN_EXCHANGE_RATE_APP_ID,
        'symbols': '{0},{1}'.format(base, to),
        'prettyprint': False
    }
    response = await request(path_param=LATEST_PATH_PARAM, query_param=query_parameter)
    currencies_dict = response.json().get('rates', {})
    if base not in currencies_dict or to not in currencies_dict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid currency code.",
        )
    base_currency_dict = get_base_currency_dict(base, currencies_dict)
    converted_value = value * base_currency_dict[to]
    return {
        'base': base,
        'to': to,
        'base_value': value,
        'converted_value': converted_value
    }
