from __future__ import annotations

from flask import request
from flask_restx import Namespace, Resource

from app.schemas.inspection import (
    parse_inspection_create,
    parse_inspection_filters,
    serialize_inspection,
)
from app.services.auth_service import enforce_write_access
from app.services.inspection_service import (
    create_inspection,
    get_inspection_summary,
    list_inspections,
)


inspections_namespace = Namespace(
    "inspections",
    description="Inspection outcomes and summaries",
    path="/inspections",
)


@inspections_namespace.route("")
class InspectionCollectionResource(Resource):
    def get(self) -> tuple[dict[str, object], int]:
        filters = parse_inspection_filters(request.args.to_dict())
        result = list_inspections(filters)
        return {
            "items": [serialize_inspection(inspection) for inspection in result.items],
            "page": result.page,
            "per_page": result.per_page,
            "total": result.total,
        }, 200

    def post(self) -> tuple[dict[str, object], int]:
        enforce_write_access()
        payload = parse_inspection_create(request.get_json(silent=True) or {})
        inspection = create_inspection(payload)
        return serialize_inspection(inspection), 201


@inspections_namespace.route("/summary")
class InspectionSummaryResource(Resource):
    def get(self) -> tuple[dict[str, object], int]:
        return get_inspection_summary(), 200
