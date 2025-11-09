"""Authentication helpers."""
from __future__ import annotations

from functools import wraps
from typing import Callable, TypeVar, cast

from flask import current_app, request

from .errors import error_response

F = TypeVar("F", bound=Callable[..., object])


def is_valid_api_key(api_key: str | None) -> bool:
    keys = current_app.config.get("API_KEYS", set())
    return bool(api_key and api_key in keys)


def require_api_key(func: F) -> F:
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not is_valid_api_key(request.args.get("apikey")):
            return error_response(401)
        return func(*args, **kwargs)

    return cast(F, wrapper)
