# Lesson 8 · AWS Access Keys — Programmatic Access to AWS
**एक्सेस की के माध्यम से AWS से जुड़ना**

`Part 2 · AWS Access & Security` · ⏱ 60 min · 💰 Free · Level: Intermediate

![Lesson 8](../../images/lesson-08-access-keys.png)

## 🎯 Learning objectives
- Explain what an Access Key ID and a Secret Access Key are.
- Create an access key for an IAM user and configure the AWS CLI.
- Use the keys from Python (boto3) and verify with `sts get-caller-identity`.

## 📖 The story
Meera: *"Can my Python application access AWS? I need to upload bakery order files to S3."*
Teacher: *"Yes — with **Access Keys**. They give **programmatic access**, so our application can
use AWS services."*

## 🧠 Concepts

### What are access keys? (panel 1)
| Part | Looks like | Think of it as |
|------|-----------|----------------|
| **Access Key ID** | `AKIAIOSFODNN7EXAMPLE` | username (public-ish) |
| **Secret Access Key** | `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY` | password (**secret!**) |

Used for access via **code, CLI or SDK**. Each IAM user can have **up to two** access keys (handy for rotation).
Console login uses a *password*; programs use *access keys*.

> The two sample values above come from AWS's own documentation — they are **fake**. Real keys must never appear in slides, chats or Git.

### When to use access keys (panel 2)
Applications (Python, Java…) · AWS CLI · automation scripts (backup/upload) · CI/CD (GitHub Actions, Jenkins) · tools like Terraform/Ansible · your own software. 
**But:** for code running *inside* AWS (EC2, Lambda, ECS) use **IAM roles** instead — no keys at all (panel 8).

### How keys reach your code
boto3/CLI look for credentials in this order: code parameters (avoid!) → **environment variables** → shared file `~/.aws/credentials` (written by `aws configure`) → **IAM role** of the compute service.

## 🛠️ Hands-on

### Step 1 — Create the key (panel 3 & 4)
1. Console → **IAM ▸ Users ▸ meera-dev** (or your own IAM user — not root).
2. Open the **Security credentials** tab → **Create access key**.
3. Use case: **Command Line Interface (CLI)** → tick the confirmation → *Next* → optional description tag → **Create access key**.
4. **Download .csv / copy both values now.** The secret is **never shown again** (panel 5).
5. Store them in a password manager. Do not paste them into chat or code.

### Step 2 — Configure the AWS CLI (panel 7)
```bash
aws configure
#AWS_ACCESS_KEY_ID=YOUR_AWS_ACCESS_KEY_ID
#AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_ACCESS_KEY
# Default region name [None]:    ap-south-1
# Default output format [None]:  json

aws sts get-caller-identity          # proves the keys work and shows WHO you are
aws s3 ls                            # lists buckets (empty or error = permissions, see below)
```
The CLI stored keys in `~/.aws/credentials` (Windows: `C:\Users\<you>\.aws\credentials`).

### Step 3 — Use the keys in Python (panel 6)
Install boto3 (already in `requirements.txt`) and run the verified scripts:
```bash
python scripts/check_identity.py      # who am I?
python scripts/list_buckets.py        # same as the slide's "List S3 buckets" example
```
They contain **no keys** — boto3 finds the ones from `aws configure` automatically. Open
`scripts/_common.py` and see how little code is needed.

### Step 4 — Meera's real flow (panel 9)
`Bakery website (Python app)` → `Access keys` → `S3 bucket (product images)` → `RDS (orders)`.
Upload an image:
```bash
python scripts/s3_upload.py my-cake.png <your-bucket-name>
```
(Create a bucket first in the console: *S3 ▸ Create bucket* → globally unique name, Region `ap-south-1`.)

### Step 5 — Practice good hygiene
- IAM ▸ Users ▸ your user ▸ Security credentials shows **Last used** — review it.
- Create a second key, switch your tools to it, then **Deactivate → Delete** the first (that is *rotation*).

## 📁 Files for this lesson
`scripts/check_identity.py` · `scripts/list_buckets.py` · `scripts/s3_upload.py` · `scripts/_common.py`

## ⚠️ Common mistakes & fixes
| Symptom | Cause | Fix |
|---------|-------|-----|
| `NoCredentialsError` | No keys found | Run `aws configure` or fill `.env` |
| `InvalidClientTokenId` / `SignatureDoesNotMatch` | Typo, extra space, wrong secret | Re-copy; recreate the key |
| `AccessDenied` on `ListBuckets` | IAM user lacks `s3:ListAllMyBuckets` | Attach `AmazonS3ReadOnlyAccess` (Lesson 7) |
| Works in CLI, fails in code | Different profile/Region | `aws configure list`; set `AWS_REGION` |
| Created keys for **root** | Dangerous | Delete them; use IAM user |

## ✅ Best practices (panel 8)
Never share keys · **never hard-code keys** · use environment variables or Systems Manager · use **IAM roles instead of keys** for EC2/Lambda · rotate regularly · delete unused keys · least privilege · enable CloudTrail.

## 📝 Quiz
1. Which key part is secret?
2. How many access keys can one IAM user have?
3. When is an IAM role better than access keys?
4. Which command proves your credentials work?
5. Where does `aws configure` store keys?

<details><summary>Show answers</summary>

1. Secret Access Key.  2. Two.  3. For code running on EC2/ECS/Lambda.  4. `aws sts get-caller-identity`.  5. `~/.aws/credentials`.
</details>

## 🏠 Assignment
Create a key for a least-privilege IAM user, run `check_identity.py` and `list_buckets.py`, upload one image, then **rotate** and delete the old key. Write the steps in your own words.

## 🔑 Key takeaway
Access keys provide programmatic access to AWS. Use them for apps, CLI and automation; keep the
secret safe and prefer IAM roles for AWS services like EC2 and Lambda.

**हिंदी में सार:** Access Key ID = username, Secret Key = password। इनसे Python/CLI से AWS चलता है।
Secret key कभी share या code में न लिखें; EC2/Lambda के लिए IAM Role बेहतर है।

⬅️ [Lesson 7](07-iam.md) · ➡️ **Next:** [Lesson 9 — The Dangerous Secret-Key Mistake](09-secret-key-mistake.md)
