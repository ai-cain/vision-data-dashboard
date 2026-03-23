from __future__ import annotations

import click
from flask import Flask
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from app.config import Config
from app.extensions import db, jwt, migrate


def create_app(config_class: type[Config] = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)

    CORS(
        app,
        resources={r"/api/*": {"origins": [app.config["FRONTEND_ORIGIN"]]}},
        supports_credentials=True,
    )

    register_extensions(app)
    register_error_handlers(app)
    register_routes(app)
    register_cli(app)

    @app.get("/health")
    def healthcheck() -> tuple[dict[str, str], int]:
        return {"status": "ok"}, 200

    return app


def register_extensions(app: Flask) -> None:
    from app import models  # noqa: F401

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)


def register_routes(app: Flask) -> None:
    from app.routes.api import api_blueprint

    app.register_blueprint(api_blueprint)


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(HTTPException)
    def handle_http_error(error: HTTPException) -> tuple[dict[str, object], int]:
        return {
            "message": error.description,
            "status": error.code,
        }, error.code or 500

    @app.errorhandler(Exception)
    def handle_unexpected_error(error: Exception) -> tuple[dict[str, object], int]:
        app.logger.exception("Unexpected application error", exc_info=error)
        return {"message": "Internal server error", "status": 500}, 500


def register_cli(app: Flask) -> None:
    from app.services.seed_service import seed_database

    @app.cli.command("seed")
    @click.option("--truncate", is_flag=True, default=False)
    def seed_command(truncate: bool) -> None:
        seed_database(truncate=truncate)
        app.logger.info("Seed data generated")
