from __future__ import annotations

from uuid import uuid4

import pytest
from werkzeug.exceptions import BadRequest

from app.schemas.auth import parse_auth_token_request
from app.schemas.device import parse_device_create
from app.schemas.event import parse_event_create, parse_event_filters
from app.schemas.inspection import parse_inspection_create


def test_parse_auth_token_request_requires_api_key() -> None:
    with pytest.raises(BadRequest):
        parse_auth_token_request({})


def test_parse_device_create_builds_payload() -> None:
    payload = parse_device_create(
        {
            "name": "Jetson-Line-03",
            "type": "jetson",
            "location": "Packaging Cell C",
            "status": "online",
        }
    )

    assert payload.name == "Jetson-Line-03"
    assert payload.device_type.value == "jetson"
    assert payload.status.value == "online"


def test_parse_event_filters_rejects_invalid_date_range() -> None:
    with pytest.raises(BadRequest):
        parse_event_filters(
            {
                "start_date": "2026-03-25T12:00:00Z",
                "end_date": "2026-03-24T12:00:00Z",
            }
        )


def test_parse_event_create_loads_metadata() -> None:
    payload = parse_event_create(
        {
            "device_id": str(uuid4()),
            "event_type": "detection",
            "confidence": 0.92,
            "label": "cap",
            "frame_ts": "2026-03-25T20:00:00Z",
            "metadata": {"source": "camera-a"},
        }
    )

    assert payload.event_type.value == "detection"
    assert payload.metadata_payload["source"] == "camera-a"


def test_parse_inspection_create_requires_defect_on_fail() -> None:
    with pytest.raises(BadRequest):
        parse_inspection_create(
            {
                "device_id": str(uuid4()),
                "job_id": "JOB-001",
                "result": "fail",
                "score": 0.88,
                "image_path": "/captures/frame.jpg",
            }
        )
