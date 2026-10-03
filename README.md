# ☁️ AWS + DevOps Business Solutions — Meera's Bakery (Zero to Hero)

A hands-on, story-based course for students. **Meera** wants to take her bakery online.
Her teacher guides her from *"Why do we need the cloud?"* all the way to a **fully automated
CI/CD pipeline running on AWS**, with security and monitoring built in.

Every lesson has: an infographic → plain-language explanation → step-by-step hands-on →
working code in this project → common mistakes → quiz → assignment.

> 🇮🇳 Bilingual friendly: each lesson ends with a short **हिंदी में सार** (Hindi summary).

---

## 🗺️ Course map

### Part 1 — AWS Foundations
| # | Lesson | Infographic | Hands-on in this project |
|---|--------|-------------|---------------------------|
| 1 | [Business Problem: Why the Cloud?](docs/lessons/01-business-problem-why-cloud.md) | [image](images/lesson-01-business-problem.png) | `scripts/lesson01_capacity_simulation.py` |
| 2 | [What is AWS?](docs/lessons/02-what-is-aws.md) | [image](images/lesson-02-what-is-aws.png) | Create account, budget alert, login |
| 3 | [Cloud Service Models (IaaS/PaaS/SaaS)](docs/lessons/03-cloud-service-models.md) | [image](images/lesson-03-cloud-service-models.png) | Classification exercise |
| 4 | [AWS Services & Categories](docs/lessons/04-services-and-categories.md) | [image](images/lesson-04-services-categories.png) | Architecture mapping |
| 5 | [AWS Regions & Availability Zones](docs/lessons/05-aws-regions.md) | [image](images/lesson-05-aws-regions.png) | `scripts/list_regions.py` |
| 6 | [AWS Management Console](docs/lessons/06-aws-console.md) | [image](images/lesson-06-aws-console.png) | Console tour + install AWS CLI |

### Part 2 — AWS Access & Security → DevOps
| # | Lesson | Infographic | Hands-on in this project |
|---|--------|-------------|---------------------------|
| 7 | [IAM — Identity & Access Management](docs/lessons/07-iam.md) | [image](images/lesson-07-iam.png) | `scripts/iam_setup.sh`, `iam/*.json` |
| 8 | [AWS Access Keys](docs/lessons/08-access-keys.md) | [image](images/lesson-08-access-keys.png) | `scripts/check_identity.py`, `list_buckets.py` |
| 9 | [The Dangerous Secret-Key Mistake](docs/lessons/09-secret-key-mistake.md) | [image](images/lesson-09-secret-key-mistake.png) | `scripts/simple_secret_scan.py`, pre-commit |
| 10 | [Python + .env for AWS Credentials](docs/lessons/10-python-dotenv.md) | [image](images/lesson-10-python-dotenv.png) | `.env.example`, `app/config.py`, `s3_upload.py` |
| 11 | [SSM Parameter Store](docs/lessons/11-ssm-parameter-store.md) | [image](images/lesson-11-ssm-parameter-store.png) | `scripts/ssm_*.py` |
| 12 | [Deploy with GitHub Actions (CI/CD)](docs/lessons/12-github-actions-cicd.md) | [image](images/lesson-12-github-actions-cicd.png) | `.github/workflows/deploy.yml` |
| 13 | [Infrastructure as Code with Terraform](docs/lessons/13-terraform.md) | [A](images/lesson-13a-terraform-iac.png) · [B](images/lesson-13b-terraform-iac.png) | `terraform/` |
| 14 | [Complete DevOps Pipeline](docs/lessons/14-complete-devops-pipeline.md) | [image](images/lesson-14-complete-devops-pipeline.png) | `Dockerfile`, `pipeline-docker.yml` |
| 15 | [Monitoring & Logging with CloudWatch](docs/lessons/15-cloudwatch.md) | [image](images/lesson-15-cloudwatch.png) | `scripts/cw_*.py`, `terraform/monitoring.tf` |
| 16 | [Next: Auto Scaling & High Availability](docs/lessons/16-next-auto-scaling.md) | — | Preview (infographic coming) |

---

## 🚀 Quick start (5 minutes, no AWS account needed)

```bash
# 1. open the folder in VS Code      →  File ▸ Open Folder ▸ aws-devops-meeras-bakery
# 2. create a virtual environment
python -m venv .venv
.venv\Scripts\activate            # Windows PowerShell   (macOS/Linux: source .venv/bin/activate)

# 3. install packages
pip install -r requirements-dev.txt

# 4. run the tests (they use a fake AWS, so they are free and safe)
python -m pytest -v

# 5. run the bakery API
python -m uvicorn app.main:app --reload
#    open http://127.0.0.1:8000  and  http://127.0.0.1:8000/docs
```

Then read **[docs/00-START-HERE.md](docs/00-START-HERE.md)** and follow the lessons in order.

---

## 📁 Project structure (file-wise guide)

```
aws-devops-meeras-bakery/
├── README.md                      ← you are here
├── docs/
│   ├── 00-START-HERE.md           ← study plan, how to use this course
│   ├── 01-environment-setup.md    ← install VS Code, Python, Git, AWS CLI, Terraform, Docker
│   ├── 02-capstone-walkthrough.md ← ALL lessons in one end-to-end build (zero → hero)
│   ├── glossary.md                ← every term explained simply
│   ├── cheatsheet.md              ← AWS CLI / Terraform / Docker / Git commands
│   ├── troubleshooting.md         ← common errors and fixes
│   ├── teaching-notes.md          ← for trainers: simplifications in the slides
│   └── lessons/                   ← 16 lesson documents (one per infographic)
├── images/                        ← the 16 infographics (lesson-01 … lesson-15)
├── app/                           ← Meera's Bakery FastAPI backend
│   ├── main.py                    ← API endpoints (/health, /products, /products/upload)
│   ├── config.py                  ← .env + SSM Parameter Store loading (Lessons 10, 11)
│   ├── aws_clients.py             ← boto3 client — NO keys in code (Lesson 9)
│   └── logging_config.py          ← logging for CloudWatch (Lesson 15)
├── static/index.html              ← static website deployed to S3 (Lesson 12)
├── tests/                         ← pytest + moto (fake AWS)
├── scripts/                       ← small hands-on programs (one per lesson topic)
├── iam/                           ← example IAM policies (Lesson 7, 11, 12)
├── terraform/                     ← infrastructure code (Lessons 13, 15)
├── .github/workflows/             ← ci.yml, deploy.yml, pipeline-docker.yml (Lessons 12, 14)
├── Dockerfile                     ← container image (Lesson 14)
├── .env.example                   ← template for secrets (Lesson 10)  — copy to .env
├── .gitignore  .dockerignore  .pre-commit-config.yaml
└── .vscode/                       ← recommended extensions, debug + task configs
```

## 💰 Cost & safety rules (read once, follow always)

1. **Never use the root user** for daily work (Lesson 7). Turn on **MFA** on root.
2. Create an **AWS Budget alert** (Lesson 2) *before* creating anything.
3. **Never commit** `.env`, `*.pem`, or access keys (Lesson 9). Run `python scripts/simple_secret_scan.py`.
4. Anything you create with Terraform → finish the lesson with **`terraform destroy`**.
5. Delete practice IAM users, access keys, S3 buckets, EC2 instances and ECR images when done.
6. Lessons 1–6 and most of 7–11 cost **nothing**. Lessons 13–15 create real resources — small, but not always free.

## 🎓 Prerequisites
Basic computer skills. Python basics help (variables, functions, `pip`) but each step is explained.
No prior AWS, Docker, Git or Terraform knowledge is assumed.
