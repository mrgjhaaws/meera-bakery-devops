"""Lesson 5 - list AWS Regions (and Availability Zones of your current Region).
Run:  python scripts/list_regions.py
"""
from _common import REGION, client

ec2 = client("ec2")
print(f"{'Region name':<18}{'Opt-in status'}")
for r in sorted(ec2.describe_regions(AllRegions=True)["Regions"], key=lambda x: x["RegionName"]):
    mark = "  <-- your region" if r["RegionName"] == REGION else ""
    print(f"{r['RegionName']:<18}{r.get('OptInStatus', '-')}{mark}")

print(f"\nAvailability Zones in {REGION}:")
for az in ec2.describe_availability_zones()["AvailabilityZones"]:
    print(f"  {az['ZoneName']:<16}{az['State']}")
