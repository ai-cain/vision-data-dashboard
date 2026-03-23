from __future__ import annotations

from flask import Blueprint
from flask_restx import Api

from app.routes.auth import auth_namespace
from app.routes.devices import devices_namespace
from app.routes.events import events_namespace
from app.routes.inspections import inspections_namespace
from app.routes.stats import stats_namespace


api_blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(
    api_blueprint,
    title="Vision Data Dashboard API",
    version="1.0",
    doc="/docs",
    description="REST API for device telemetry, CV events, and inspection metrics.",
)

api.add_namespace(auth_namespace)
api.add_namespace(devices_namespace)
api.add_namespace(events_namespace)
api.add_namespace(inspections_namespace)
api.add_namespace(stats_namespace)
