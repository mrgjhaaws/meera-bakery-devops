"""boto3 clients - Lessons 8, 9 and 10.

IMPORTANT: there are NO credentials in this file. boto3 automatically looks for them in
this order: environment variables (AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY, which
python-dotenv loaded from .env) -> ~/.aws/credentials -> IAM role of EC2/ECS/Lambda.
That is exactly why the "Dangerous Secret-Key Mistake" (Lesson 9) is avoidable.
"""
import boto3

from .config import get_settings


def s3_client():
    return boto3.client("s3", region_name=get_settings().aws_region)
