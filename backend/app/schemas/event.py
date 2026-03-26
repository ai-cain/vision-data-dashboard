from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import UUID

from marshmallow import Schema, fields, post_load, validate, validates_schema
from marshmallow.exceptions import ValidationError

from app.models.event import EventType, VisionEvent
from app.schemas.common import (
    UTCDateTime,
    EnumValueField,
    dump_many_with_schema,
    dump_with_schema,
    load_or_abort,
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


class EventCreateSchema(Schema):
    device_id = fields.UUID(required=True)
    event_type = EnumValueField(EventType, required=True)
    confidence = fields.Float(required=True, validate=validate.Range(min=0, max=1))
    label = fields.Str(required=True, validate=validate.Length(min=1))
    frame_ts = UTCDateTime(required=True)
    metadata_payload = fields.Dict(
        load_default=dict,
        dump_default=dict,
        data_key="metadata",
        attribute="metadata_payload",
    )

    @post_load
    def make_payload(self, data: dict[str, Any], **kwargs: Any) -> EventCreatePayload:
        return EventCreatePayload(**data)


class EventFilterSchema(Schema):
    page = fields.Int(load_default=1, validate=validate.Range(min=1))
    per_page = fields.Int(load_default=25, validate=validate.Range(min=1, max=100))
    device_id = fields.UUID(load_default=None, allow_none=True, data_key="device")
    event_type = EnumValueField(EventType, load_default=None, allow_none=True, data_key="type")
    start_date = UTCDateTime(load_default=None, allow_none=True)
    end_date = UTCDateTime(load_default=None, allow_none=True)

    @validates_schema
    def validate_range(self, data: dict[str, Any], **kwargs: Any) -> None:
        start_date = data.get("start_date")
        end_date = data.get("end_date")
        if start_date is not None and end_date is not None and start_date > end_date:
            raise ValidationError("start_date must be earlier than or equal to end_date")

    @post_load
    def make_payload(self, data: dict[str, Any], **kwargs: Any) -> EventFilters:
        return EventFilters(**data)


class EventResponseSchema(Schema):
    id = fields.UUID()
    device_id = fields.UUID()
    device_name = fields.Method("get_device_name")
    event_type = EnumValueField(EventType)
    confidence = fields.Float()
    label = fields.Str()
    frame_ts = UTCDateTime()
    metadata = fields.Dict(attribute="metadata_payload")
    created_at = UTCDateTime()

    def get_device_name(self, obj: VisionEvent) -> str | None:
        return obj.device.name if obj.device else None


event_create_schema = EventCreateSchema()
event_filter_schema = EventFilterSchema()
event_response_schema = EventResponseSchema()
event_response_list_schema = EventResponseSchema(many=True)


def parse_event_create(data: Any) -> EventCreatePayload:
    return load_or_abort(event_create_schema, data)


def parse_event_filters(data: dict[str, Any]) -> EventFilters:
    return load_or_abort(event_filter_schema, data)


def serialize_event(event: VisionEvent) -> dict[str, object]:
    return dump_with_schema(event_response_schema, event)


def serialize_events(events: list[VisionEvent]) -> list[dict[str, object]]:
    return dump_many_with_schema(event_response_list_schema, events)
