"""Initial schema."""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "20260325_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    device_type_enum = sa.Enum("jetson", "esp32", "raspi", name="device_type_enum")
    device_status_enum = sa.Enum("online", "offline", "error", name="device_status_enum")
    event_type_enum = sa.Enum("detection", "anomaly", "count", name="event_type_enum")
    inspection_result_enum = sa.Enum("pass", "fail", "uncertain", name="inspection_result_enum")

    op.create_table(
        "devices",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("type", device_type_enum, nullable=False),
        sa.Column("location", sa.String(length=160), nullable=False),
        sa.Column("status", device_status_enum, nullable=False),
        sa.Column("last_seen", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )

    op.create_table(
        "vision_events",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("device_id", sa.Uuid(), nullable=False),
        sa.Column("event_type", event_type_enum, nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("label", sa.String(length=120), nullable=False),
        sa.Column("frame_ts", sa.DateTime(timezone=True), nullable=False),
        sa.Column("metadata", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["device_id"], ["devices.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_vision_events_device_id"), "vision_events", ["device_id"], unique=False)
    op.create_index(op.f("ix_vision_events_frame_ts"), "vision_events", ["frame_ts"], unique=False)

    op.create_table(
        "inspection_results",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("device_id", sa.Uuid(), nullable=False),
        sa.Column("job_id", sa.String(length=120), nullable=False),
        sa.Column("result", inspection_result_enum, nullable=False),
        sa.Column("defect_type", sa.String(length=120), nullable=True),
        sa.Column("score", sa.Float(), nullable=False),
        sa.Column("image_path", sa.String(length=260), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["device_id"], ["devices.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_inspection_results_created_at"), "inspection_results", ["created_at"], unique=False)
    op.create_index(op.f("ix_inspection_results_device_id"), "inspection_results", ["device_id"], unique=False)
    op.create_index(op.f("ix_inspection_results_job_id"), "inspection_results", ["job_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_inspection_results_job_id"), table_name="inspection_results")
    op.drop_index(op.f("ix_inspection_results_device_id"), table_name="inspection_results")
    op.drop_index(op.f("ix_inspection_results_created_at"), table_name="inspection_results")
    op.drop_table("inspection_results")

    op.drop_index(op.f("ix_vision_events_frame_ts"), table_name="vision_events")
    op.drop_index(op.f("ix_vision_events_device_id"), table_name="vision_events")
    op.drop_table("vision_events")

    op.drop_table("devices")
