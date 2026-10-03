# Troubleshooting

## Python / VS Code
| Problem | Fix |
|---------|-----|
| `python` not recognized | Reinstall Python with *Add to PATH*, reopen terminal. Try `py` on Windows. |
| PowerShell blocks `Activate.ps1` | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| VS Code uses wrong Python | `Ctrl+Shift+P` → *Python: Select Interpreter* → `.venv` |
| `ModuleNotFoundError: boto3/fastapi` | venv not active, or `pip install -r requirements-dev.txt` not run |
| `ModuleNotFoundError: app` | Run commands from the **project root** (folder containing `app/`) |
| Tests fail with credential errors | Run with `python -m pytest` from the project root (conftest sets fake keys) |

## AWS CLI / credentials
| Error | Meaning / fix |
|-------|---------------|
| `Unable to locate credentials` / `NoCredentialsError` | `aws configure`, or set variables in `.env` |
| `InvalidClientTokenId` | Key typo, deleted or deactivated key |
| `SignatureDoesNotMatch` | Wrong secret key or clock skew — re-copy, check system time |
| `AccessDenied` / `UnauthorizedOperation` | IAM policy missing — read the message, it names the missing action |
| `ExpiredToken` | Temporary credentials expired — refresh/login again |
| Works in console, not CLI | Different user/Region — `aws sts get-caller-identity`, `aws configure list` |
| `Could not connect to the endpoint URL` | Wrong Region name or no internet |

## S3 / SSM / CloudWatch
| Error | Fix |
|-------|-----|
| `BucketAlreadyExists` | Names are global — add your name + numbers |
| `IllegalLocationConstraintException` | In regions other than `us-east-1` pass `CreateBucketConfiguration={'LocationConstraint': region}` |
| `NoSuchBucket` | Typo or wrong Region |
| `ParameterNotFound` | Name is case-sensitive, must start with `/`, check Region |
| No alarm e-mails | Confirm the SNS subscription e-mail |

## Git / GitHub
| Problem | Fix |
|---------|-----|
| `.env` shows in `git status` | `git rm --cached .env`, ensure `.gitignore`; **rotate keys if pushed** |
| `remote: Permission denied` | Use a Personal Access Token / GitHub login in the credential manager |
| Workflow not visible | File must be in `.github/workflows/` with `.yml` extension and valid YAML |
| Deploy job "skipped" | Repo variable `DEPLOY_ENABLED` must equal `true` |

## Terraform
| Error | Fix |
|-------|-----|
| `Error acquiring the state lock` | Another run active; if stuck `terraform force-unlock <ID>` (carefully) |
| `Provider produced inconsistent result` | Re-run `terraform apply` (eventual consistency) |
| `InvalidKeyPair.NotFound` | `key_name` must exist in the same Region |
| `terraform destroy` fails on S3 | Buckets have `force_destroy = true`; if you created extras manually, empty them first |
| Plan shows replace of EC2 each time | AMI lookup changed (new AMI released) — expected; pin an AMI for production |

## Docker
| Problem | Fix |
|---------|-----|
| `Cannot connect to the Docker daemon` | Start Docker Desktop |
| Port already allocated | Another program uses 8000/80 — change `-p 8001:8000` |
| Container exits immediately | `docker logs <name>`; usually wrong module path or missing env vars |
| `no basic auth credentials` | `docker login` to ECR again |
