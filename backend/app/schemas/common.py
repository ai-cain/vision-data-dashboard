from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Mapping, TypeVar
from uuid import UUID

from marshmallow import Schema, ValidationError, fields
from werkzeug.exceptions import BadRequest


T = TypeVar("T")


def normalize_datetime(value: datetime | None) -> datetime | None:
    if value is None:
        return None
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def isoformat_value(value: datetime | None) -> str | None:
    normalized_value = normalize_datetime(value)
    if normalized_value is None:
        return None
    normalized = normalized_value.replace(microsecond=0)
    return normalized.isoformat().replace("+00:00", "Z")


class UTCDateTime(fields.DateTime):
    def _deserialize(
        self,
        value: Any,
        attr: str | None,
        data: Mapping[str, Any] | None,
        **kwargs: Any,
    ) -> datetime:
        parsed = super()._deserialize(value, attr, data, **kwargs)
        normalized = normalize_datetime(parsed)
        if normalized is None:
            raise ValidationError("Invalid datetime value.")
        return normalized

    def _serialize(
        self,
        value: datetime | None,
        attr: str | None,
        obj: Any,
        **kwargs: Any,
    ) -> str | None:
        return isoformat_value(value)


class EnumValueField(fields.Field):
    def __init__(self, enum_class: type[Enum], *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.enum_class = enum_class

    def _deserialize(
        self,
        value: Any,
        attr: str | None,
        data: Mapping[str, Any] | None,
        **kwargs: Any,
    ) -> Enum:
        if not isinstance(value, str):
            raise ValidationError(self._choices_message())

        candidate = value.strip().lower()
        for enum_value in self.enum_class:
            if enum_value.value == candidate:
                return enum_value
        raise ValidationError(self._choices_message())

    def _serialize(
        self,
        value: Enum | str | None,
        attr: str | None,
        obj: Any,
        **kwargs: Any,
    ) -> str | None:
        if value is None:
            return None
        if isinstance(value, Enum):
            return str(value.value)
        return str(value)

    def _choices_message(self) -> str:
        options = ", ".join(str(item.value) for item in self.enum_class)
        return f"Must be one of: {options}"


def load_or_abort(schema: Schema, data: Any) -> Any:
    try:
        return schema.load(data)
    except ValidationError as error:
        raise BadRequest(_format_validation_error(error.messages)) from error


def parse_uuid_value(value: str, key: str) -> UUID:
    try:
        return UUID(str(value))
    except ValueError as error:
        raise BadRequest(f"Field '{key}' must be a valid UUID") from error


def dump_with_schema(schema: Schema, obj: Any) -> dict[str, Any]:
    return schema.dump(obj)


def dump_many_with_schema(schema: Schema, items: list[Any]) -> list[dict[str, Any]]:
    return schema.dump(items)


def _format_validation_error(messages: dict[str, Any] | list[Any] | str) -> str:
    if isinstance(messages, str):
        return messages
    if isinstance(messages, list):
        return "; ".join(_format_validation_error(item) for item in messages)

    flattened: list[str] = []
    for key, value in messages.items():
        if isinstance(value, list):
            flattened.extend(f"{key}: {_format_validation_error(item)}" for item in value)
        elif isinstance(value, dict):
            nested = _format_validation_error(value)
            flattened.append(f"{key}: {nested}")
        else:
            flattened.append(f"{key}: {value}")
    return "; ".join(flattened)
