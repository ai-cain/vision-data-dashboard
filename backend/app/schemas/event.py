from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Mapping
from uuid import UUID

from werkzeug.exceptions import BadRequest

from app.models.event import EventType, VisionEvent
from app.schemas.common import (
    ensure_mapping,
    isoformat_value,
    parse_datetime_value,
    parse_float_value,
    parse_integer_value,
    parse_optional_datetime,
    parse_optional_string,
    parse_required_string,
    parse_uuid_value,
)


@dataclass(slots=True)
class EventCreatePayload:
    device_id: UUID
    event_type: EventType
    confidence: float
    label: str
    frame_ts: datetime
    metadata_payload: dict[str, Any]


@dataclass(slots=True)
class EventFilters:
    page: int
    per_page: int
    device_id: UUID | None
    event_type: EventType | None
    start_date: datetime | None
    end_date: datetime | None


def parse_event_create(data: Any) -> EventCreatePayload:
    payload = ensure_mapping(data)
    metadata_payload = payload.get("metadata", {})
    if not isinstance(metadata_payload, Mapping):
        raise BadRequest("Field 'metadata' must be a JSON object")

    confidence = parse_float_value(payload, "confidence")
    if confidence < 0 or confidence > 1:
        raise BadRequest("Field 'confidence' must be between 0 and 1")

    return EventCreatePayload(
        device_id=parse_uuid_value(parse_required_string(payload, "device_id"), "device_id"),
        event_type=_parse_event_type(payload.get("event_type")),
        confidence=confidence,
        label=parse_required_string(payload, "label"),
        frame_ts=parse_datetime_value(payload.get("frame_ts"), "frame_ts"),
        metadata_payload=dict(metadata_payload),
    )


def parse_event_filters(data: Mapping[str, Any]) -> EventFilters:
    device_id = parse_optional_string(data, "device")
    return EventFilters(
        page=parse_integer_value(data.get("page"), "page", default=1, minimum=1),
        per_page=parse_integer_value(data.get("per_page"), "per_page", default=25, minimum=1, maximum=100),
        device_id=parse_uuid_value(device_id, "device") if device_id else None,
        event_type=_parse_optional_event_type(data.get("type")),
        start_date=parse_optional_datetime(data.get("start_date"), "start_date"),
        end_date=parse_optional_datetime(data.get("end_date"), "end_date"),
    )


def serialize_event(event: VisionEvent) -> dict[str, object]:
    return {
        "id": str(event.id),
        "device_id": str(event.device_id),
        "device_name": event.device.name if event.device else None,
        "event_type": event.event_type.value,
        "confidence": event.confidence,
        "label": event.label,
        "frame_ts": isoformat_value(event.frame_ts),
        "metadata": event.metadata_payload,
        "created_at": isoformat_value(event.created_at),
    }


def _parse_event_type(value: Any) -> EventType:
    if not isinstance(value, str):
        raise BadRequest("Field 'event_type' must be one of: detection, anomaly, count")
    try:
        return EventType(value.strip().lower())
    except ValueError as error:
        raise BadRequest("Field 'event_type' must be one of: detection, anomaly, count") from error


def _parse_optional_event_type(value: Any) -> EventType | None:
    if value in (None, ""):
        return None
    return _parse_event_type(value)
