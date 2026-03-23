from __future__ import annotations

from flask import request
from flask_restx import Namespace, Resource

from app.schemas.common import ensure_mapping, parse_required_string
from app.services.auth_service import issue_access_token


auth_namespace = Namespace("auth", description="Authentication helpers", path="/auth")


@auth_namespace.route("/token")
class AuthTokenResource(Resource):
    def post(self) -> tuple[dict[str, object], int]:
        payload = ensure_mapping(request.get_json(silent=True) or {})
        token = issue_access_token(parse_required_string(payload, "api_key"))
        return {"access_token": token}, 200
