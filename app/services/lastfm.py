"""Utilities for interacting with the Last.fm API and local mapping."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

import requests
from flask import current_app

from app.utils.time import formatted_brazil_time


class LastFMError(RuntimeError):
    """Raised when an interaction with the Last.fm API fails."""


def _database_path() -> Path:
    return Path(current_app.config["DATABASE_FM"])


def load_registry() -> list[dict[str, str]]:
    path = _database_path()
    if not path.exists() or path.stat().st_size == 0:
        return []
    with path.open("r", encoding="utf8") as handle:
        try:
            return json.load(handle)
        except json.JSONDecodeError:
            return []


def save_registry(entries: Iterable[dict[str, str]]) -> None:
    path = _database_path()
    with path.open("w", encoding="utf8") as handle:
        json.dump(list(entries), handle, ensure_ascii=False)


def upsert_user(phone_number: str, username: str) -> None:
    entries = load_registry()
    for entry in entries:
        if entry["phone_number"] == phone_number:
            entry.update({"user": username, "last_change": formatted_brazil_time()})
            break
    else:
        entries.append(
            {
                "phone_number": phone_number,
                "user": username,
                "last_change": formatted_brazil_time(),
            }
        )
    save_registry(entries)


def lookup_user(phone_number: str) -> str | None:
    entries = load_registry()
    for entry in entries:
        if entry.get("phone_number") == phone_number:
            return entry.get("user")
    return None


def call_lastfm(method: str, **params: Any) -> dict[str, Any]:
    payload = {
        "api_key": current_app.config.get("LASTFM_API_KEY"),
        "format": "json",
        **params,
    }
    response = requests.get(
        "https://ws.audioscrobbler.com/2.0/",
        params={"method": method, **payload},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def get_recent_track(username: str) -> dict[str, Any] | None:
    data = call_lastfm("user.getrecenttracks", user=username, limit=1)
    tracks = data.get("recenttracks", {}).get("track", [])
    return tracks[0] if tracks else None


def get_top_albums(username: str) -> list[dict[str, Any]]:
    data = call_lastfm("user.gettopalbums", user=username)
    return data.get("topalbums", {}).get("album", [])


def get_top_tracks(username: str) -> list[dict[str, Any]]:
    data = call_lastfm("user.gettoptracks", user=username)
    return data.get("toptracks", {}).get("track", [])


def get_top_artists(username: str) -> list[dict[str, Any]]:
    data = call_lastfm("user.gettopartists", user=username)
    return data.get("topartists", {}).get("artist", [])


def get_track_info(username: str, artist: str, track: str) -> dict[str, Any]:
    return call_lastfm("track.getInfo", user=username, artist=artist, track=track).get("track", {})
