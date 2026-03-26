from __future__ import annotations


def test_issue_token_returns_metadata(client) -> None:
    response = client.post("/api/v1/auth/token", json={"api_key": "test-admin-key"})

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["token_type"] == "Bearer"
    assert payload["principal"] == "dashboard-admin"
    assert payload["expires_in_seconds"] == 3600
    assert "dashboard:write" in payload["scopes"]
    assert payload["access_token"]


def test_auth_me_rejects_missing_credentials_when_auth_is_required(client) -> None:
    response = client.get("/api/v1/auth/me")

    assert response.status_code == 401
    assert response.get_json()["message"] == "Write access requires a valid JWT or X-API-Key header"


def test_auth_me_accepts_api_key(client) -> None:
    response = client.get("/api/v1/auth/me", headers={"X-API-Key": "test-admin-key"})

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["auth_method"] == "api-key"
    assert payload["principal"] == "dashboard-admin"
    assert payload["scopes"] == ["dashboard:write"]


def test_auth_me_accepts_jwt(client) -> None:
    token_response = client.post("/api/v1/auth/token", json={"api_key": "test-admin-key"})
    access_token = token_response.get_json()["access_token"]

    response = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["auth_method"] == "api_key"
    assert payload["principal"] == "dashboard-admin"
    assert "dashboard:write" in payload["scopes"]
    assert payload["expires_at"]
