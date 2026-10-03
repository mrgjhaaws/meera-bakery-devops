# Lesson 15 - CloudWatch log group, alarm, SNS notification and dashboard

resource "aws_cloudwatch_log_group" "app" {
  name              = "/aws/app/meera-bakery"
  retention_in_days = 30 # panel 9: set a retention period
}

resource "aws_sns_topic" "alerts" {
  name = "${local.name_prefix}-alerts"
}

resource "aws_sns_topic_subscription" "email" {
  count     = var.alert_email == "" ? 0 : 1
  topic_arn = aws_sns_topic.alerts.arn
  protocol  = "email"
  endpoint  = var.alert_email # you must click "Confirm subscription" in the e-mail
}

resource "aws_cloudwatch_metric_alarm" "high_cpu" {
  alarm_name          = "${local.name_prefix}-High-CPU-Alarm"
  alarm_description   = "CPU above 80% for 10 minutes on the bakery web server"
  namespace           = "AWS/EC2"
  metric_name         = "CPUUtilization"
  dimensions          = { InstanceId = aws_instance.web.id }
  statistic           = "Average"
  period              = 300
  evaluation_periods  = 2
  threshold           = 80
  comparison_operator = "GreaterThanThreshold"
  treat_missing_data  = "notBreaching"
  alarm_actions       = [aws_sns_topic.alerts.arn]
  ok_actions          = [aws_sns_topic.alerts.arn]
}

resource "aws_cloudwatch_dashboard" "bakery" {
  dashboard_name = "${local.name_prefix}-dashboard"

  dashboard_body = jsonencode({
    widgets = [
      {
        type = "metric", x = 0, y = 0, width = 12, height = 6
        properties = {
          title   = "EC2 CPU Utilization (%)"
          region  = var.aws_region
          stat    = "Average"
          period  = 300
          metrics = [["AWS/EC2", "CPUUtilization", "InstanceId", aws_instance.web.id]]
        }
      },
      {
        type = "metric", x = 12, y = 0, width = 12, height = 6
        properties = {
          title   = "EC2 Network In (bytes)"
          region  = var.aws_region
          stat    = "Average"
          period  = 300
          metrics = [["AWS/EC2", "NetworkIn", "InstanceId", aws_instance.web.id]]
        }
      }
    ]
  })
}
