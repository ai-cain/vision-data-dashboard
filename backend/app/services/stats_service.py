from __future__ import annotations

from collections import Counter
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import selectinload

from app.extensions import db
from app.models.device import Device
from app.models.event import VisionEvent
from app.models.inspection import InspectionOutcome, InspectionResult
from app.schemas.device import serialize_device
from app.schemas.event import serialize_event
from app.schemas.inspection import serialize_inspection
from app.services.event_service import build_hourly_series
from app.services.inspection_service import build_daily_trend


def get_dashboard_overview() -> dict[str, object]:
    devices = list(db.session.scalars(db.select(Device).order_by(Device.name.asc())))
    recent_events = list(
        db.session.scalars(
            db.select(VisionEvent)
            .options(selectinload(VisionEvent.device))
            .order_by(VisionEvent.frame_ts.desc())
            .limit(10)
        )
    )
    all_events = list(
        db.session.scalars(
            db.select(VisionEvent)
            .options(selectinload(VisionEvent.device))
            .order_by(VisionEvent.frame_ts.asc())
        )
    )
    inspections = list(
        db.session.scalars(
            db.select(InspectionResult)
            .options(selectinload(InspectionResult.device))
            .order_by(InspectionResult.created_at.asc())
        )
    )

    device_counts = Counter(device.status.value for device in devices)
    recent_threshold = datetime.now(timezone.utc) - timedelta(hours=24)
    events_last_day = [event for event in all_events if event.frame_ts >= recent_threshold]

    inspection_counts = Counter(inspection.result.value for inspection in inspections)
    total_inspections = len(inspections)
    pass_rate = (
        round((inspection_counts.get(InspectionOutcome.PASS.value, 0) / total_inspections) * 100, 1)
        if total_inspections
        else 0.0
    )

    return {
        "device_counts": {
            "total": len(devices),
            "online": device_counts.get("online", 0),
            "offline": device_counts.get("offline", 0),
            "error": device_counts.get("error", 0),
        },
        "events_last_24h": build_hourly_series(events_last_day, hours=24),
        "events_total": len(all_events),
        "inspection_pass_rate": pass_rate,
        "inspection_trend": build_daily_trend(inspections, days=7),
        "recent_events": [serialize_event(event) for event in recent_events],
        "devices": [serialize_device(device) for device in devices],
        "latest_inspections": [serialize_inspection(item) for item in inspections[-10:][::-1]],
    }
