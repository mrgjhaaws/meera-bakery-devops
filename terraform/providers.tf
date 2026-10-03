# Lesson 13, panel 3/4 - AWS provider configuration
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.5"
    }
  }
}

provider "aws" {
  region = var.aws_region

  # Every resource gets these tags automatically (Lesson 13, panel 7 "Tags")
  default_tags {
    tags = {
      Project     = "meera-bakery"
      Environment = var.environment
      ManagedBy   = "terraform"
    }
  }
}
