"""Lesson 11 - create the /meera-bakery/<env>/... parameters (panel 3 & 4).
Run:  python scripts/ssm_put_parameters.py dev my-bucket-name
Creates:  /meera-bakery/dev/AWS_REGION   (String)
          /meera-bakery/dev/S3_BUCKET    (String)
          /meera-bakery/dev/DB_PASSWORD  (SecureString, example secret - only if DB_PASSWORD is set)
"""
import os
import sys

from _common import REGION, client

if len(sys.argv) < 3:
    sys.exit("Usage: python scripts/ssm_put_parameters.py <dev|test|prod> <s3-bucket-name>")

env, bucket = sys.argv[1], sys.argv[2]
ssm = client("ssm")
prefix = f"/meera-bakery/{env}"

params = [(f"{prefix}/AWS_REGION", REGION, "String"),
          (f"{prefix}/S3_BUCKET", bucket, "String")]
if os.getenv("DB_PASSWORD"):                     # never type secrets on the command line
    params.append((f"{prefix}/DB_PASSWORD", os.environ["DB_PASSWORD"], "SecureString"))

for name, value, ptype in params:
    ssm.put_parameter(Name=name, Value=value, Type=ptype, Overwrite=True)
    print(f"saved {ptype:<13}{name}")
