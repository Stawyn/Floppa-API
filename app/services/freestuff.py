"""Helpers for interacting with the FreeStuff API."""
from __future__ import annotations

import base64
from pathlib import Path
from typing import Any

import requests
from flask import current_app


GAMES_ENDPOINT = "https://api.freestuffbot.xyz/v1/games/free"
GAME_INFO_ENDPOINT = "https://api.freestuffbot.xyz/v1/game/{game_id}/info"
IMGBB_ENDPOINT = "https://api.imgbb.com/1/upload"


class FreeStuffError(RuntimeError):
    """Raised when the external API returns an unexpected response."""


def _auth_headers() -> dict[str, str]:
    return {"Authorization": current_app.config["FREESTUFF_API_KEY"]}


def fetch_free_game_ids() -> list[int]:
    response = requests.get(GAMES_ENDPOINT, headers=_auth_headers(), timeout=30)
    response.raise_for_status()
    payload = response.json()
    return payload.get("data", [])


def fetch_game_details(game_id: int) -> dict[str, Any]:
    params = {"lang": "pt-BR"}
    url = GAME_INFO_ENDPOINT.format(game_id=game_id)
    response = requests.get(url, headers=_auth_headers(), params=params, timeout=30)
    response.raise_for_status()
    payload = response.json().get("data", {})
    return payload.get(str(game_id), {})


def upload_thumbnail(content: bytes) -> str:
    encoded = base64.b64encode(content).decode("utf-8")
    data = {"expiration": 600, "key": current_app.config["IMGBB_API_KEY"], "image": encoded}
    response = requests.post(IMGBB_ENDPOINT, data=data, timeout=30)
    response.raise_for_status()
    return response.json()["data"]["url"]


def read_last_game_id(path: Path) -> int | None:
    if not path.exists():
        return None
    raw = path.read_text().strip()
    return int(raw) if raw else None


def write_last_game_id(path: Path, game_id: int) -> None:
    path.write_text(str(game_id))
