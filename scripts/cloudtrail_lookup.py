"""Lessons 7 & 9 - 'Audit & Compliance: track who did what (CloudTrail)'.
Shows the last 20 management events. Handy after a suspected key leak.
Run:  python scripts/cloudtrail_lookup.py [AccessKeyId]
"""
import sys

from _common import client

kwargs = {"MaxResults": 20}
if len(sys.argv) > 1:
    kwargs["LookupAttributes"] = [{"AttributeKey": "AccessKeyId", "AttributeValue": sys.argv[1]}]

for e in client("cloudtrail").lookup_events(**kwargs)["Events"]:
    print(f"{e['EventTime']:%Y-%m-%d %H:%M}  {e.get('Username', '-'):<20}  {e['EventName']}")
