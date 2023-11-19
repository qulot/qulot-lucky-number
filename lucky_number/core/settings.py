# settings.py
import os
from typing import Any
import typing
from dotenv import load_dotenv


def load_settings():
    load_dotenv()


def get(key: str, default: Any = None):
    return os.environ.get(key, default)


def set(key: str, value: typing.Any, override: bool = True):
    if os.environ[key] and not override:
        return

    os.environ[key] = str(value)
