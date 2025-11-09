"""Downloader related routes."""
from __future__ import annotations

from pathlib import Path

import requests
from flask import Blueprint, abort, jsonify, request, send_file

from app.utils.auth import require_api_key
from app.utils.errors import error_response


downloads_bp = Blueprint("downloads", __name__)


@downloads_bp.get("/downloader/geral")
@require_api_key
def download_general():
    target_url = request.args.get("input")
    if not target_url:
        return error_response(400)

    headers = {
        "x-rapidapi-key": "8e941c6787mshba06793555144d9p16fa99jsn7fb15baa1a2e",
        "x-rapidapi-host": "full-downloader-social-media.p.rapidapi.com",
    }

    try:
        response = requests.get(
            "https://full-downloader-social-media.p.rapidapi.com/",
            headers=headers,
            params={"url": target_url},
            timeout=30,
        )
        response.raise_for_status()
        download_url = response.json().get("download_url")
        return jsonify({"text": download_url}), 200
    except requests.RequestException as exc:  # pragma: no cover - network errors
        return jsonify({"error": "download_failed", "error_desc": str(exc)}), 502


@downloads_bp.get("/temp_image/<path:filename>")
def serve_temp_image(filename: str):
    temp_path = Path("temp_image") / filename
    if not temp_path.exists():
        abort(404)
    return send_file(temp_path, mimetype="image/png")
