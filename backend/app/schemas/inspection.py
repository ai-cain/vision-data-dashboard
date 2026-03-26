from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import UUID

from marshmallow import Schema, fields, post_load, validate, validates_schema
from marshmallow.exceptions import ValidationError

from app.models.inspection import InspectionOutcome, InspectionResult
from app.schemas.common import (
    UTCDateTime,
    EnumValueField,
    dump_many_with_schema,
    dump_with_schema,
    load_or_abort,
)


@dataclass(slots=True)
class InspectionCreatePayload:
    device_id: UUID
    job_id: str
    result: InspectionOutcome
    defect_type: str | None
    score: float
    image_path: str


@dataclass(slots=True)
class InspectionFilters:
    page: int
    per_page: int
    device_id: UUID | None
    result: InspectionOutcome | None


class InspectionCreateSchema(Schema):
    device_id = fields.UUID(required=True)
    job_id = fields.Str(required=True, validate=validate.Length(min=1))
    result = EnumValueField(InspectionOutcome, required=True)
    defect_type = fields.Str(load_default=None, allow_none=True)
    score = fields.Float(required=True, validate=validate.Range(min=0, max=1))
    image_path = fields.Str(required=True, validate=validate.Length(min=1))

    @validates_schema
    def validate_payload(self, data: dict[str, Any], **kwargs: Any) -> None:
        if data["result"] == InspectionOutcome.FAIL and not data.get("defect_type"):
            raise ValidationError("defect_type is required when result is fail", field_name="defect_type")

    @post_load
    def make_payload(self, data: dict[str, Any], **kwargs: Any) -> InspectionCreatePayload:
        return InspectionCreatePayload(**data)


class InspectionFilterSchema(Schema):
    page = fields.Int(load_default=1, validate=validate.Range(min=1))
    per_page = fields.Int(load_default=25, validate=validate.Range(min=1, max=100))
    device_id = fields.UUID(load_default=None, allow_none=True, data_key="device")
    result = EnumValueField(InspectionOutcome, load_default=None, allow_none=True)

    @post_load
    def make_payload(self, data: dict[str, Any], **kwargs: Any) -> InspectionFilters:
        return InspectionFilters(**data)


class InspectionResponseSchema(Schema):
    id = fields.UUID()
    device_id = fields.UUID()
    device_name = fields.Method("get_device_name")
    job_id = fields.Str()
    result = EnumValueField(InspectionOutcome)
    defect_type = fields.Str(allow_none=True)
    score = fields.Float()
    image_path = fields.Str()
    created_at = UTCDateTime()

    def get_device_name(self, obj: InspectionResult) -> str | None:
        return obj.device.name if obj.device else None


inspection_create_schema = InspectionCreateSchema()
inspection_filter_schema = InspectionFilterSchema()
inspection_response_schema = InspectionResponseSchema()
inspection_response_list_schema = InspectionResponseSchema(many=True)


def parse_inspection_create(data: Any) -> InspectionCreatePayload:
    return load_or_abort(inspection_create_schema, data)


def parse_inspection_filters(data: dict[str, Any]) -> InspectionFilters:
    return load_or_abort(inspection_filter_schema, data)


def serialize_inspection(inspection: InspectionResult) -> dict[str, object]:
    return dump_with_schema(inspection_response_schema, inspection)


def serialize_inspections(inspections: list[InspectionResult]) -> list[dict[str, object]]:
    return dump_many_with_schema(inspection_response_list_schema, inspections)
