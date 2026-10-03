# Lesson 13, panel 8 - values printed after `terraform apply`

output "web_public_ip" {
  description = "Public IP of the bakery web server"
  value       = aws_instance.web.public_ip
}

output "web_instance_id" {
  description = "Use this with scripts/cw_create_alarm.py"
  value       = aws_instance.web.id
}

output "images_bucket" {
  description = "Put this in S3_BUCKET (.env) for the app"
  value       = aws_s3_bucket.images.bucket
}

output "static_bucket" {
  description = "GitHub secret STATIC_BUCKET for the static-site workflow"
  value       = aws_s3_bucket.static.bucket
}

output "static_website_url" {
  description = "Only available when enable_public_static_site = true"
  value       = try("http://${aws_s3_bucket_website_configuration.static[0].website_endpoint}", "disabled")
}

output "ecr_repository_url" {
  description = "GitHub secret ECR_URI for the Docker pipeline"
  value       = aws_ecr_repository.bakery.repository_url
}

output "alerts_topic_arn" {
  value = aws_sns_topic.alerts.arn
}
