from __future__ import annotations

from collections import Counter
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import selectinload
from werkzeug.exceptions import NotFound

from app.extensions import db
from app.models.device import Device
from app.models.event import VisionEvent
from app.schemas.common import isoformat_value, normalize_datetime
from app.schemas.event import EventCreatePayload, EventFilters
from app.services.common import PaginatedResult


def list_events(filters: EventFilters) -> PaginatedResult[VisionEvent]:
    statement = (
        db.select(VisionEvent)
        .options(selectinload(VisionEvent.device))
        .order_by(VisionEvent.frame_ts.desc())
    )

    if filters.device_id is not None:
        statement = statement.where(VisionEvent.device_id == filters.device_id)
    if filters.event_type is not None:
        statement = statement.where(VisionEvent.event_type == filters.event_type)
    if filters.start_date is not None:
        statement = statement.where(VisionEvent.frame_ts >= filters.start_date)
    if filters.end_date is not None:
        statement = statement.where(VisionEvent.frame_ts <= filters.end_date)

    pagination = db.paginate(statement, page=filters.page, per_page=filters.per_page, error_out=False)
    return PaginatedResult(
        items=list(pagination.items),
        page=pagination.page,
        per_page=pagination.per_page,
        total=pagination.total,
    )


def create_event(payload: EventCreatePayload) -> VisionEvent:
    device = db.session.scalar(db.select(Device).where(Device.id == payload.device_id))
    if device is None:
        raise NotFound("Device not found")

    event = VisionEvent(
        device_id=payload.device_id,
        event_type=payload.event_type,
        confidence=payload.confidence,
        label=payload.label,
        frame_ts=payload.frame_ts,
        metadata_payload=payload.metadata_payload,
    )
    db.session.add(event)
    device.last_seen = datetime.now(timezone.utc)
    db.session.commit()
    db.session.refresh(event)
    return event


def get_event_stats() -> dict[str, object]:
    events = list(
        db.session.scalars(
            db.select(VisionEvent)
            .options(selectinload(VisionEvent.device))
            .order_by(VisionEvent.frame_ts.asc())
        )
    )

    by_type = Counter(event.event_type.value for event in events)
    by_device = Counter(event.device.name if event.device else "Unknown" for event in events)
    confidences = [event.confidence for event in events]

    now = datetime.now(timezone.utc)
    threshold = now - timedelta(hours=24)
    recent_events = [
        event
        for event in events
        if (normalize_datetime(event.frame_ts) or threshold) >= threshold
    ]

    return {
        "total_events": len(events),
        "average_confidence": round(sum(confidences) / len(confidences), 3) if confidences else 0.0,
        "count_by_type": dict(by_type),
        "count_by_device": dict(by_device),
        "recent_volume": build_hourly_series(recent_events, hours=24),
    }


def build_hourly_series(events: list[VisionEvent], hours: int) -> list[dict[str, object]]:
    now = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
    buckets = [
        {"timestamp": isoformat_value(now - timedelta(hours=offset)), "count": 0}
        for offset in reversed(range(hours))
    ]
    bucket_map = {bucket["timestamp"]: bucket for bucket in buckets}

    for event in events:
        event_dt = normalize_datetime(event.frame_ts)
        if event_dt is None:
            continue
        normalized = event_dt.replace(minute=0, second=0, microsecond=0)
        key = isoformat_value(normalized)
        if key in bucket_map:
            bucket_map[key]["count"] = int(bucket_map[key]["count"]) + 1

    return buckets
