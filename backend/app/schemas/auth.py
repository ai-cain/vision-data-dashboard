from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from marshmallow import Schema, fields, post_load, validate

from app.schemas.common import UTCDateTime, dump_with_schema, load_or_abort


class AuthTokenRequestSchema(Schema):
    api_key = fields.Str(required=True, validate=validate.Length(min=1))

    @post_load
    def make_payload(self, data: dict[str, str], **kwargs: Any) -> AuthTokenRequestPayload:
        return AuthTokenRequestPayload(**data)


@dataclass(slots=True)
class AuthTokenRequestPayload:
    api_key: str


@dataclass(slots=True)
class AuthTokenResponsePayload:
    access_token: str
    token_type: str
    expires_at: datetime
    expires_in_seconds: int
    principal: str
    scopes: tuple[str, ...]


@dataclass(slots=True)
class AuthContextPayload:
    authenticated: bool
    auth_required: bool
    principal: str
    auth_method: str
    scopes: tuple[str, ...]
    expires_at: datetime | None


class AuthTokenResponseSchema(Schema):
    access_token = fields.Str(required=True)
    token_type = fields.Str(required=True)
    expires_at = UTCDateTime(required=True)
    expires_in_seconds = fields.Int(required=True)
    principal = fields.Str(required=True)
    scopes = fields.List(fields.Str(), required=True)


class AuthContextSchema(Schema):
    authenticated = fields.Bool(required=True)
    auth_required = fields.Bool(required=True)
    principal = fields.Str(required=True)
    auth_method = fields.Str(required=True)
    scopes = fields.List(fields.Str(), required=True)
    expires_at = UTCDateTime(allow_none=True)


auth_token_request_schema = AuthTokenRequestSchema()
auth_token_response_schema = AuthTokenResponseSchema()
auth_context_schema = AuthContextSchema()


def parse_auth_token_request(data: Any) -> AuthTokenRequestPayload:
    return load_or_abort(auth_token_request_schema, data)


def serialize_auth_token_response(payload: AuthTokenResponsePayload) -> dict[str, object]:
    return dump_with_schema(auth_token_response_schema, payload)


def serialize_auth_context(payload: AuthContextPayload) -> dict[str, object]:
    return dump_with_schema(auth_context_schema, payload)
