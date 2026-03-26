from __future__ import annotations

import os
from datetime import timedelta


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


def _build_admin_api_keys() -> tuple[str, ...]:
    explicit_keys = os.environ.get("ADMIN_API_KEYS")
    if explicit_keys:
        parsed = tuple(dict.fromkeys(item.strip() for item in explicit_keys.split(",") if item.strip()))
        if parsed:
            return parsed

    fallback = os.environ.get("ADMIN_API_KEY", "local-dev-key").strip()
    return (fallback,) if fallback else ("local-dev-key",)


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-me")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "change-me-too")
    ADMIN_API_KEYS = _build_admin_api_keys()
    ADMIN_API_KEY = ADMIN_API_KEYS[0]
    AUTH_REQUIRED = os.environ.get("AUTH_REQUIRED", "false").lower() == "true"
    AUTH_ALLOW_LOCAL_BYPASS = os.environ.get("AUTH_ALLOW_LOCAL_BYPASS", "true").lower() == "true"
    SQLALCHEMY_DATABASE_URI = _build_database_url()
    POSTGRES_ADMIN_DB = os.environ.get("POSTGRES_ADMIN_DB", "postgres")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RESTX_MASK_SWAGGER = False
    RESTX_ERROR_404_HELP = False
    JSON_SORT_KEYS = False
    API_TITLE = "Vision Data Dashboard API"
    API_VERSION = "1.0"
    API_PREFIX = "/api/v1"
    SWAGGER_UI_DOC_EXPANSION = "list"
    FRONTEND_ORIGIN = os.environ.get("FRONTEND_ORIGIN", "http://localhost:5173")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        minutes=int(os.environ.get("JWT_ACCESS_TOKEN_EXPIRES_MINUTES", "60"))
    )
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_ENCODE_ISSUER = os.environ.get("JWT_ISSUER", "vision-data-dashboard")
    JWT_DECODE_ISSUER = os.environ.get("JWT_ISSUER", "vision-data-dashboard")
    JWT_ENCODE_AUDIENCE = os.environ.get("JWT_AUDIENCE", "vision-dashboard-clients")
    JWT_DECODE_AUDIENCE = os.environ.get("JWT_AUDIENCE", "vision-dashboard-clients")
