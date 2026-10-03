# IAM policy examples (Lesson 7, 8, 11, 12)

Replace the placeholders (`BUCKET_NAME`, `ACCOUNT_ID`, `STATIC_BUCKET_NAME`) before using.

| File | Used for |
|------|----------|
| `s3-bakery-images-policy.json` | Minimum rights for the bakery app: list the bucket, read/write `products/*` |
| `ssm-read-policy.json` | Read-only access to `/meera-bakery/*` parameters (Lesson 11, panel 7) |
| `ec2-trust-policy.json` | Lets EC2 assume an IAM role -> **no access keys on the server** |
| `github-actions-deploy-policy.json` | Least-privilege permissions for the CI/CD IAM user (Lesson 12/14) |

Create a policy from a file:

```bash
aws iam create-policy --policy-name MeeraBakeryS3Images \
  --policy-document file://iam/s3-bakery-images-policy.json
```
