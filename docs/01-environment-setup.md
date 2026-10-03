# 01 · Environment Setup (do this once)

Windows is shown first (the slides use Windows paths like `C:\MeeraBakery>`); macOS/Linux
equivalents are given where they differ.

## 1. Tools checklist

| Tool | Why | Check it works |
|------|-----|----------------|
| VS Code | Editor for the whole project | `code --version` |
| Python 3.11+ | App + scripts | `python --version` |
| Git | Version control, GitHub Actions | `git --version` |
| AWS account | Everything from Lesson 2 | Can sign in to the console |
| AWS CLI v2 | Talk to AWS from the terminal | `aws --version` |
| Terraform 1.5+ | Lesson 13 | `terraform -version` |
| Docker Desktop | Lesson 14 | `docker --version` |

## 2. Install (Windows PowerShell)

```powershell
winget install Microsoft.VisualStudioCode
winget install Python.Python.3.11
winget install Git.Git
winget install Amazon.AWSCLI
winget install HashiCorp.Terraform
winget install Docker.DockerDesktop
```
Close and reopen the terminal afterwards so the new programs are on your `PATH`.

**macOS (Homebrew):** `brew install --cask visual-studio-code docker` and
`brew install python@3.11 git awscli terraform`.

## 3. Open the project in VS Code
1. **File ▸ Open Folder…** → choose `aws-devops-meeras-bakery`.
2. Click **Install** when VS Code offers the recommended extensions
   (Python, AWS Toolkit, Terraform, Docker, GitHub Actions, YAML).
3. Open a terminal: **Terminal ▸ New Terminal**.

## 4. Python virtual environment

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1          # if blocked: Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
pip install -r requirements-dev.txt
python -m pytest -v                 # should show: 6 passed
```
macOS/Linux: `source .venv/bin/activate`.
In VS Code press **Ctrl+Shift+P → "Python: Select Interpreter" →** choose `.venv`.

## 5. Create your AWS account (see also Lesson 2)
1. Go to **https://aws.amazon.com** → *Create an AWS Account*.
2. Enter e-mail, a strong password, and payment details (a card is required; the Free Tier covers small usage).
3. Choose the **Basic (free) support plan**.
4. Sign in as **root user**, then immediately:
   - Turn on **MFA** (Account name ▸ Security credentials ▸ Assign MFA device).
   - Create a **budget alert**: *Billing and Cost Management ▸ Budgets ▸ Create budget ▸ Zero spend / monthly cost budget* with your e-mail.
5. Create an everyday **IAM user** (Lesson 7) and stop using root.

## 6. Connect the AWS CLI (after Lesson 7/8)

```bash
aws configure
# AWS Access Key ID [None]:      <from Lesson 8>
# AWS Secret Access Key [None]:  <from Lesson 8>
# Default region name [None]:    ap-south-1
# Default output format [None]:  json

aws sts get-caller-identity       # who am I?  (proves it works)
```

## 7. Create your own `.env`

```powershell
Copy-Item .env.example .env       # macOS/Linux: cp .env.example .env
```
Edit `.env` in VS Code. It is listed in `.gitignore`, so Git will not upload it.

## 8. Verify everything

```bash
python --version && git --version && aws --version && terraform -version && docker --version
python -m pytest -q
python scripts/lesson01_capacity_simulation.py
```
If a command is "not recognized", reopen the terminal; if still failing see
[troubleshooting.md](troubleshooting.md).
