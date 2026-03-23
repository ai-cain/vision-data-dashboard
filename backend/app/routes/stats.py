from __future__ import annotations

from flask_restx import Namespace, Resource

from app.services.stats_service import get_dashboard_overview


stats_namespace = Namespace("stats", description="Dashboard rollups", path="/stats")


@stats_namespace.route("/overview")
class DashboardOverviewResource(Resource):
    def get(self) -> tuple[dict[str, object], int]:
        return get_dashboard_overview(), 200
