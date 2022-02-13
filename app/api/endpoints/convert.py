from fastapi import APIRouter, HTTPException, status

from app.api.constants import LATEST_PATH_PARAM
from app.api.utils import request
from app.core.config import settings
from app.schemas.convert import ConvertedValue

router = APIRouter()


@router.get("/", response_model=ConvertedValue)
async def convert_currency(value: float, base: str, to: str):
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
            detail="Invalid country code.",
        )
    converted_value = (value * currencies_dict.get(to)) / currencies_dict.get(base)
    return {
        'base': base,
        'to': to,
        'base_value': value,
        'converted_value': converted_value
    }
