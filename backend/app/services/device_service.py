from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.orm import selectinload
from werkzeug.exceptions import Conflict, NotFound

from app.extensions import db
from app.models.device import Device
from app.models.event import VisionEvent
from app.schemas.device import DeviceCreatePayload, DeviceStatusUpdatePayload


def list_devices() -> list[Device]:
    statement = db.select(Device).order_by(Device.name.asc())
    return list(db.session.scalars(statement))


def create_device(payload: DeviceCreatePayload) -> Device:
    existing = db.session.scalar(db.select(Device).where(Device.name == payload.name))
    if existing is not None:
        raise Conflict(f"Device with name '{payload.name}' already exists")

    device = Device(
        name=payload.name,
        type=payload.device_type,
        location=payload.location,
        status=payload.status,
        last_seen=datetime.now(timezone.utc),
    )
    db.session.add(device)
    db.session.commit()
    return device


def get_device(device_id: UUID) -> Device:
    statement = db.select(Device).where(Device.id == device_id)
    device = db.session.scalar(statement)
    if device is None:
        raise NotFound("Device not found")
    return device


def get_device_detail(device_id: UUID, recent_limit: int = 20) -> tuple[Device, list[VisionEvent]]:
    statement = (
        db.select(Device)
        .options(selectinload(Device.events))
        .where(Device.id == device_id)
    )
    device = db.session.scalar(statement)
    if device is None:
        raise NotFound("Device not found")

    recent_events_statement = (
        db.select(VisionEvent)
        .options(selectinload(VisionEvent.device))
        .where(VisionEvent.device_id == device_id)
        .order_by(VisionEvent.frame_ts.desc())
        .limit(recent_limit)
    )
    recent_events = list(db.session.scalars(recent_events_statement))
    return device, recent_events


def update_device_status(device_id: UUID, payload: DeviceStatusUpdatePayload) -> Device:
    device = get_device(device_id)
    device.status = payload.status
    device.last_seen = payload.last_seen or datetime.now(timezone.utc)
    db.session.commit()
    return device
