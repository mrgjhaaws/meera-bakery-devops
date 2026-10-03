# Lesson 13, panel 6/8 - input variables (same code for dev / test / prod)

variable "aws_region" {
  description = "AWS region to deploy into"
  type        = string
  default     = "ap-south-1"
}

variable "environment" {
  description = "Environment name: dev, test or prod"
  type        = string
  default     = "dev"

  validation {
    condition     = contains(["dev", "test", "prod"], var.environment)
    error_message = "environment must be dev, test or prod."
  }
}

variable "instance_type" {
  description = "EC2 instance size for the bakery web server"
  type        = string
  default     = "t3.micro"
}

variable "key_name" {
  description = "Name of an existing EC2 key pair for SSH (leave empty to disable SSH keys)"
  type        = string
  default     = ""
}

variable "allowed_ssh_cidr" {
  description = "CIDR allowed to SSH, e.g. 203.0.113.10/32 (your IP). Empty = no SSH rule."
  type        = string
  default     = ""
}

variable "alert_email" {
  description = "E-mail that receives CloudWatch alarm notifications (empty = no subscription)"
  type        = string
  default     = ""
}

variable "enable_public_static_site" {
  description = "true = make the static S3 bucket a public website (learning only)"
  type        = bool
  default     = false
}
