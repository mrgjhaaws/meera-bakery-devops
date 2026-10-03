"""Lesson 11 - read parameters back (panel 5 & 8).
Run:  python scripts/ssm_get_parameters.py dev
SecureString values are printed masked.
"""
import sys

from _common import client

env = sys.argv[1] if len(sys.argv) > 1 else "dev"
ssm = client("ssm")
path = f"/meera-bakery/{env}"

paginator = ssm.get_paginator("get_parameters_by_path")
found = 0
for page in paginator.paginate(Path=path, Recursive=True, WithDecryption=True):
    for p in page["Parameters"]:
        value = p["Value"] if p["Type"] == "String" else p["Value"][:2] + "*" * 8
        print(f"{p['Name']:<40}{p['Type']:<13}{value}")
        found += 1
print(f"\n{found} parameter(s) under {path}")
