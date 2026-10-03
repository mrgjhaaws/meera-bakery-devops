# Cheat Sheet

## AWS CLI
```bash
aws configure                                   # save keys + region
aws sts get-caller-identity                     # who am I?
aws ec2 describe-regions --query "Regions[].{Name:RegionName}" --output table
aws s3 ls                                       # list buckets
aws s3 mb s3://my-unique-bucket-name            # make bucket
aws s3 cp cake.png s3://my-bucket/products/     # upload
aws s3 sync ./static s3://my-bucket --delete    # mirror a folder
aws iam list-users
aws iam list-access-keys --user-name meera-dev
aws ssm put-parameter --name /meera-bakery/dev/AWS_REGION --type String --value ap-south-1
aws ssm get-parameters-by-path --path /meera-bakery/dev --with-decryption
aws ec2 describe-instances --query "Reservations[].Instances[].[InstanceId,State.Name,PublicIpAddress]" --output table
aws cloudwatch describe-alarms --query "MetricAlarms[].[AlarmName,StateValue]" --output table
aws logs tail /aws/app/meera-bakery --follow
aws ecr describe-repositories
```

## Git
```bash
git init && git add . && git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/<you>/meera-bakery.git
git push -u origin main
git status            git log --oneline            git diff
git rm --cached .env  # stop tracking a file you committed by mistake (then ROTATE the key!)
```

## Python
```bash
python -m venv .venv                 pip install -r requirements-dev.txt
python -m pytest -v                  python -m uvicorn app.main:app --reload
```

## Docker
```bash
docker build -t meera-bakery:local .
docker run --rm -p 8000:8000 --env-file .env meera-bakery:local
docker ps          docker logs -f bakery          docker stop bakery          docker rm bakery
docker images      docker system prune
```

## Terraform
```bash
terraform init            terraform fmt            terraform validate
terraform plan  -var-file=envs/dev.tfvars
terraform apply -var-file=envs/dev.tfvars
terraform output          terraform state list
terraform destroy -var-file=envs/dev.tfvars
```

## GitHub Actions (YAML skeleton)
```yaml
name: My workflow
on: { push: { branches: [main] } }
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: echo "hello"
```

## Quick rules
| Situation | Do this |
|-----------|---------|
| Need AWS access from code on EC2/ECS/Lambda | Use an **IAM role** — no keys |
| Need AWS access from your laptop | IAM user/SSO + `aws configure` or `.env` |
| Key leaked | **Rotate → delete old → clean history → check CloudTrail** |
| Config differs per environment | `.env.<env>`, SSM paths `/app/<env>/...`, `*.tfvars` |
| Practice is over | `terraform destroy`, delete keys/buckets/instances |
