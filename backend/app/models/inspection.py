from __future__ import annotations

import enum
from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import Float, ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db
from app.models.device import utc_now


class InspectionOutcome(str, enum.Enum):
    PASS = "pass"
    FAIL = "fail"
    UNCERTAIN = "uncertain"


class InspectionResult(db.Model):
    __tablename__ = "inspection_results"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    device_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("devices.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    job_id: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    result: Mapped[InspectionOutcome] = mapped_column(
        SQLEnum(InspectionOutcome, name="inspection_result_enum"),
        nullable=False,
    )
    defect_type: Mapped[str | None] = mapped_column(String(120), nullable=True)
    score: Mapped[float] = mapped_column(Float, nullable=False)
    image_path: Mapped[str] = mapped_column(String(260), nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=utc_now, index=True)

    device: Mapped["Device"] = relationship(back_populates="inspections")

    def __repr__(self) -> str:
        return f"InspectionResult(id={self.id!s}, job_id={self.job_id!r}, result={self.result.value!r})"
