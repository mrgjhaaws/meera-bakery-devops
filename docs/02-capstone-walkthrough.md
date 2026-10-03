# 02 · Capstone — Zero to Hero in one walkthrough

Do this **after** finishing the lessons (or use it as a fast-track). You will build Meera's Bakery
end to end: secure access → configuration → infrastructure as code → CI/CD → monitoring → cleanup.
Estimated time: 3–4 hours. Cost: a few rupees if you clean up the same day.

```
 You ──push──► GitHub ──Actions──► tests ──► Docker image ──► ECR ──► EC2 (Docker) ──► Customers
                                                   ▲                      │
                              Terraform creates:   │  S3 · IAM role · SSM · SG · CloudWatch
                                                   └──────────────────────┘ alarms ──► SNS ──► your e-mail
```

## Phase 0 — Prepare (Lessons 2, 6, setup guide)
- [ ] AWS account, **MFA on root**, **budget alert**
- [ ] Tools installed (`python`, `git`, `aws`, `terraform`, `docker`)
- [ ] `python -m pytest -q` → 6 passed

## Phase 1 — Secure access (Lessons 7, 8, 9)
- [ ] Create IAM group `admins` + your admin user (stop using root)
- [ ] Create IAM user `meera-dev` with limited rights; MFA on
- [ ] Access key for your admin/practice user → `aws configure`
- [ ] `python scripts/check_identity.py` shows your IAM user ARN
- [ ] `python scripts/simple_secret_scan.py .` → *No secrets found.*
- [ ] `git init`, confirm `.env` is ignored: `git check-ignore -v .env`

## Phase 2 — Local app with safe configuration (Lesson 10)
- [ ] `cp .env.example .env` and fill values (leave `USE_PARAMETER_STORE=false`)
- [ ] Run `python -m uvicorn app.main:app --reload` → `/health`, `/docs`
- [ ] Create a bucket (console) and set `S3_BUCKET`; upload an image through `/docs`

## Phase 3 — Infrastructure as Code (Lessons 13, 4, 5)
```bash
cd terraform
terraform init && terraform validate
terraform plan  -var-file=envs/dev.tfvars \
  -var key_name=<keypair> -var allowed_ssh_cidr=<your-ip>/32 -var alert_email=<you@example.com>
terraform apply -var-file=envs/dev.tfvars \
  -var key_name=<keypair> -var allowed_ssh_cidr=<your-ip>/32 -var alert_email=<you@example.com>
terraform output
```
- [ ] Confirm the SNS e-mail subscription
- [ ] Verify in console: S3, EC2, IAM role, ECR, SSM parameters, CloudWatch alarm
- [ ] Put `images_bucket` into `.env` → `python scripts/list_buckets.py`

## Phase 4 — Configuration from Parameter Store (Lesson 11)
- [ ] `python scripts/ssm_get_parameters.py dev` shows the two parameters Terraform created
- [ ] Set `USE_PARAMETER_STORE=true`, run the API, check `/config`

## Phase 5 — CI/CD (Lessons 12, 14)
- [ ] Create GitHub repo, push, watch **CI** go green
- [ ] Deployer IAM user + secrets (`AWS_*`, `ECR_URI`, `EC2_HOST`, `EC2_USER`, `EC2_SSH_KEY`) + variable `DEPLOY_ENABLED=true`
- [ ] Push a change → pipeline: test → build → ECR → EC2
- [ ] Open `http://<EC2_HOST>/health`

## Phase 6 — Monitoring (Lesson 15)
- [ ] Run `stress-ng` on EC2, watch the alarm → e-mail → OK again
- [ ] Look at `/aws/app/meera-bakery` logs and the dashboard

## Phase 7 — Cleanup (do not skip!)
```bash
cd terraform && terraform destroy -var-file=envs/dev.tfvars   # same -var flags you used for apply
```
- [ ] Delete practice IAM users and **access keys**
- [ ] Delete any manually created S3 buckets, ECR images, log groups, parameters
- [ ] Remove GitHub secrets (or the repo)
- [ ] Check **Billing ▸ Bills** tomorrow — should be ~0

## 🎓 Final reflection (write 10 lines)
1. Which lesson changed how you think the most?
2. Where could a secret have leaked in your project, and how did you prevent it?
3. What would you add next? (Lesson 16: load balancer + Auto Scaling.)
