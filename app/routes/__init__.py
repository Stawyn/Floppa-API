"""Blueprint registration."""
from __future__ import annotations

from flask import Flask

from .alerts import alerts_bp
from .ai import ai_bp
from .downloads import downloads_bp
from .lastfm import lastfm_bp


def register_routes(app: Flask) -> None:
    app.register_blueprint(alerts_bp)
    app.register_blueprint(ai_bp)
    app.register_blueprint(downloads_bp)
    app.register_blueprint(lastfm_bp)
