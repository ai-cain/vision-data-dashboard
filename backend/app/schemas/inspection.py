from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping
from uuid import UUID

from werkzeug.exceptions import BadRequest

from app.models.inspection import InspectionOutcome, InspectionResult
from app.schemas.common import (
    ensure_mapping,
    isoformat_value,
    parse_float_value,
    parse_integer_value,
    parse_optional_string,
    parse_required_string,
    parse_uuid_value,
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


def parse_inspection_create(data: Any) -> InspectionCreatePayload:
    payload = ensure_mapping(data)
    score = parse_float_value(payload, "score")
    if score < 0 or score > 1:
        raise BadRequest("Field 'score' must be between 0 and 1")

    result = _parse_outcome(payload.get("result"))
    defect_type = parse_optional_string(payload, "defect_type")
    if result == InspectionOutcome.FAIL and defect_type is None:
        raise BadRequest("Field 'defect_type' is required when result is 'fail'")

    return InspectionCreatePayload(
        device_id=parse_uuid_value(parse_required_string(payload, "device_id"), "device_id"),
        job_id=parse_required_string(payload, "job_id"),
        result=result,
        defect_type=defect_type,
        score=score,
        image_path=parse_required_string(payload, "image_path"),
    )


def parse_inspection_filters(data: Mapping[str, Any]) -> InspectionFilters:
    device_id = parse_optional_string(data, "device")
    raw_result = data.get("result")
    return InspectionFilters(
        page=parse_integer_value(data.get("page"), "page", default=1, minimum=1),
        per_page=parse_integer_value(data.get("per_page"), "per_page", default=25, minimum=1, maximum=100),
        device_id=parse_uuid_value(device_id, "device") if device_id else None,
        result=_parse_outcome(raw_result) if raw_result not in (None, "") else None,
    )


def serialize_inspection(inspection: InspectionResult) -> dict[str, object]:
    return {
        "id": str(inspection.id),
        "device_id": str(inspection.device_id),
        "device_name": inspection.device.name if inspection.device else None,
        "job_id": inspection.job_id,
        "result": inspection.result.value,
        "defect_type": inspection.defect_type,
        "score": inspection.score,
        "image_path": inspection.image_path,
        "created_at": isoformat_value(inspection.created_at),
    }


def _parse_outcome(value: Any) -> InspectionOutcome:
    if not isinstance(value, str):
        raise BadRequest("Field 'result' must be one of: pass, fail, uncertain")
    try:
        return InspectionOutcome(value.strip().lower())
    except ValueError as error:
        raise BadRequest("Field 'result' must be one of: pass, fail, uncertain") from error
