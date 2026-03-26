from __future__ import annotations

import sys
from pathlib import Path

import pytest


BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))


from app import create_app  # noqa: E402
from app.config import Config  # noqa: E402


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg://vision:vision@localhost:5432/vision_dashboard_test"
    AUTH_REQUIRED = True
    ADMIN_API_KEY = "test-admin-key"
    ADMIN_API_KEYS = ("test-admin-key",)
    JWT_SECRET_KEY = "test-jwt-secret-with-32-plus-characters"
    FRONTEND_ORIGIN = "http://localhost:5173"


@pytest.fixture
def app():
    return create_app(TestConfig)


@pytest.fixture
def client(app):
    return app.test_client()
