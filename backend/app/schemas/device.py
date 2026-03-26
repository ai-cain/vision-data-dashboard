from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from marshmallow import Schema, fields, post_load, validate

from app.models.device import Device, DeviceStatus, DeviceType
from app.models.event import EventType, VisionEvent
from app.schemas.common import (
    UTCDateTime,
    EnumValueField,
    dump_many_with_schema,
    dump_with_schema,
    load_or_abort,
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
    last_seen: datetime | None


class DeviceCreateSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1))
    device_type = EnumValueField(DeviceType, required=True, data_key="type")
    location = fields.Str(required=True, validate=validate.Length(min=1))
    status = EnumValueField(DeviceStatus, load_default=DeviceStatus.ONLINE.value)

    @post_load
    def make_payload(self, data: dict[str, Any], **kwargs: Any) -> DeviceCreatePayload:
        return DeviceCreatePayload(**data)


class DeviceStatusUpdateSchema(Schema):
    status = EnumValueField(DeviceStatus, required=True)
    last_seen = UTCDateTime(load_default=None, allow_none=True)

    @post_load
    def make_payload(self, data: dict[str, Any], **kwargs: Any) -> DeviceStatusUpdatePayload:
        return DeviceStatusUpdatePayload(**data)


class RecentEventSchema(Schema):
    id = fields.UUID()
    event_type = EnumValueField(EventType)
    confidence = fields.Float()
    label = fields.Str()
    frame_ts = UTCDateTime()
    metadata = fields.Dict(attribute="metadata_payload")


class DeviceResponseSchema(Schema):
    id = fields.UUID()
    name = fields.Str()
    type = EnumValueField(DeviceType, attribute="type")
    location = fields.Str()
    status = EnumValueField(DeviceStatus)
    last_seen = UTCDateTime()
    created_at = UTCDateTime()


device_create_schema = DeviceCreateSchema()
device_status_update_schema = DeviceStatusUpdateSchema()
device_response_schema = DeviceResponseSchema()
device_response_list_schema = DeviceResponseSchema(many=True)
recent_event_list_schema = RecentEventSchema(many=True)


def parse_device_create(data: Any) -> DeviceCreatePayload:
    return load_or_abort(device_create_schema, data)


def parse_device_status_update(data: Any) -> DeviceStatusUpdatePayload:
    return load_or_abort(device_status_update_schema, data)


def serialize_device(device: Device) -> dict[str, object]:
    return dump_with_schema(device_response_schema, device)


def serialize_devices(devices: list[Device]) -> list[dict[str, object]]:
    return dump_many_with_schema(device_response_list_schema, devices)


def serialize_device_detail(device: Device, recent_events: list[VisionEvent]) -> dict[str, object]:
    payload = serialize_device(device)
    payload["recent_events"] = dump_many_with_schema(recent_event_list_schema, recent_events)
    return payload
