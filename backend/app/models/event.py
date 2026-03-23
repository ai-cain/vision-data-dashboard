from __future__ import annotations

import enum
from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import Float, ForeignKey, JSON, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db
from app.models.device import utc_now


class EventType(str, enum.Enum):
    DETECTION = "detection"
    ANOMALY = "anomaly"
    COUNT = "count"


class VisionEvent(db.Model):
    __tablename__ = "vision_events"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    device_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("devices.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    event_type: Mapped[EventType] = mapped_column(
        SQLEnum(EventType, name="event_type_enum"),
        nullable=False,
    )
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    label: Mapped[str] = mapped_column(String(120), nullable=False)
    frame_ts: Mapped[datetime] = mapped_column(nullable=False, index=True)
    metadata_payload: Mapped[dict[str, Any]] = mapped_column(
        "metadata",
        JSON,
        nullable=False,
        default=dict,
    )
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=utc_now)

    device: Mapped["Device"] = relationship(back_populates="events")

    def __repr__(self) -> str:
        return f"VisionEvent(id={self.id!s}, type={self.event_type.value!r}, label={self.label!r})"
