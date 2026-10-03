#!/bin/bash
# Runs once when the EC2 instance first boots.
# Meera's Bakery - Web Server + Docker + ECR
set -euxo pipefail

# --------------------------------------------------
# 1. Install Apache Web Server
# --------------------------------------------------
dnf install -y httpd

systemctl enable --now httpd

# --------------------------------------------------
# 2. Deploy Meera's Bakery homepage
# --------------------------------------------------
cat >/var/www/html/index.html <<'HTML'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Meera's Bakery</title>
</head>
<body>
    <h1>Welcome to Meera Bakery</h1>
    <p>Deployed on AWS EC2 with Terraform</p>
    <p>Apache Web Server is running successfully.</p>
</body>
</html>
HTML

systemctl restart httpd

# --------------------------------------------------
# 3. Install Docker
# --------------------------------------------------
dnf install -y docker

systemctl enable --now docker

usermod -aG docker ec2-user

# --------------------------------------------------
# 4. ECR Login Helper
# --------------------------------------------------
cat >/usr/local/bin/ecr-login <<'SCRIPT'
#!/bin/bash
# usage: ecr-login 123456789012.dkr.ecr.${region}.amazonaws.com
aws ecr get-login-password --region ${region} | docker login --username AWS --password-stdin "$1"
SCRIPT

chmod +x /usr/local/bin/ecr-login