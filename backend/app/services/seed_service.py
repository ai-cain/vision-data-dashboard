from __future__ import annotations

import random
from datetime import datetime, timedelta, timezone

from app.extensions import db
from app.models.device import Device, DeviceStatus, DeviceType
from app.models.event import EventType, VisionEvent
from app.models.inspection import InspectionOutcome, InspectionResult


def seed_database(*, truncate: bool = False) -> None:
    if truncate:
        db.session.execute(db.delete(VisionEvent))
        db.session.execute(db.delete(InspectionResult))
        db.session.execute(db.delete(Device))
        db.session.commit()

    existing_device = db.session.scalar(db.select(Device.id).limit(1))
    if existing_device is not None:
        return

    rng = random.Random(42)
    now = datetime.now(timezone.utc)

    devices = [
        Device(name="Jetson-Line-01", type=DeviceType.JETSON, location="Packaging Cell A", status=DeviceStatus.ONLINE, last_seen=now - timedelta(minutes=2)),
        Device(name="Jetson-Line-02", type=DeviceType.JETSON, location="Packaging Cell B", status=DeviceStatus.ERROR, last_seen=now - timedelta(minutes=12)),
        Device(name="ESP32-Gateway-01", type=DeviceType.ESP32, location="Warehouse Dock", status=DeviceStatus.ONLINE, last_seen=now - timedelta(minutes=1)),
        Device(name="Raspi-QC-01", type=DeviceType.RASPI, location="Quality Lab", status=DeviceStatus.OFFLINE, last_seen=now - timedelta(hours=4)),
        Device(name="Raspi-QC-02", type=DeviceType.RASPI, location="Quality Lab Annex", status=DeviceStatus.ONLINE, last_seen=now - timedelta(minutes=7)),
    ]
    db.session.add_all(devices)
    db.session.flush()

    labels = ["bottle", "seal", "cap", "label", "pallet", "worker"]
    defects = ["scratch", "misalignment", "missing_cap", "seal_breach"]

    events: list[VisionEvent] = []
    for hour in range(0, 48):
        device = devices[hour % len(devices)]
        event_count = rng.randint(1, 3)
        for offset in range(event_count):
            timestamp = now - timedelta(hours=hour, minutes=rng.randint(0, 59))
            events.append(
                VisionEvent(
                    device_id=device.id,
                    event_type=rng.choice(list(EventType)),
                    confidence=round(rng.uniform(0.61, 0.99), 3),
                    label=rng.choice(labels),
                    frame_ts=timestamp,
                    metadata_payload={
                        "bbox": [
                            rng.randint(0, 300),
                            rng.randint(0, 300),
                            rng.randint(20, 90),
                            rng.randint(20, 90),
                        ],
                        "source": "seed",
                        "sequence": hour * 10 + offset,
                    },
                )
            )

    inspections: list[InspectionResult] = []
    for day in range(0, 14):
        for batch in range(0, 4):
            device = rng.choice(devices)
            outcome = rng.choices(
                population=[InspectionOutcome.PASS, InspectionOutcome.FAIL, InspectionOutcome.UNCERTAIN],
                weights=[0.7, 0.2, 0.1],
                k=1,
            )[0]
            created_at = now - timedelta(days=day, hours=rng.randint(0, 23))
            inspections.append(
                InspectionResult(
                    device_id=device.id,
                    job_id=f"JOB-{created_at:%Y%m%d}-{batch + 1:03d}",
                    result=outcome,
                    defect_type=rng.choice(defects) if outcome == InspectionOutcome.FAIL else None,
                    score=round(rng.uniform(0.6, 0.99), 3),
                    image_path=f"/captures/{created_at:%Y/%m/%d}/frame-{batch + 1:03d}.jpg",
                    created_at=created_at,
                )
            )

    db.session.add_all(events)
    db.session.add_all(inspections)
    db.session.commit()
