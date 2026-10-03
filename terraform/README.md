# Terraform - Meera's Bakery infrastructure (Lesson 13)

```bash
cd terraform
terraform init                          # download providers
terraform fmt                           # tidy the code
terraform validate                      # check syntax
terraform plan  -var-file=envs/dev.tfvars     # preview (nothing is created)
terraform apply -var-file=envs/dev.tfvars     # create (type: yes)
terraform output                        # see IPs / bucket names
terraform destroy -var-file=envs/dev.tfvars   # DELETE everything when done
```

| File | Purpose |
|------|---------|
| `providers.tf` | Terraform + AWS provider, default tags |
| `variables.tf` | Inputs (region, environment, instance type...) |
| `main.tf` | S3 buckets, SSM parameters, ECR, IAM role, security group, EC2 |
| `monitoring.tf` | CloudWatch log group, alarm, SNS, dashboard (Lesson 15) |
| `outputs.tf` | Values to copy into `.env` and GitHub secrets |
| `envs/*.tfvars` | Values for dev / test / prod |
| `user_data.sh.tpl` | Boot script: installs Docker on the server |

> **Cost warning:** a `t2.micro`/`t3.micro` is Free-Tier eligible only for new accounts and
> limited hours. Always run `terraform destroy` after practice.
