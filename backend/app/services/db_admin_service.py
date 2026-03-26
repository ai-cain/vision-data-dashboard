from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from alembic import command
from alembic.config import Config as AlembicConfig
from flask import current_app
from psycopg import connect, sql
from sqlalchemy.engine import URL, make_url

from app.extensions import db
from app.services.seed_service import seed_database


@dataclass(frozen=True, slots=True)
class DatabaseAdminUrls:
    target_url: URL
    admin_url: URL


def create_database(*, migrate: bool = True, seed: bool = False) -> bool:
    urls = _build_admin_urls()
    database_name = _target_database_name(urls)

    _dispose_current_engine()

    with connect(urls.admin_url.render_as_string(hide_password=False), autocommit=True) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (database_name,))
            exists = cursor.fetchone() is not None
            if not exists:
                cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(database_name)))

    if migrate:
        upgrade_database_schema()
    if seed:
        seed_database(truncate=False)

    return not exists


def delete_database() -> bool:
    urls = _build_admin_urls()
    database_name = _target_database_name(urls)

    _dispose_current_engine()

    with connect(urls.admin_url.render_as_string(hide_password=False), autocommit=True) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (database_name,))
            exists = cursor.fetchone() is not None
            if not exists:
                return False

            cursor.execute(
                """
                SELECT pg_terminate_backend(pid)
                FROM pg_stat_activity
                WHERE datname = %s
                  AND pid <> pg_backend_pid()
                """,
                (database_name,),
            )
            cursor.execute(sql.SQL("DROP DATABASE {}").format(sql.Identifier(database_name)))

    return True


def reset_database(*, seed: bool = True) -> None:
    delete_database()
    create_database(migrate=True, seed=seed)


def upgrade_database_schema() -> None:
    alembic_config = _build_alembic_config()
    command.upgrade(alembic_config, "head")


def _build_admin_urls() -> DatabaseAdminUrls:
    target_url = make_url(current_app.config["SQLALCHEMY_DATABASE_URI"])
    if not target_url.drivername.startswith("postgresql"):
        raise RuntimeError("Database admin commands only support PostgreSQL targets.")

    admin_url = target_url.set(
        drivername="postgresql",
        database=current_app.config["POSTGRES_ADMIN_DB"],
    )
    return DatabaseAdminUrls(target_url=target_url, admin_url=admin_url)


def _target_database_name(urls: DatabaseAdminUrls) -> str:
    if not urls.target_url.database:
        raise RuntimeError("Target database name is missing from SQLALCHEMY_DATABASE_URI.")
    return urls.target_url.database


def _build_alembic_config() -> AlembicConfig:
    backend_root = Path(__file__).resolve().parents[2]
    alembic_config = AlembicConfig(str(backend_root / "alembic.ini"))
    alembic_config.set_main_option("script_location", str(backend_root / "migrations"))
    alembic_config.set_main_option("sqlalchemy.url", current_app.config["SQLALCHEMY_DATABASE_URI"])
    return alembic_config


def _dispose_current_engine() -> None:
    db.session.remove()
    db.engine.dispose()
