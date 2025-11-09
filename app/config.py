"""Centralised application configuration."""
from __future__ import annotations

import os
from pathlib import Path


class Config:
    """Base configuration for all environments."""

    BASE_DIR = Path(__file__).resolve().parent.parent

    API_KEYS = {
        key.strip()
        for key in os.getenv("APP_API_KEYS", "Floppa887,jorgegogorio23").split(",")
        if key.strip()
    }

    FREESTUFF_API_KEY = os.getenv(
        "FREESTUFF_API_KEY",
        "Basic NTg0MTE5MDg3NzQ0MDI0NzE3.00KOS7D8xreAwbav21vVqe4D.c0c8",
    )
    LASTFM_API_KEY = os.getenv(
        "LASTFM_API_KEY", "afe79d2eec23a06e9b39a879b5427559"
    )
    IMGBB_API_KEY = os.getenv("IMGBB_API_KEY", "4170baf9ab968eeec13a3bc79553447a")
    CHARACTER_AI_TOKEN = os.getenv(
        "CHARACTER_AI_TOKEN", "2f97b396ac603fe7e787952a68ecdf94988e5a3a"
    )
    CHARACTER_ID = os.getenv(
        "CHARACTER_ID", "zveWItgxoXlh19utBS7pt5rSEDnohG7B7QJeTPdvdL0"
    )
    BING_AUTH_TOKEN = os.getenv(
        "BING_AUTH_TOKEN",
        "1JyskSYHBQDULjRx0eiYm_tkkNQ8eDbZMoaPGk3iJlSH6i2bOHJgcs1hjAdE7-zSsQAcLSNM13ypKWA1v_jIy2tchnsvCBvcpMFUPV-jQo7hW8uCQcnKbi3NpB_eobTxylzYBGdsRA9Grv2fC_BcuAis1CjM8Z7GbDz2q78AZ2-_lK8txHghpJ4jY739F9haAnSKS6S0aRvx7ViOGwLFzXw",
    )

    DATABASE_FM = os.getenv(
        "DATABASE_FM", str(BASE_DIR / "DATABASE_FM.json")
    )
    LAST_GAME_ID_FILE = os.getenv(
        "LAST_GAME_ID_FILE", str(BASE_DIR / "last_game_id.txt")
    )

    LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
    RATELIMIT_STORAGE = os.getenv("RATELIMIT_STORAGE", "memory://")

    FROSTING_DEFAULT_NEGATIVE_PROMPT = os.getenv(
        "FROSTING_DEFAULT_NEGATIVE_PROMPT",
        (
            "Bug, bugged, anatomy bugs, contemporary, realistic, rustic, primitive, ugly, "
            "deformed, noisy, blurry, low contrast, cheerful, lowres, cropped, pixelated, "
            "padding, third dimension, black and white, photo, disfigured, mutated, "
            "glitch, off-center, bad anatomy, poorly drawn hands"
        ),
    )

    # Flask
    JSON_SORT_KEYS = False
    TEMPLATES_AUTO_RELOAD = True
