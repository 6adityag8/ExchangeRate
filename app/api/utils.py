from typing import Optional, Dict, List

import httpx
from furl import furl
from pydantic import HttpUrl

from app.api.constants import OPENEXCHANGERATES_BASE_URL


async def request(
        path_param: Optional[List[str]] = None,
        query_param: Optional[Dict[str, str]] = None
) -> any:
    url = prepare_url(path_param, query_param)
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    return response


def prepare_url(
        path_param: Optional[List[str]] = None,
        query_param: Optional[Dict[str, str]] = None
) -> HttpUrl:
    f = furl(OPENEXCHANGERATES_BASE_URL)
    f.add(path=path_param, query_params=query_param)
    return f.url
