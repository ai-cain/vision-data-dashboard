from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Mapping
from uuid import UUID

from werkzeug.exceptions import BadRequest


def ensure_mapping(data: Any) -> Mapping[str, Any]:
    if not isinstance(data, Mapping):
        raise BadRequest("Request body must be a JSON object")
    return data


def parse_required_string(data: Mapping[str, Any], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise BadRequest(f"Field '{key}' is required")
    return value.strip()


def parse_optional_string(data: Mapping[str, Any], key: str) -> str | None:
    value = data.get(key)
    if value is None:
        return None
    if not isinstance(value, str):
        raise BadRequest(f"Field '{key}' must be a string")
    cleaned = value.strip()
    return cleaned or None


def parse_float_value(data: Mapping[str, Any], key: str) -> float:
    raw_value = data.get(key)
    if raw_value is None:
        raise BadRequest(f"Field '{key}' is required")
    try:
        value = float(raw_value)
    except (TypeError, ValueError) as error:
        raise BadRequest(f"Field '{key}' must be a number") from error
    return value


def parse_integer_value(
    value: Any,
    key: str,
    *,
    default: int | None = None,
    minimum: int | None = None,
    maximum: int | None = None,
) -> int:
    if value in (None, ""):
        if default is None:
            raise BadRequest(f"Field '{key}' is required")
        return default
    try:
        parsed = int(value)
    except (TypeError, ValueError) as error:
        raise BadRequest(f"Field '{key}' must be an integer") from error

    if minimum is not None and parsed < minimum:
        raise BadRequest(f"Field '{key}' must be at least {minimum}")
    if maximum is not None and parsed > maximum:
        raise BadRequest(f"Field '{key}' must be at most {maximum}")
    return parsed


def parse_uuid_value(value: str, key: str) -> UUID:
    try:
        return UUID(str(value))
    except ValueError as error:
        raise BadRequest(f"Field '{key}' must be a valid UUID") from error


def parse_datetime_value(value: Any, key: str) -> datetime:
    if not isinstance(value, str) or not value.strip():
        raise BadRequest(f"Field '{key}' must be an ISO datetime string")

    normalized = value.strip().replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as error:
        raise BadRequest(f"Field '{key}' must be an ISO datetime string") from error

    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)

    return parsed.astimezone(timezone.utc)


def parse_optional_datetime(value: Any, key: str) -> datetime | None:
    if value in (None, ""):
        return None
    return parse_datetime_value(value, key)


def isoformat_value(value: datetime | None) -> str | None:
    if value is None:
        return None
    normalized = value.astimezone(timezone.utc).replace(microsecond=0)
    return normalized.isoformat().replace("+00:00", "Z")
