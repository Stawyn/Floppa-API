"""Alert related routes."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import requests
from flask import Blueprint, current_app, jsonify

from app.extensions import limiter
from app.services.freestuff import (
    fetch_free_game_ids,
    fetch_game_details,
    read_last_game_id,
    upload_thumbnail,
    write_last_game_id,
)
from app.utils.auth import require_api_key


alerts_bp = Blueprint("alerts", __name__, url_prefix="/alert")


@alerts_bp.get("/games")
@limiter.limit("1 per 4 minutes")
@require_api_key
def free_games() -> tuple[Any, int] | tuple[list[dict[str, Any]], int]:
    last_game_file = Path(current_app.config["LAST_GAME_ID_FILE"])

    try:
        game_ids = fetch_free_game_ids()
    except requests.HTTPError as exc:  # pragma: no cover - depends on external API
        status = exc.response.status_code if exc.response else 502
        if status == 429:
            return {"error": "rate_limit", "error_desc": "Rate limit exceeded"}, status
        return {"error": "freestuff_error", "error_desc": str(exc)}, status

    if not game_ids:
        return jsonify([]), 200

    last_seen_id = read_last_game_id(last_game_file)
    games: list[dict[str, Any]] = []

    for game_id in game_ids[:1]:
        try:
            details = fetch_game_details(game_id)
        except requests.HTTPError as exc:  # pragma: no cover
            current_app.logger.warning("Failed to fetch game %s info: %s", game_id, exc)
            continue

        if not details:
            continue

        detail_id = details.get("id")
        if detail_id is None:
            continue

        try:
            numeric_id = int(detail_id)
        except (TypeError, ValueError):  # pragma: no cover - defensive
            current_app.logger.debug("Game id %s is not numeric", detail_id)
            numeric_id = None

        if last_seen_id and numeric_id == last_seen_id:
            continue
        thumbnail_url = details.get("thumbnail", {}).get("org")
        image_url = None
        if thumbnail_url:
            try:
                response = requests.get(thumbnail_url, timeout=30)
                response.raise_for_status()
                image_url = upload_thumbnail(response.content)
            except requests.RequestException as exc:  # pragma: no cover
                current_app.logger.warning("Unable to upload thumbnail: %s", exc)

        game_payload = {
            "id": details.get("id"),
            "nome": details.get("title"),
            "descri": details.get("description"),
            "linkd": details.get("urls", {}).get("browser"),
            "termino": details.get("localized", {}).get("pt-BR", {}).get("until"),
            "brl": details.get("org_price", {}).get("brl"),
            "tumbnail": image_url,
        }
        games.append(game_payload)
        if numeric_id is not None:
            write_last_game_id(last_game_file, numeric_id)

    return jsonify(games), 200
