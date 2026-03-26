from __future__ import annotations

from flask import request
from flask_restx import Namespace, Resource

from app.schemas.auth import (
    AuthContextPayload,
    AuthTokenResponsePayload,
    parse_auth_token_request,
    serialize_auth_context,
    serialize_auth_token_response,
)
from app.services.auth_service import get_request_auth_context, issue_access_token


auth_namespace = Namespace("auth", description="Authentication helpers", path="/auth")


@auth_namespace.route("/token")
class AuthTokenResource(Resource):
    def post(self) -> tuple[dict[str, object], int]:
        payload = parse_auth_token_request(request.get_json(silent=True) or {})
        token = issue_access_token(payload.api_key)
        return (
            serialize_auth_token_response(
                AuthTokenResponsePayload(
                    access_token=token.access_token,
                    token_type=token.token_type,
                    expires_at=token.expires_at,
                    expires_in_seconds=token.expires_in_seconds,
                    principal=token.principal,
                    scopes=token.scopes,
                )
            ),
            200,
        )


@auth_namespace.route("/me")
class AuthContextResource(Resource):
    def get(self) -> tuple[dict[str, object], int]:
        context = get_request_auth_context(optional=False)
        return (
            serialize_auth_context(
                AuthContextPayload(
                    authenticated=context.authenticated,
                    auth_required=context.auth_required,
                    principal=context.principal,
                    auth_method=context.auth_method,
                    scopes=context.scopes,
                    expires_at=context.expires_at,
                )
            ),
            200,
        )
