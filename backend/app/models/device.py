from __future__ import annotations

import enum
from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class DeviceType(str, enum.Enum):
    JETSON = "jetson"
    ESP32 = "esp32"
    RASPI = "raspi"


class DeviceStatus(str, enum.Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    ERROR = "error"


class Device(db.Model):
    __tablename__ = "devices"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    type: Mapped[DeviceType] = mapped_column(
        SQLEnum(DeviceType, name="device_type_enum"),
        nullable=False,
    )
    location: Mapped[str] = mapped_column(String(160), nullable=False)
    status: Mapped[DeviceStatus] = mapped_column(
        SQLEnum(DeviceStatus, name="device_status_enum"),
        nullable=False,
        default=DeviceStatus.ONLINE,
    )
    last_seen: Mapped[datetime] = mapped_column(nullable=False, default=utc_now)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=utc_now)

    events: Mapped[list["VisionEvent"]] = relationship(
        back_populates="device",
        cascade="all, delete-orphan",
        order_by="desc(VisionEvent.frame_ts)",
    )
    inspections: Mapped[list["InspectionResult"]] = relationship(
        back_populates="device",
        cascade="all, delete-orphan",
        order_by="desc(InspectionResult.created_at)",
    )

    def __repr__(self) -> str:
        return f"Device(id={self.id!s}, name={self.name!r}, status={self.status.value!r})"
