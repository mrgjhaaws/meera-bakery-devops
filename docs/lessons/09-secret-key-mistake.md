# Lesson 9 · The Dangerous Secret-Key Mistake
**गुप्त कुंजी (Secret Key) की सबसे बड़ी गलती**

`Part 2 · AWS Access & Security` · ⏱ 60 min · 💰 Free · Level: Intermediate · 🔥 *Most important security lesson*

![Lesson 9](../../images/lesson-09-secret-key-mistake.png)

## 🎯 Learning objectives
- Recognise hard-coded credentials and explain the damage they cause.
- List where keys commonly leak.
- Follow the **5-step response** to an exposed key.
- Prevent leaks with `.gitignore`, scanning and pre-commit hooks.

## 📖 The story
Meera: *"Sir, I put my AWS Access Key and Secret Key in my Python script, so now I can upload
bakery images to S3!"* Teacher: *"This is a **very big mistake**. Never share a Secret Key in code,
on GitHub or in front of anyone — your whole AWS account can be at risk."*

## 🧠 Concepts

### The common mistake (panel 1)
```python
# ❌ DANGEROUS — never do this
import boto3
s3 = boto3.client('s3',
    AWS_ACCESS_KEY_ID=YOUR_AWS_ACCESS_KEY_ID,
AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_ACCESS_KEY,
    region_name='ap-south-1')
```
Credentials are visible in the code → if the code is shared, keys leak → anyone can use them.
(The values shown are AWS's fake documentation examples.)

### What can happen? (panels 2–3)
An attacker can: access your account · create/delete/modify resources (EC2, S3, RDS) · **steal customer data** · launch costly resources (e.g. **crypto-mining** servers → huge bill) · delete your data · use your account for malicious activity (damaging your reputation).

*Automated bots scan public GitHub continuously — leaked keys can be abused within minutes.* AWS also scans public repos and may apply a quarantine policy to a leaked key and e-mail you — treat that e-mail as an emergency.

### Real incident patterns (panel 4)
GitHub (keys committed to public repos) · Stack Overflow (keys pasted into questions) · blogs/tutorials (screenshots) · browser console/logs/error messages.

### Where keys get exposed (panel 5)
Source code (GitHub/GitLab) · config files (`config.py`, `settings.json`) · logs and error messages · screenshots and videos · chat, e-mail, documents · shared computers · blogs, forums, Q&A sites · online tutorials and courses.

### 🚨 How to remove exposed keys — the 5 steps (panel 6)
| Step | Action | How |
|------|--------|-----|
| 1 | **Rotate the keys** | IAM ▸ Users ▸ Security credentials ▸ create a new key; **deactivate** the old one |
| 2 | **Remove from code** | Delete the hard-coded values; load from environment/SSM |
| 3 | **Check Git history** | Removing the line is not enough — old commits still contain it. Use `git filter-repo` or **BFG Repo-Cleaner**, then force-push |
| 4 | **Revoke access** | **Delete** the exposed key in AWS immediately |
| 5 | **Monitor** | Check **CloudTrail** for suspicious activity; check Billing and all Regions |

> ⚠️ **Order matters in real life:** *revoke first* (steps 1 & 4 — takes 1 minute), then clean code and history. Once a key was public, assume it was copied; rewriting history does **not** un-leak it.

### Safer ways (panel 7–9)
Environment variables (`.env`, Lesson 10) · **Systems Manager Parameter Store** (Lesson 11) · **IAM roles** for EC2/Lambda/ECS · **Secrets Manager** for database passwords etc. · never hard-code · least privilege · monitor with CloudTrail · scan with **truffleHog, git-secrets, gitleaks**.

## 🛠️ Hands-on — safe lab (uses FAKE keys)

### Lab 1 — Find the leak
1. Create a throw-away file `leak_demo.py` in the project root:
   ```python
   aws_access_key_id = "AKIAABCDEFGHIJKLMNOP"      # fake pattern for the lab
   ```
2. Run the teaching scanner:
   ```bash
   python scripts/simple_secret_scan.py .
   ```
   It reports `leak_demo.py:1: AWS Access Key ID` and exits with code **1**.
3. Delete `leak_demo.py` and run again → *No secrets found.*
4. Read `scripts/simple_secret_scan.py`: see how a **regular expression** (`AKIA[0-9A-Z]{16}`) finds keys.

### Lab 2 — Block leaks automatically
1. Make sure `.gitignore` contains `.env` (it does).
2. Install the pre-commit hook (uses `.pre-commit-config.yaml`, gitleaks):
   ```bash
   pip install pre-commit
   git init            # if not already a repo
   pre-commit install
   ```
3. Try committing a file containing a fake key → the commit is **blocked**.
4. The CI workflow `.github/workflows/ci.yml` also runs the scanner on every push.

### Lab 3 — Fire drill: respond to a "leaked" key (use a practice IAM user)
1. Create a key for a practice user (Lesson 8) and pretend it leaked.
2. Follow the table above: create a new key → **Deactivate** old → **Delete** old.
3. `python scripts/cloudtrail_lookup.py <old-access-key-id>` — see what that key did (CloudTrail events can take minutes to appear).
4. Write a short incident report: *what leaked, when, what you did, how you'll prevent it.*

### Lab 4 — Refactor Meera's script
Take the ❌ example above and rewrite it with **no keys in code** (answer: `scripts/list_buckets.py` and Lesson 10).

## 📁 Files for this lesson
`scripts/simple_secret_scan.py` · `.pre-commit-config.yaml` · `.gitignore` · `scripts/cloudtrail_lookup.py` · `.github/workflows/ci.yml`

## ⚠️ Common mistakes
- Deleting the key from the file but leaving it in **Git history**.
- Thinking a *private* repo is safe (repos get made public, forked, or accessed by many).
- Putting keys in a Docker image or `Dockerfile` (`ENV AWS_SECRET_ACCESS_KEY=...` is baked in!).
- Pasting full error logs or screenshots that contain keys.
- Forgetting to check **all Regions** after an incident.

## ✅ Best practices (panel 9)
Never expose the Secret Key · use environment variables or Parameter Store/Secrets Manager · use IAM roles (no keys for EC2) · give only required permissions · rotate regularly · monitor with CloudTrail · scan repositories regularly.

## 📝 Quiz
1. Name three places keys leak.
2. Is deleting the line from the file enough? Why not?
3. What are the 5 response steps?
4. Which AWS feature gives an EC2 server access with no stored keys?
5. Which tools scan for secrets?

<details><summary>Show answers</summary>

1. e.g. GitHub, logs, screenshots, chat, config files.  2. No — old commits still contain the key and it may already be copied.  3. Rotate, remove from code, check Git history, revoke, monitor.  4. An IAM role (instance profile).  5. truffleHog, git-secrets, gitleaks.
</details>

## 🏠 Assignment
Audit one of your old projects with the scanner or gitleaks. Write a one-page "Secret handling policy" for a team of 5 developers.

## 🔑 Key takeaway
Never hard-code AWS Secret Keys. Exposed keys cause data loss, high bills and account takeover.
Use `.env`, IAM roles or Secrets Manager; rotate keys and watch CloudTrail.

**हिंदी में सार:** Secret Key कभी code, GitHub या screenshot में न डालें। लीक हो जाए तो तुरंत key rotate/delete करें,
code और Git history साफ़ करें, और CloudTrail से गतिविधि जाँचें।

⬅️ [Lesson 8](08-access-keys.md) · ➡️ **Next:** [Lesson 10 — Python + .env](10-python-dotenv.md)
