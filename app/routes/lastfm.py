"""Routes for interacting with Last.fm."""
from __future__ import annotations

from typing import Any

import requests
from flask import Blueprint, jsonify, request

from app.services import lastfm
from app.utils.auth import require_api_key
from app.utils.errors import error_response


lastfm_bp = Blueprint("lastfm", __name__, url_prefix="/fm")


def _username_from_number(number: str | None) -> str | None:
    return lastfm.lookup_user(number) if number else None


def _resolve_username() -> tuple[str | None, tuple[Any, int] | None]:
    number = request.args.get("number")
    username = _username_from_number(number)
    if not username:
        username = request.args.get("user")

    if not username:
        status = 404 if number else 400
        return None, error_response(status)

    return username, None


@lastfm_bp.get("/register")
@require_api_key
def register_user() -> tuple[Any, int]:
    username = request.args.get("user")
    phone_number = request.args.get("number")
    if not username or not phone_number:
        return error_response(400)

    phone_number = phone_number.replace("@s.whatsapp.net", "")
    lastfm.upsert_user(phone_number, username)
    return error_response(200)


@lastfm_bp.get("/album")
@require_api_key
def album() -> tuple[Any, int]:
    number = request.args.get("number")
    if not number:
        return error_response(400)

    username = _username_from_number(number)
    if not username:
        return error_response(404)

    try:
        recent = lastfm.get_recent_track(username)
        if not recent:
            return error_response(404)

        album_name = recent.get("album", {}).get("#text")
        top_albums = lastfm.get_top_albums(username)
        playcount = next(
            (item.get("playcount") for item in top_albums if item.get("name") == album_name),
            "0",
        )
        image_url = (recent.get("image") or [{}])[-1].get("#text", "")
        payload = {
            "album": album_name,
            "playcount": playcount,
            "image_url": image_url,
        }
        return jsonify(payload), 200
    except requests.RequestException:  # pragma: no cover - network errors
        return error_response(404)


@lastfm_bp.get("/top/album")
@require_api_key
def top_albums() -> tuple[Any, int]:
    number = request.args.get("number")
    if not number:
        return error_response(400)

    username = _username_from_number(number)
    if not username:
        return error_response(404)

    try:
        albums = lastfm.get_top_albums(username)
    except requests.RequestException:  # pragma: no cover
        return error_response(404)

    payload = []
    for index, album in enumerate(albums[:5]):
        payload.append(
            {
                "top": index,
                "track": album.get("name"),
                "artist": album.get("artist", {}).get("name"),
                "album": album.get("name"),
                "playcount": album.get("playcount"),
            }
        )
    return jsonify(payload), 200


@lastfm_bp.get("/top/track")
@require_api_key
def top_tracks() -> tuple[Any, int]:
    number = request.args.get("number")
    if not number:
        return error_response(400)

    username = _username_from_number(number)
    if not username:
        return error_response(404)

    try:
        tracks = lastfm.get_top_tracks(username)
    except requests.RequestException:  # pragma: no cover
        return error_response(404)

    payload = []
    for index, track in enumerate(tracks[:5]):
        payload.append(
            {
                "top": index,
                "track": track.get("name"),
                "artist": track.get("artist", {}).get("name"),
                "playcount": track.get("playcount"),
            }
        )
    return jsonify(payload), 200


@lastfm_bp.get("/top/artist")
@require_api_key
def top_artists() -> tuple[Any, int]:
    number = request.args.get("number")
    if not number:
        return error_response(400)

    username = _username_from_number(number)
    if not username:
        return error_response(404)

    try:
        artists = lastfm.get_top_artists(username)
    except requests.RequestException:  # pragma: no cover
        return error_response(404)

    payload = []
    for index, artist in enumerate(artists[:5]):
        payload.append(
            {
                "top": index,
                "artist": artist.get("name"),
                "playcount": artist.get("playcount"),
            }
        )
    return jsonify(payload), 200


@lastfm_bp.get("/artist")
@require_api_key
def artist() -> tuple[Any, int]:
    number = request.args.get("number")
    if not number:
        return error_response(400)

    username = _username_from_number(number)
    if not username:
        return error_response(404)

    try:
        recent = lastfm.get_recent_track(username)
        if not recent:
            return error_response(404)
        artist_name = recent.get("artist", {}).get("#text")
        artists = lastfm.get_top_artists(username)
        playcount = next(
            (item.get("playcount") for item in artists if item.get("name") == artist_name),
            "0",
        )
        image_url = (recent.get("image") or [{}])[-1].get("#text", "")
        payload = {
            "artist": artist_name,
            "playcount": playcount,
            "image_url": image_url,
        }
        return jsonify(payload), 200
    except requests.RequestException:  # pragma: no cover
        return error_response(404)


@lastfm_bp.get("/recent")
@require_api_key
def recent() -> tuple[Any, int]:
    username, error = _resolve_username()
    if error:
        return error

    try:
        track = lastfm.get_recent_track(username)
        if not track:
            return error_response(404)

        track_name = track.get("name")
        artist_name = track.get("artist", {}).get("#text")
        album_name = track.get("album", {}).get("#text")
        now_playing = track.get("@attr", {}).get("nowplaying", "false") == "true"
        image_url = (track.get("image") or [{}])[-1].get("#text", "")

        track_info = lastfm.get_track_info(username, artist_name, track_name)
        playcount = track_info.get("userplaycount", "0")

        payload = {
            "track_name": track_name,
            "artist": artist_name,
            "album": album_name,
            "playcount": playcount,
            "now_playing": now_playing,
            "image_url": image_url,
        }
        return jsonify(payload), 200
    except requests.RequestException:  # pragma: no cover
        return error_response(500)
