from __future__ import annotations

import click
from flask import Flask
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from app.config import Config
from app.extensions import db, jwt, migrate, sock


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
    sock.init_app(app)
    register_jwt_handlers()


def register_routes(app: Flask) -> None:
    from app.routes.api import api_blueprint
    from app.routes.stream import register_stream_routes

    app.register_blueprint(api_blueprint)
    register_stream_routes(app)


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


def register_jwt_handlers() -> None:
    @jwt.expired_token_loader
    def handle_expired_token(
        jwt_header: dict[str, object],
        jwt_payload: dict[str, object],
    ) -> tuple[dict[str, object], int]:
        return {"message": "JWT has expired", "status": 401}, 401

    @jwt.invalid_token_loader
    def handle_invalid_token(error: str) -> tuple[dict[str, object], int]:
        return {"message": f"Invalid JWT: {error}", "status": 401}, 401

    @jwt.unauthorized_loader
    def handle_missing_token(error: str) -> tuple[dict[str, object], int]:
        return {"message": error, "status": 401}, 401

    @jwt.revoked_token_loader
    def handle_revoked_token(
        jwt_header: dict[str, object],
        jwt_payload: dict[str, object],
    ) -> tuple[dict[str, object], int]:
        return {"message": "JWT has been revoked", "status": 401}, 401


def register_cli(app: Flask) -> None:
    from app.services.db_admin_service import (
        create_database,
        delete_database,
        reset_database,
    )
    from app.services.seed_service import seed_database

    @app.cli.command("db-create")
    @click.option("--migrate/--no-migrate", default=True)
    @click.option("--seed/--no-seed", default=False)
    def db_create_command(migrate: bool, seed: bool) -> None:
        created = create_database(migrate=migrate, seed=seed)
        if created:
            app.logger.info("Database created successfully")
        else:
            app.logger.info("Database already exists")

    @app.cli.command("db-reset")
    @click.option("--seed/--no-seed", default=True)
    @click.option("--yes-i-know", is_flag=True, default=False)
    def db_reset_command(seed: bool, yes_i_know: bool) -> None:
        if not yes_i_know:
            raise click.ClickException("Pass --yes-i-know to reset the PostgreSQL database.")
        reset_database(seed=seed)
        app.logger.info("Database reset completed")

    @app.cli.command("db-delete")
    @click.option("--yes-i-know", is_flag=True, default=False)
    def db_delete_command(yes_i_know: bool) -> None:
        if not yes_i_know:
            raise click.ClickException("Pass --yes-i-know to delete the PostgreSQL database.")
        deleted = delete_database()
        if deleted:
            app.logger.info("Database deleted successfully")
        else:
            app.logger.info("Database did not exist")

    @app.cli.command("seed")
    @click.option("--truncate", is_flag=True, default=False)
    def seed_command(truncate: bool) -> None:
        seed_database(truncate=truncate)
        app.logger.info("Seed data generated")
