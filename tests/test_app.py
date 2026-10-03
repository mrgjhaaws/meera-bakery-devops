import boto3
from fastapi.testclient import TestClient
from moto import mock_aws

from app.config import get_settings
from app.main import app

client = TestClient(app)
REGION = "ap-south-1"


def _make_bucket(name="meera-test-bucket"):
    s3 = boto3.client("s3", region_name=REGION)
    s3.create_bucket(Bucket=name, CreateBucketConfiguration={"LocationConstraint": REGION})
    return s3


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_config_never_leaks_secrets():
    body = client.get("/config").json()
    assert "secret" not in str(body).lower()
    assert body["bucket_configured"] is True


@mock_aws
def test_upload_and_list_products():
    _make_bucket()
    files = {"file": ("chocolate-cake.png", b"\x89PNG fake", "image/png")}
    assert client.post("/products/upload", files=files).status_code == 200
    r = client.get("/products")
    assert r.status_code == 200
    assert r.json()["images"] == ["products/chocolate-cake.png"]


@mock_aws
def test_upload_rejects_non_images():
    _make_bucket()
    files = {"file": ("notes.txt", b"hello", "text/plain")}
    assert client.post("/products/upload", files=files).status_code == 415


def test_missing_bucket_returns_503(monkeypatch):
    monkeypatch.setenv("S3_BUCKET", "")
    get_settings.cache_clear()
    assert client.get("/products").status_code == 503


@mock_aws
def test_settings_from_parameter_store(monkeypatch):
    ssm = boto3.client("ssm", region_name=REGION)
    ssm.put_parameter(Name="/meera-bakery/test/S3_BUCKET", Value="from-ssm-bucket", Type="String")
    ssm.put_parameter(Name="/meera-bakery/test/AWS_REGION", Value=REGION, Type="String")
    monkeypatch.setenv("USE_PARAMETER_STORE", "true")
    monkeypatch.setenv("S3_BUCKET", "ignored")
    get_settings.cache_clear()
    assert get_settings().s3_bucket == "from-ssm-bucket"
