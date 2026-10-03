"""Lessons 8 & 10 - 'Test with AWS (list S3 buckets)'.  Run: python scripts/list_buckets.py"""
from _common import client

response = client("s3").list_buckets()
print("Your S3 Buckets:")
for bucket in response["Buckets"]:
    print(" -", bucket["Name"])
if not response["Buckets"]:
    print("  (none yet - create one in the console or with Terraform in Lesson 13)")
