from typing import Optional

from fastapi import APIRouter, HTTPException, status

from app.api.constants import LATEST_PATH_PARAM
from app.api.utils import request, get_base_currency_dict
from app.core.config import settings
from app.schemas.latest import LatestCurrency

router = APIRouter()


@router.get("/", response_model=LatestCurrency)
async def get_latest_exchange_rate(base: str, currencies: Optional[str] = None):
    query_parameter = {
        'app_id': settings.OPEN_EXCHANGE_RATE_APP_ID,
        'prettyprint': False
    }
    if currencies:
        query_parameter['symbols'] = '{0},{1}'.format(base, currencies)
    response = await request(path_param=LATEST_PATH_PARAM, query_param=query_parameter)
    currencies_dict = response.json().get('rates', {})
    if base not in currencies_dict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid country code for Base Currency.",
        )
    base_currency_dict = get_base_currency_dict(base, currencies_dict)
    return {
        'base': base,
        'rates': base_currency_dict
    }
