from __future__ import annotations

from flask import request
from flask_restx import Namespace, Resource

from app.schemas.auth import parse_auth_token_request
from app.services.auth_service import issue_access_token


auth_namespace = Namespace("auth", description="Authentication helpers", path="/auth")


@auth_namespace.route("/token")
class AuthTokenResource(Resource):
    def post(self) -> tuple[dict[str, object], int]:
        payload = parse_auth_token_request(request.get_json(silent=True) or {})
        token = issue_access_token(payload["api_key"])
        return {"access_token": token}, 200
