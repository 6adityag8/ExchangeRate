from typing import Optional, Set

from fastapi import APIRouter, HTTPException, status, Path, Query
from pydantic import constr

from app.api.utils import request, get_base_currency_dict
from app.core.config import settings
from app.schemas.historical import HistoricalCurrency

router = APIRouter()


@router.get("/{base}", response_model=HistoricalCurrency)
async def get_historical_exchange_rate(
        base: str = Path(
            ...,
            title="Base Currency Code",
            description="3-letter ISO currency code of the base currency.",
            regex="^[A-Z]{3}$",
            example="EUR"
        ),
        date: str = Query(
            ...,
            title="Requested date",
            description="The requested date in YYYY-MM-DD format.",
            regex=r"^(\d{4})[-](\d{2})[-](\d{2})$",
            example="2012-07-10"
        ),
        currencies: Optional[Set[constr(regex="^[A-Z]{3}$")]] = Query(
            None,
            title="Limit results to specific currencies",
            description="List of 3-letter ISO currency codes for which the results are needed to be limited to."
        )
):
    query_parameter = {
        'app_id': settings.OPEN_EXCHANGE_RATE_APP_ID,
        'prettyprint': False
    }
    if currencies:
        query_parameter['symbols'] = '{0},{1}'.format(base, ','.join(currencies))
    response = await request(path_param=['historical', '{0}.json'.format(date)], query_param=query_parameter)
    currencies_dict = response.json().get('rates', {})
    if base not in currencies_dict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid currency code for Base Currency.",
        )
    base_currency_dict = get_base_currency_dict(base, currencies_dict)
    return {
        'base': base,
        'requested_date': date,
        'rates': base_currency_dict
    }
