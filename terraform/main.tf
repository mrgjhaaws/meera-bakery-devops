# Lesson 13, panel 5 - the resources (S3 + EC2) plus the supporting pieces
# that Lessons 11, 14 and 15 need (SSM parameters, ECR, IAM role, security group).

locals {
  name_prefix = "meera-bakery-${var.environment}"
}

# Bucket names are global across ALL of AWS, so add a random suffix.
resource "random_id" "suffix" {
  byte_length = 3
}

# ---------------------------------------------------------------- S3 (storage)
resource "aws_s3_bucket" "images" {
  bucket = "${local.name_prefix}-images-${random_id.suffix.hex}"
  # lets `terraform destroy` delete the bucket even if it has files (classroom use)
  force_destroy = true

  tags = { Name = "Meera Bakery Product Images" }
}

resource "aws_s3_bucket_public_access_block" "images" {
  bucket                  = aws_s3_bucket.images.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket" "static" {
  bucket        = "${local.name_prefix}-static-${random_id.suffix.hex}"
  force_destroy = true

  tags = { Name = "MeeraBakery-S3-Static" }
}

resource "aws_s3_bucket_public_access_block" "static" {
  bucket                  = aws_s3_bucket.static.id
  block_public_acls       = !var.enable_public_static_site
  block_public_policy     = !var.enable_public_static_site
  ignore_public_acls      = !var.enable_public_static_site
  restrict_public_buckets = !var.enable_public_static_site
}

resource "aws_s3_bucket_website_configuration" "static" {
  count  = var.enable_public_static_site ? 1 : 0
  bucket = aws_s3_bucket.static.id

  index_document {
    suffix = "index.html"
  }
}

resource "aws_s3_bucket_policy" "static_public_read" {
  count      = var.enable_public_static_site ? 1 : 0
  bucket     = aws_s3_bucket.static.id
  depends_on = [aws_s3_bucket_public_access_block.static]

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Sid       = "PublicReadForWebsite"
      Effect    = "Allow"
      Principal = "*"
      Action    = "s3:GetObject"
      Resource  = "${aws_s3_bucket.static.arn}/*"
    }]
  })
}

# ------------------------------------------------- SSM Parameter Store (Lesson 11)
resource "aws_ssm_parameter" "region" {
  name  = "/meera-bakery/${var.environment}/AWS_REGION"
  type  = "String"
  value = var.aws_region
}

resource "aws_ssm_parameter" "bucket" {
  name  = "/meera-bakery/${var.environment}/S3_BUCKET"
  type  = "String"
  value = aws_s3_bucket.images.bucket
}

# ----------------------------------------------------------- ECR (Lesson 14)
resource "aws_ecr_repository" "bakery" {
  name                 = "meera-bakery"
  image_tag_mutability = "MUTABLE"
  force_delete         = true # classroom use: allow destroy even if images exist

  image_scanning_configuration {
    scan_on_push = true
  }
}

# ------------------------------------------- IAM role for EC2: NO keys on the server
data "aws_iam_policy_document" "ec2_assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "web" {
  name               = "${local.name_prefix}-web-role"
  assume_role_policy = data.aws_iam_policy_document.ec2_assume.json
}

data "aws_caller_identity" "current" {}

data "aws_iam_policy_document" "web_access" {
  statement {
    sid       = "ListImagesBucket"
    actions   = ["s3:ListBucket"]
    resources = [aws_s3_bucket.images.arn]
  }
  statement {
    sid       = "ReadWriteProductImages"
    actions   = ["s3:GetObject", "s3:PutObject"]
    resources = ["${aws_s3_bucket.images.arn}/products/*"]
  }
  statement {
    sid     = "ReadBakeryParameters"
    actions = ["ssm:GetParameter", "ssm:GetParameters", "ssm:GetParametersByPath"]
    resources = [
      "arn:aws:ssm:${var.aws_region}:${data.aws_caller_identity.current.account_id}:parameter/meera-bakery/${var.environment}/*"
    ]
  }
}

resource "aws_iam_role_policy" "web_access" {
  name   = "bakery-app-access"
  role   = aws_iam_role.web.id
  policy = data.aws_iam_policy_document.web_access.json
}

# Managed policies: pull images from ECR, ship logs/metrics, optional Session Manager shell
resource "aws_iam_role_policy_attachment" "ecr_read" {
  role       = aws_iam_role.web.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
}

resource "aws_iam_role_policy_attachment" "cloudwatch_agent" {
  role       = aws_iam_role.web.name
  policy_arn = "arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy"
}

resource "aws_iam_role_policy_attachment" "ssm_core" {
  role       = aws_iam_role.web.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

resource "aws_iam_instance_profile" "web" {
  name = "${local.name_prefix}-web-profile"
  role = aws_iam_role.web.name
}

# ------------------------------------------------------------ network + EC2
data "aws_vpc" "default" {
  default = true
}

resource "aws_security_group" "web" {
  name        = "${local.name_prefix}-web-sg"
  description = "Allow web traffic to Meera Bakery"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    description = "HTTP from anywhere"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  dynamic "ingress" {
    for_each = var.allowed_ssh_cidr == "" ? [] : [var.allowed_ssh_cidr]
    content {
      description = "SSH from my IP only"
      from_port   = 22
      to_port     = 22
      protocol    = "tcp"
      cidr_blocks = [ingress.value]
    }
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Latest Amazon Linux 2023 AMI for this region (AMI IDs differ per region,
# so never hard-code one like in the slide - look it up instead).
data "aws_ssm_parameter" "al2023" {
  name = "/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64"
}

resource "aws_instance" "web" {
  ami                    = data.aws_ssm_parameter.al2023.value
  instance_type          = var.instance_type
  key_name               = var.key_name == "" ? null : var.key_name
  iam_instance_profile   = aws_iam_instance_profile.web.name
  vpc_security_group_ids = [aws_security_group.web.id]
  monitoring             = false # true = detailed monitoring (1-minute metrics, extra cost)

  user_data = templatefile("${path.module}/user_data.sh.tpl", {
    region = var.aws_region
  })

  metadata_options {
    http_tokens = "required" # IMDSv2 only (security best practice)
  }

  tags = {
    Name = "Meera-Bakery-Web"
  }
}
