from __future__ import annotations

from flask import current_app, request
from flask_jwt_extended import create_access_token, verify_jwt_in_request
from werkzeug.exceptions import Unauthorized


def issue_access_token(api_key: str) -> str:
    expected = current_app.config["ADMIN_API_KEY"]
    if api_key != expected:
        raise Unauthorized("Invalid API key")
    return create_access_token(identity="dashboard-admin")


def enforce_write_access() -> None:
    if not current_app.config["AUTH_REQUIRED"]:
        return

    header_key = request.headers.get("X-API-Key")
    if header_key and header_key == current_app.config["ADMIN_API_KEY"]:
        return

    try:
        verify_jwt_in_request()
    except Exception as error:  # noqa: BLE001
        raise Unauthorized("Write access requires a valid JWT or X-API-Key header") from error
