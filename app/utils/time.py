"""Timezone helpers."""
from __future__ import annotations

from datetime import datetime

import pytz


BRAZIL_TZ = pytz.timezone("America/Sao_Paulo")


def formatted_brazil_time(fmt: str = "%d-%m-%Y %H:%M:%S") -> str:
    return datetime.now(BRAZIL_TZ).strftime(fmt)
