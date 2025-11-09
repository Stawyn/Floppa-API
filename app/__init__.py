"""Application factory for the Flask service."""
from __future__ import annotations

from pathlib import Path

from flask import Flask

from .config import Config
from .extensions import limiter
from .routes import register_routes
from .utils.logging import configure_logging
from .utils.storage import ensure_file_exists


def create_app(config_object: type[Config] | None = None) -> Flask:
    """Application factory used by the WSGI entry points."""
    app = Flask(__name__)
    app.config.from_object(config_object or Config)

    configure_logging(app)
    limiter.init_app(app)
    register_routes(app)

    # Ensure required files exist so the application can operate.
    ensure_file_exists(Path(app.config["DATABASE_FM"]))
    ensure_file_exists(Path(app.config["LAST_GAME_ID_FILE"]))

    @app.get("/")
    def root() -> tuple[dict[str, str], int]:
        return {"error": "Diretorio Invalido"}, 404

    return app


app = create_app()
