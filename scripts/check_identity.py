"""Lesson 8 - FIRST thing to run after `aws configure` or creating your .env.
Asks AWS "who am I?" (STS). Costs nothing. Works with keys, profiles and IAM roles.
Run:  python scripts/check_identity.py
"""
from botocore.exceptions import ClientError, NoCredentialsError

from _common import client

try:
    me = client("sts").get_caller_identity()
    print("Credentials work!")
    print("  Account :", me["Account"])
    print("  User/Role ARN:", me["Arn"])
except NoCredentialsError:
    print("No credentials found. Run `aws configure` or fill in your .env file (Lesson 8/10).")
except ClientError as exc:
    print("AWS rejected the credentials:", exc.response["Error"]["Message"])
