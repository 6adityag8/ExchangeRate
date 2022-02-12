from fastapi import APIRouter, HTTPException, status

from app.api.constants import LATEST_PATH_PARAM
from app.api.utils import request
from app.core.config import settings
from app.schemas.convert import ConvertedValue

router = APIRouter()


@router.get("/", response_model=ConvertedValue)
async def convert_currency(value: float, from_currency: str, to_currency: str):
    query_parameter = {
        'app_id': settings.OPEN_EXCHANGE_RATE_APP_ID,
        'symbols': '{0},{1}'.format(from_currency, to_currency)
    }
    response = await request(path_param=LATEST_PATH_PARAM, query_param=query_parameter)
    currencies_dict = response.json().get('rates', {})
    if from_currency not in currencies_dict or to_currency not in currencies_dict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid country code.",
        )
    converted_value = (value * currencies_dict.get(to_currency)) / currencies_dict.get(from_currency)
    return {'converted_value': converted_value}
