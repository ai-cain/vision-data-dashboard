from __future__ import annotations

from collections import Counter
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import selectinload
from werkzeug.exceptions import NotFound

from app.extensions import db
from app.models.device import Device
from app.models.inspection import InspectionOutcome, InspectionResult
from app.schemas.inspection import InspectionCreatePayload, InspectionFilters
from app.services.common import PaginatedResult


def list_inspections(filters: InspectionFilters) -> PaginatedResult[InspectionResult]:
    statement = (
        db.select(InspectionResult)
        .options(selectinload(InspectionResult.device))
        .order_by(InspectionResult.created_at.desc())
    )
    if filters.device_id is not None:
        statement = statement.where(InspectionResult.device_id == filters.device_id)
    if filters.result is not None:
        statement = statement.where(InspectionResult.result == filters.result)

    pagination = db.paginate(statement, page=filters.page, per_page=filters.per_page, error_out=False)
    return PaginatedResult(
        items=list(pagination.items),
        page=pagination.page,
        per_page=pagination.per_page,
        total=pagination.total,
    )


def create_inspection(payload: InspectionCreatePayload) -> InspectionResult:
    device = db.session.scalar(db.select(Device).where(Device.id == payload.device_id))
    if device is None:
        raise NotFound("Device not found")

    inspection = InspectionResult(
        device_id=payload.device_id,
        job_id=payload.job_id,
        result=payload.result,
        defect_type=payload.defect_type,
        score=payload.score,
        image_path=payload.image_path,
    )
    db.session.add(inspection)
    db.session.commit()
    db.session.refresh(inspection)
    return inspection


def get_inspection_summary() -> dict[str, object]:
    inspections = list(
        db.session.scalars(
            db.select(InspectionResult)
            .options(selectinload(InspectionResult.device))
            .order_by(InspectionResult.created_at.asc())
        )
    )

    by_result = Counter(inspection.result.value for inspection in inspections)
    defects = Counter(
        inspection.defect_type
        for inspection in inspections
        if inspection.defect_type is not None
    )

    total = len(inspections)
    passed = by_result.get(InspectionOutcome.PASS.value, 0)
    pass_rate = round((passed / total) * 100, 1) if total else 0.0

    return {
        "total_inspections": total,
        "pass_rate": pass_rate,
        "count_by_result": dict(by_result),
        "defect_breakdown": dict(defects),
        "trend": build_daily_trend(inspections, days=7),
    }


def build_daily_trend(inspections: list[InspectionResult], days: int) -> list[dict[str, object]]:
    today = datetime.now(timezone.utc).date()
    buckets = [
        {"date": (today - timedelta(days=offset)).isoformat(), "pass": 0, "fail": 0, "uncertain": 0}
        for offset in reversed(range(days))
    ]
    bucket_map = {bucket["date"]: bucket for bucket in buckets}

    for inspection in inspections:
        key = inspection.created_at.astimezone(timezone.utc).date().isoformat()
        if key not in bucket_map:
            continue
        bucket = bucket_map[key]
        bucket[inspection.result.value] = int(bucket[inspection.result.value]) + 1

    return buckets
