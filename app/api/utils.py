from typing import Optional, Dict, List

import httpx
from furl import furl
from pydantic import HttpUrl

from app.api.constants import OPENEXCHANGERATES_BASE_URL


async def request(
        path_param: Optional[List[str]] = None,
        query_param: Optional[Dict[str, str]] = None
) -> any:
    """
    Makes an async GET call to the OpenExchange URL
    after adding the given path & query parameters.
    :param path_param: path parameters to be added to the URL
    :param query_param: query parameters to be sent with the URL
    :return: httpx Response object
    """
    url = prepare_url(path_param, query_param)
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    return response


def prepare_url(
        path_param: Optional[List[str]] = None,
        query_param: Optional[Dict[str, str]] = None
) -> HttpUrl:
    """
    Prepares the OpenExchange API call by
    adding the given path & query parameters
    :param path_param: path parameters to be added to the URL
    :param query_param: query parameters to be sent with the URL
    :return: prepared OpenExchange URL
    """
    f = furl(OPENEXCHANGERATES_BASE_URL)
    f.add(path=path_param, query_params=query_param)
    return f.url


def get_base_currency_dict(base: str, currency_dict: Dict[str, float]) -> Dict[str, float]:
    """
    Converts USD based currency dictionary to that of the given base currency.
    :param base: base currency code
    :param currency_dict: USD based currency dictionary
    :return: base currency converted currency dictionary
    """
    base_value = 1 / currency_dict[base]
    base_currency_dict = {}
    for currency_code, currency_value in currency_dict.items():
        base_currency_dict[currency_code] = base_value * currency_value
    base_currency_dict.pop(base, None)
    return base_currency_dict
