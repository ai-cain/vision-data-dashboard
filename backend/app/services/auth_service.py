from __future__ import annotations

import hmac
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from flask import current_app, request
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, verify_jwt_in_request
from werkzeug.exceptions import Unauthorized


WRITE_SCOPE = "dashboard:write"


@dataclass(slots=True)
class AuthContext:
    authenticated: bool
    auth_required: bool
    principal: str
    auth_method: str
    scopes: tuple[str, ...]
    expires_at: datetime | None = None


@dataclass(slots=True)
class IssuedToken:
    access_token: str
    token_type: str
    expires_at: datetime
    expires_in_seconds: int
    principal: str
    scopes: tuple[str, ...]


def issue_access_token(api_key: str) -> IssuedToken:
    if not is_valid_api_key(api_key):
        raise Unauthorized("Invalid API key")

    expires_delta = _access_token_expires()
    expires_at = datetime.now(timezone.utc) + expires_delta
    scopes = (WRITE_SCOPE,)
    token = create_access_token(
        identity="dashboard-admin",
        additional_claims={
            "scope": " ".join(scopes),
            "auth_method": "api_key",
            "role": "dashboard-admin",
        },
        expires_delta=expires_delta,
    )
    return IssuedToken(
        access_token=token,
        token_type="Bearer",
        expires_at=expires_at,
        expires_in_seconds=int(expires_delta.total_seconds()),
        principal="dashboard-admin",
        scopes=scopes,
    )


def get_request_auth_context(optional: bool = False) -> AuthContext:
    header_key = request.headers.get("X-API-Key")
    if is_valid_api_key(header_key):
        return AuthContext(
            authenticated=True,
            auth_required=bool(current_app.config["AUTH_REQUIRED"]),
            principal="dashboard-admin",
            auth_method="api-key",
            scopes=(WRITE_SCOPE,),
        )

    if _local_bypass_enabled():
        return AuthContext(
            authenticated=True,
            auth_required=False,
            principal="local-dev",
            auth_method="local-bypass",
            scopes=(WRITE_SCOPE,),
        )

    try:
        verify_jwt_in_request(optional=optional)
    except Exception as error:  # noqa: BLE001
        raise Unauthorized("Write access requires a valid JWT or X-API-Key header") from error

    identity = get_jwt_identity()
    claims = get_jwt()
    if identity is None:
        if optional:
            return AuthContext(
                authenticated=False,
                auth_required=bool(current_app.config["AUTH_REQUIRED"]),
                principal="anonymous",
                auth_method="anonymous",
                scopes=tuple(),
            )
        raise Unauthorized("JWT identity is missing")

    return AuthContext(
        authenticated=True,
        auth_required=bool(current_app.config["AUTH_REQUIRED"]),
        principal=str(identity),
        auth_method=str(claims.get("auth_method", "jwt")),
        scopes=_parse_scopes(claims.get("scope")),
        expires_at=_timestamp_to_datetime(claims.get("exp")),
    )


def enforce_write_access() -> AuthContext:
    if not current_app.config["AUTH_REQUIRED"] and not _local_bypass_enabled():
        return AuthContext(
            authenticated=False,
            auth_required=False,
            principal="anonymous",
            auth_method="anonymous",
            scopes=tuple(),
        )

    context = get_request_auth_context(optional=False)
    if context.auth_method == "jwt" and WRITE_SCOPE not in context.scopes:
        raise Unauthorized("JWT is missing dashboard:write scope")
    return context


def is_valid_api_key(candidate: str | None) -> bool:
    if not candidate:
        return False
    return any(hmac.compare_digest(candidate, configured) for configured in _configured_api_keys())


def _configured_api_keys() -> tuple[str, ...]:
    configured = current_app.config.get("ADMIN_API_KEYS")
    keys: list[str] = []
    if isinstance(configured, tuple):
        keys.extend(str(item) for item in configured if str(item))
    elif isinstance(configured, list):
        keys.extend(str(item) for item in configured if str(item))

    legacy = current_app.config.get("ADMIN_API_KEY")
    if legacy:
        legacy_value = str(legacy)
        if legacy_value not in keys:
            keys.append(legacy_value)

    return tuple(keys)


def _parse_scopes(raw_scope: object) -> tuple[str, ...]:
    if not isinstance(raw_scope, str):
        return tuple()
    return tuple(part for part in raw_scope.split() if part)


def _access_token_expires() -> timedelta:
    expires_delta = current_app.config.get("JWT_ACCESS_TOKEN_EXPIRES")
    if isinstance(expires_delta, timedelta):
        return expires_delta
    return timedelta(minutes=60)


def _local_bypass_enabled() -> bool:
    return not current_app.config["AUTH_REQUIRED"] and bool(current_app.config["AUTH_ALLOW_LOCAL_BYPASS"])


def _timestamp_to_datetime(timestamp: object) -> datetime | None:
    if not isinstance(timestamp, (int, float)):
        return None
    return datetime.fromtimestamp(timestamp, tz=timezone.utc)
