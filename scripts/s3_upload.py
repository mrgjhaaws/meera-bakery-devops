"""Lessons 8 & 10 - upload a product image to S3.
Run:  python scripts/s3_upload.py path/to/cake.png [bucket-name]
If bucket-name is omitted, S3_BUCKET from .env is used.
"""
import mimetypes
import os
import sys
from pathlib import Path

from _common import client

if len(sys.argv) < 2:
    sys.exit("Usage: python scripts/s3_upload.py <image-file> [bucket]")

path = Path(sys.argv[1])
bucket = sys.argv[2] if len(sys.argv) > 2 else os.getenv("S3_BUCKET")
if not bucket:
    sys.exit("Give a bucket name or set S3_BUCKET in .env")

key = f"products/{path.name}"
content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
client("s3").upload_file(str(path), bucket, key, ExtraArgs={"ContentType": content_type})
print(f"Uploaded {path} -> s3://{bucket}/{key}")
