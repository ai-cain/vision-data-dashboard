from __future__ import annotations

import os


def _build_database_url() -> str:
    explicit_url = os.environ.get("DATABASE_URL")
    if explicit_url:
        return explicit_url

    user = os.environ.get("POSTGRES_USER", "vision")
    password = os.environ.get("POSTGRES_PASSWORD", "vision")
    host = os.environ.get("POSTGRES_HOST", "localhost")
    port = os.environ.get("POSTGRES_PORT", "5432")
    database = os.environ.get("POSTGRES_DB", "vision_dashboard")
    return f"postgresql+psycopg://{user}:{password}@{host}:{port}/{database}"


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-me")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "change-me-too")
    ADMIN_API_KEY = os.environ.get("ADMIN_API_KEY", "local-dev-key")
    AUTH_REQUIRED = os.environ.get("AUTH_REQUIRED", "false").lower() == "true"
    SQLALCHEMY_DATABASE_URI = _build_database_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RESTX_MASK_SWAGGER = False
    ERROR_404_HELP = False
    JSON_SORT_KEYS = False
    API_TITLE = "Vision Data Dashboard API"
    API_VERSION = "1.0"
    API_PREFIX = "/api/v1"
    SWAGGER_UI_DOC_EXPANSION = "list"
    FRONTEND_ORIGIN = os.environ.get("FRONTEND_ORIGIN", "http://localhost:5173")
