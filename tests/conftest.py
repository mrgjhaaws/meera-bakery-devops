import os

import pytest

# Fake credentials so tests can NEVER touch a real AWS account (moto intercepts calls).
os.environ.setdefault("AWS_ACCESS_KEY_ID", "testing")
os.environ.setdefault("AWS_SECRET_ACCESS_KEY", "testing")
os.environ.setdefault("AWS_DEFAULT_REGION", "ap-south-1")


@pytest.fixture(autouse=True)
def _clean_settings(monkeypatch):
    from app.config import get_settings

    monkeypatch.setenv("APP_ENV", "test")
    monkeypatch.setenv("AWS_REGION", "ap-south-1")
    monkeypatch.setenv("S3_BUCKET", "meera-test-bucket")
    monkeypatch.setenv("USE_PARAMETER_STORE", "false")
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()
