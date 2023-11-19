from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyQuery
from lucky_number.core import settings
import typing

_api_key_scheme = APIKeyQuery(name='api_key')  # use token authentication


_api_keys: typing.List[str] = None


def get_api_keys():
    global _api_keys
    if _api_keys is None:
        raw_api_keys_str = settings.get('API_KEY', '')
        _api_keys = [api_key.strip()
                     for api_key in raw_api_keys_str.split(',')]

    return _api_keys


def api_key_auth(api_key: str = Depends(_api_key_scheme)):
    keys = get_api_keys()
    if api_key not in keys:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Forbidden"
        )
    return api_key
