"""Shared helper: load .env and build boto3 clients (no keys hard-coded - Lesson 9/10)."""
import os

import boto3
from dotenv import load_dotenv

load_dotenv()
REGION = os.getenv("AWS_REGION", "ap-south-1")


def client(service: str):
    return boto3.client(service, region_name=REGION)
