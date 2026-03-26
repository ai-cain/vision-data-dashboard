from __future__ import annotations

from flask import request
from flask_restx import Namespace, Resource

from app.schemas.common import parse_uuid_value
from app.schemas.device import (
    parse_device_create,
    parse_device_status_update,
    serialize_device,
    serialize_device_detail,
    serialize_devices,
)
from app.services.auth_service import enforce_write_access
from app.services.device_service import (
    create_device,
    get_device_detail,
    list_devices,
    update_device_status,
)


devices_namespace = Namespace("devices", description="Edge device fleet", path="/devices")


@devices_namespace.route("")
class DeviceCollectionResource(Resource):
    def get(self) -> tuple[dict[str, object], int]:
        devices = list_devices()
        return {
            "items": serialize_devices(devices),
            "total": len(devices),
        }, 200

    def post(self) -> tuple[dict[str, object], int]:
        enforce_write_access()
        payload = parse_device_create(request.get_json(silent=True) or {})
        device = create_device(payload)
        return serialize_device(device), 201


@devices_namespace.route("/<string:device_id>")
class DeviceDetailResource(Resource):
    def get(self, device_id: str) -> tuple[dict[str, object], int]:
        device, recent_events = get_device_detail(parse_uuid_value(device_id, "device_id"))
        return serialize_device_detail(device, recent_events), 200


@devices_namespace.route("/<string:device_id>/status")
class DeviceStatusResource(Resource):
    def patch(self, device_id: str) -> tuple[dict[str, object], int]:
        enforce_write_access()
        payload = parse_device_status_update(request.get_json(silent=True) or {})
        device = update_device_status(parse_uuid_value(device_id, "device_id"), payload)
        return serialize_device(device), 200
