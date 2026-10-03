"""Meera's Bakery Online - API.

Run locally:   python -m uvicorn app.main:app --reload
Open docs:     http://127.0.0.1:8000/docs
"""
from pathlib import Path

from botocore.exceptions import BotoCoreError, ClientError
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .aws_clients import s3_client
from .config import get_settings
from .logging_config import setup_logging

log = setup_logging()
app = FastAPI(title="Meera's Bakery Online", version="1.0.0")

STATIC_DIR = Path(__file__).resolve().parent.parent / "static"
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

PRODUCT_PREFIX = "products/"
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}


@app.get("/", include_in_schema=False)
def home():
    index = STATIC_DIR / "index.html"
    if index.exists():
        return FileResponse(index)
    return {"message": "Welcome to Meera's Bakery Online"}


@app.get("/health")
def health():
    """Used by load balancers, Docker health checks and CloudWatch (Lessons 14/15)."""
    s = get_settings()
    return {"status": "ok", "env": s.app_env, "region": s.aws_region}


@app.get("/config")
def show_config():
    """Shows NON-secret settings only. Never return keys from an endpoint!"""
    s = get_settings()
    return {
        "env": s.app_env,
        "region": s.aws_region,
        "bucket_configured": bool(s.s3_bucket),
        "parameter_store": s.use_parameter_store,
    }


@app.get("/products")
def list_products():
    """List product images stored in S3."""
    s = get_settings()
    if not s.s3_bucket:
        raise HTTPException(503, "S3_BUCKET is not configured")
    try:
        resp = s3_client().list_objects_v2(Bucket=s.s3_bucket, Prefix=PRODUCT_PREFIX)
    except (ClientError, BotoCoreError) as exc:
        log.error("Failed to list products: %s", exc)
        raise HTTPException(502, "Could not read from S3") from exc
    items = [o["Key"] for o in resp.get("Contents", []) if not o["Key"].endswith("/")]
    log.info("Listed %d product images", len(items))
    return {"bucket": s.s3_bucket, "count": len(items), "images": items}


@app.post("/products/upload")
async def upload_product_image(file: UploadFile = File(...)):
    """Upload a product image to S3 (Lesson 8/10 real business example)."""
    s = get_settings()
    if not s.s3_bucket:
        raise HTTPException(503, "S3_BUCKET is not configured")
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(415, "Only JPEG, PNG or WEBP images are allowed")
    key = PRODUCT_PREFIX + Path(file.filename or "upload").name
    data = await file.read()
    try:
        s3_client().put_object(Bucket=s.s3_bucket, Key=key, Body=data,
                               ContentType=file.content_type)
    except (ClientError, BotoCoreError) as exc:
        log.error("Failed to upload %s: %s", key, exc)  # ERROR logs -> CloudWatch alarms
        raise HTTPException(502, "Could not write to S3") from exc
    log.info("Uploaded %s (%d bytes)", key, len(data))
    return {"uploaded": key, "bytes": len(data)}
