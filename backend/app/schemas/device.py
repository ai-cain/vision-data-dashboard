from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from werkzeug.exceptions import BadRequest

from app.models.device import Device, DeviceStatus, DeviceType
from app.models.event import VisionEvent
from app.schemas.common import (
    ensure_mapping,
    isoformat_value,
    parse_optional_datetime,
    parse_required_string,
)


@dataclass(slots=True)
class DeviceCreatePayload:
    name: str
    device_type: DeviceType
    location: str
    status: DeviceStatus


@dataclass(slots=True)
class DeviceStatusUpdatePayload:
    status: DeviceStatus
    last_seen: object | None


def parse_device_create(data: Any) -> DeviceCreatePayload:
    payload = ensure_mapping(data)
    return DeviceCreatePayload(
        name=parse_required_string(payload, "name"),
        device_type=_parse_device_type(payload.get("type")),
        location=parse_required_string(payload, "location"),
        status=_parse_device_status(payload.get("status", DeviceStatus.ONLINE.value)),
    )


def parse_device_status_update(data: Any) -> DeviceStatusUpdatePayload:
    payload = ensure_mapping(data)
    return DeviceStatusUpdatePayload(
        status=_parse_device_status(payload.get("status")),
        last_seen=parse_optional_datetime(payload.get("last_seen"), "last_seen"),
    )


def serialize_device(device: Device) -> dict[str, object]:
    return {
        "id": str(device.id),
        "name": device.name,
        "type": device.type.value,
        "location": device.location,
        "status": device.status.value,
        "last_seen": isoformat_value(device.last_seen),
        "created_at": isoformat_value(device.created_at),
    }


def serialize_device_detail(device: Device, recent_events: list[VisionEvent]) -> dict[str, object]:
    return {
        **serialize_device(device),
        "recent_events": [
            {
                "id": str(event.id),
                "event_type": event.event_type.value,
                "confidence": event.confidence,
                "label": event.label,
                "frame_ts": isoformat_value(event.frame_ts),
                "metadata": event.metadata_payload,
            }
            for event in recent_events
        ],
    }


def _parse_device_type(value: Any) -> DeviceType:
    if not isinstance(value, str):
        raise BadRequest("Field 'type' must be one of: jetson, esp32, raspi")
    try:
        return DeviceType(value.strip().lower())
    except ValueError as error:
        raise BadRequest("Field 'type' must be one of: jetson, esp32, raspi") from error


def _parse_device_status(value: Any) -> DeviceStatus:
    if not isinstance(value, str):
        raise BadRequest("Field 'status' must be one of: online, offline, error")
    try:
        return DeviceStatus(value.strip().lower())
    except ValueError as error:
        raise BadRequest("Field 'status' must be one of: online, offline, error") from error
