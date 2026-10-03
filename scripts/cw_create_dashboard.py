"""Lesson 15 - panel 6: 'Meera Bakery Dashboard'.
Run:  python scripts/cw_create_dashboard.py <instance-id>
"""
import json
import sys

from _common import REGION, client

if len(sys.argv) < 2:
    sys.exit("Usage: python scripts/cw_create_dashboard.py <instance-id>")
iid = sys.argv[1]


def widget(x, title, namespace, metric, dims):
    return {"type": "metric", "x": x, "y": 0, "width": 12, "height": 6,
            "properties": {"title": title, "region": REGION, "view": "timeSeries",
                           "stat": "Average", "period": 300,
                           "metrics": [[namespace, metric, *dims]]}}


body = {"widgets": [
    widget(0, "EC2 CPU Utilization (%)", "AWS/EC2", "CPUUtilization", ["InstanceId", iid]),
    widget(12, "EC2 Network In (bytes)", "AWS/EC2", "NetworkIn", ["InstanceId", iid]),
]}
client("cloudwatch").put_dashboard(DashboardName="Meera-Bakery-Dashboard",
                                   DashboardBody=json.dumps(body))
print("Dashboard created: CloudWatch -> Dashboards -> Meera-Bakery-Dashboard")
