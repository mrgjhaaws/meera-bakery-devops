# Glossary — simple words for big ideas

| Term | Simple meaning | Lesson |
|------|----------------|--------|
| **Cloud computing** | Renting computing power (servers, storage, databases) over the internet instead of buying it | 1 |
| **On-premise** | Servers you own and keep in your own building | 1 |
| **Scalability** | Ability to handle more (or less) load by adding (or removing) capacity | 1 |
| **High availability** | Service keeps running even if one part fails | 1, 5 |
| **Pay-as-you-go** | You pay only for what you use, like electricity | 2 |
| **AWS** | Amazon Web Services — Amazon's cloud platform | 2 |
| **IaaS** | You rent infrastructure (virtual server); you manage OS + app | 3 |
| **PaaS** | You bring only code; the platform runs it | 3 |
| **SaaS** | Ready-made software used in a browser (Gmail) | 3 |
| **EC2** | Virtual servers | 4 |
| **S3** | Object storage for files/images (buckets) | 4 |
| **RDS** | Managed relational databases | 4 |
| **VPC** | Your private network inside AWS | 4 |
| **Lambda** | Run code without managing servers (serverless) | 4 |
| **Region** | A physical location (e.g. Mumbai `ap-south-1`) containing several data-center groups | 5 |
| **Availability Zone (AZ)** | One or more separate data centers inside a Region | 5 |
| **Latency** | Delay between a user's request and the response | 5 |
| **Data residency** | Law/rule that data must stay inside a country or region | 5 |
| **Management Console** | The AWS website where you click to manage services | 6 |
| **IAM** | Service that controls *who* can do *what* in AWS | 7 |
| **Root user** | The all-powerful account owner login — do not use daily | 7 |
| **User / Group / Role** | Person or app identity / set of users / temporary identity assumed by services | 7 |
| **Policy** | JSON document listing allowed or denied actions | 7 |
| **Least privilege** | Give only the permissions that are needed | 7 |
| **MFA** | Second proof of identity (code from an app) | 7 |
| **Access Key ID** | Public part of programmatic credentials (like a username) | 8 |
| **Secret Access Key** | Private part (like a password) — never share | 8, 9 |
| **SDK / boto3** | Library to call AWS from code / the Python one | 8 |
| **CLI** | Command Line Interface — type commands to use AWS | 8 |
| **Hard-coding** | Writing secrets directly in source code (dangerous!) | 9 |
| **Key rotation** | Replacing keys regularly | 9 |
| **.env file** | Text file with `NAME=value` settings kept out of Git | 10 |
| **Environment variable** | A named value an operating system provides to programs | 10 |
| **python-dotenv** | Library that loads `.env` into environment variables | 10 |
| **.gitignore** | List of files Git must never upload | 10 |
| **SSM Parameter Store** | AWS service to store configuration/secrets centrally | 11 |
| **SecureString** | Encrypted parameter type (uses KMS) | 11 |
| **KMS** | Key Management Service — encryption keys | 11 |
| **CI** | Continuous Integration — automatically build & test on every push | 12 |
| **CD** | Continuous Deployment — automatically release after tests pass | 12 |
| **GitHub Actions** | GitHub's built-in automation (workflows) | 12 |
| **Workflow / Job / Step** | The YAML file / a group of steps on one machine / one command or action | 12 |
| **GitHub Secrets** | Encrypted storage for passwords/keys used in workflows | 12 |
| **IaC** | Infrastructure as Code — define servers/networks in files | 13 |
| **Terraform** | Open-source IaC tool by HashiCorp | 13 |
| **Provider** | Terraform plugin for a platform (AWS) | 13 |
| **State file** | Terraform's record of what it created | 13 |
| **plan / apply / destroy** | Preview / create / delete infrastructure | 13 |
| **Docker / Image / Container** | Packaging tool / packaged app / running instance of an image | 14 |
| **ECR** | Elastic Container Registry — storage for Docker images | 14 |
| **ECS / EKS** | AWS services that run containers | 14 |
| **CloudWatch** | Monitoring: metrics, logs, alarms, dashboards | 15 |
| **Metric / Log / Alarm / Dashboard** | A number over time / text records / alert rule / visual summary | 15 |
| **SNS** | Simple Notification Service — sends e-mail/SMS alerts | 15 |
| **CloudTrail** | Records *who* did *what* in your AWS account (audit) | 7, 9 |
| **Auto Scaling** | Automatically add/remove servers with demand | 16 |
| **Load balancer (ALB)** | Spreads traffic over several servers | 16 |
