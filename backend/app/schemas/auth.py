from __future__ import annotations

from typing import Any

from marshmallow import Schema, fields, validate

from app.schemas.common import load_or_abort


class AuthTokenRequestSchema(Schema):
    api_key = fields.Str(required=True, validate=validate.Length(min=1))


auth_token_request_schema = AuthTokenRequestSchema()


def parse_auth_token_request(data: Any) -> dict[str, str]:
    return load_or_abort(auth_token_request_schema, data)
