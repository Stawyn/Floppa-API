"""Logging helpers."""
from __future__ import annotations

import logging
from typing import Iterable

from flask import Flask


def configure_logging(app: Flask) -> None:
    """Configure application and werkzeug loggers."""
    log_level = getattr(logging, str(app.config.get("LOG_LEVEL", "INFO")).upper(), logging.INFO)

    handler = logging.StreamHandler()
    handler.setLevel(log_level)
    handler.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s] %(name)s - %(message)s")
    )

    for logger in _unique_loggers([app.logger, logging.getLogger("werkzeug")]):
        logger.setLevel(log_level)
        logger.handlers.clear()
        logger.addHandler(handler)


def _unique_loggers(loggers: Iterable[logging.Logger]) -> list[logging.Logger]:
    seen: set[int] = set()
    unique: list[logging.Logger] = []
    for logger in loggers:
        identifier = id(logger)
        if identifier not in seen:
            seen.add(identifier)
            unique.append(logger)
    return unique
