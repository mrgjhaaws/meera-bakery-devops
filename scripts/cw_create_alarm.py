"""Lesson 15 - panels 4 & 7: CPU alarm that notifies you through SNS.
Run:  python scripts/cw_create_alarm.py <instance-id> you@example.com
Steps: create SNS topic -> subscribe your e-mail (confirm the e-mail!) -> create alarm.
"""
import sys

from _common import client

if len(sys.argv) < 3:
    sys.exit("Usage: python scripts/cw_create_alarm.py <instance-id> <email>")
instance_id, email = sys.argv[1], sys.argv[2]

sns, cw = client("sns"), client("cloudwatch")
topic_arn = sns.create_topic(Name="meera-bakery-alerts")["TopicArn"]
sns.subscribe(TopicArn=topic_arn, Protocol="email", Endpoint=email)
print("Check your inbox and CONFIRM the subscription:", email)

cw.put_metric_alarm(
    AlarmName="High-CPU-Alarm",
    AlarmDescription="CPU above 80% for 10 minutes on the bakery web server",
    Namespace="AWS/EC2",
    MetricName="CPUUtilization",
    Dimensions=[{"Name": "InstanceId", "Value": instance_id}],
    Statistic="Average",
    Period=300,
    EvaluationPeriods=2,
    Threshold=80.0,
    ComparisonOperator="GreaterThanThreshold",
    TreatMissingData="notBreaching",
    AlarmActions=[topic_arn],
    OKActions=[topic_arn],
)
print("Alarm 'High-CPU-Alarm' created. View it: CloudWatch -> Alarms")
