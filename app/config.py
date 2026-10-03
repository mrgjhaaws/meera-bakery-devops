"""Configuration loading - Lessons 10 and 11.

Order of precedence (highest first):
  1. Real environment variables (e.g. set by Docker / EC2 / GitHub Actions)
  2. .env.<environment> file  (Lesson 10, panel 8)  e.g. .env.development
  3. .env file                (Lesson 10, panel 3)
  4. SSM Parameter Store      (Lesson 11) - only if USE_PARAMETER_STORE=true
"""
import os
from dataclasses import dataclass
from functools import lru_cache

from dotenv import load_dotenv

# load_dotenv() never overrides variables that already exist in the environment,
# so load the most specific file first, then the general one.
_env_name = {"dev": "development", "test": "testing", "prod": "production"}.get(
    os.getenv("APP_ENV", "dev"), os.getenv("APP_ENV", "dev")
)
load_dotenv(f".env.{_env_name}")
load_dotenv(".env")


@dataclass(frozen=True)
class Settings:
    app_env: str
    aws_region: str
    s3_bucket: str
    use_parameter_store: bool

    @property
    def ssm_prefix(self) -> str:
        return f"/meera-bakery/{self.app_env}"


def _read_from_parameter_store(prefix: str, region: str) -> dict:
    """Read every parameter under /meera-bakery/<env>/ (Lesson 11, panel 5/8)."""
    import boto3

    ssm = boto3.client("ssm", region_name=region)
    values = {}
    paginator = ssm.get_paginator("get_parameters_by_path")
    for page in paginator.paginate(Path=prefix, Recursive=True, WithDecryption=True):
        for p in page["Parameters"]:
            values[p["Name"].rsplit("/", 1)[-1]] = p["Value"]
    return values


@lru_cache
def get_settings() -> Settings:
    """Build settings once and cache them (Lesson 11 best practice: use caching)."""
    app_env = os.getenv("APP_ENV", "dev")
    region = os.getenv("AWS_REGION", "ap-south-1")
    bucket = os.getenv("S3_BUCKET", "")
    use_ssm = os.getenv("USE_PARAMETER_STORE", "false").lower() == "true"

    if use_ssm:
        params = _read_from_parameter_store(f"/meera-bakery/{app_env}", region)
        region = params.get("AWS_REGION", region)
        bucket = params.get("S3_BUCKET", bucket)

    return Settings(app_env=app_env, aws_region=region, s3_bucket=bucket,
                    use_parameter_store=use_ssm)
