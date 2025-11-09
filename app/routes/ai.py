"""AI related routes."""
from __future__ import annotations

import asyncio
from typing import Any

from flask import Blueprint, current_app, jsonify, request
from PyCharacterAI import Client

from app.services.gpt import gpt_input
from app.utils.auth import require_api_key
from app.utils.errors import error_response


ai_bp = Blueprint("ai", __name__)


def _required_arg(name: str) -> str | None:
    value = request.args.get(name)
    return value.strip() if value else None


@ai_bp.get("/ai/floppa")
@require_api_key
def ai_floppa() -> tuple[Any, int]:
    message = _required_arg("input")
    if not message:
        return error_response(400)

    try:
        client = Client()
        asyncio.run(client.authenticate_with_token(current_app.config["CHARACTER_AI_TOKEN"]))
        chat = asyncio.run(client.create_or_continue_chat(current_app.config["CHARACTER_ID"]))
        response = asyncio.run(chat.send_message(message))
        text = response.text
        return jsonify({"text": text}), 200
    except Exception:  # pragma: no cover - external service
        return error_response(408)


@ai_bp.get("/ai/gpt4")
@require_api_key
def ai_gpt4() -> tuple[Any, int]:
    message = _required_arg("input")
    if not message:
        return error_response(400)
    return jsonify({"text": gpt_input(message, "text")}), 200


