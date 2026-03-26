from __future__ import annotations

from flask import request
from flask_restx import Namespace, Resource

from app.schemas.event import parse_event_create, parse_event_filters, serialize_event, serialize_events
from app.services.auth_service import enforce_write_access
from app.services.event_service import create_event, get_event_stats, list_events


events_namespace = Namespace("events", description="Vision event ingestion and analytics", path="/events")


@events_namespace.route("")
class EventCollectionResource(Resource):
    def get(self) -> tuple[dict[str, object], int]:
        filters = parse_event_filters(request.args.to_dict())
        result = list_events(filters)
        return {
            "items": serialize_events(result.items),
            "page": result.page,
            "per_page": result.per_page,
            "total": result.total,
        }, 200

    def post(self) -> tuple[dict[str, object], int]:
        enforce_write_access()
        payload = parse_event_create(request.get_json(silent=True) or {})
        event = create_event(payload)
        return serialize_event(event), 201


@events_namespace.route("/stats")
class EventStatsResource(Resource):
    def get(self) -> tuple[dict[str, object], int]:
        return get_event_stats(), 200
