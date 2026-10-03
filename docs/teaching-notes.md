# Teaching Notes (for trainers)

The infographics are designed for clarity, so some details are simplified. Use these notes to
add accuracy in class. None of them changes the lesson flow.

| Lesson | Slide says | Add this nuance |
|-------|-----------|-----------------|
| 2 | "Pay only for what you use" | True for most services, but some resources (idle databases, unattached IPs/volumes, NAT gateways) cost even when idle. Teach budgets early. |
| 3 | Lambda listed under PaaS | Often called *serverless / FaaS*; many courses treat it as a separate level above PaaS. |
| 5 | "Each Region has multiple AZs" | Yes (typically 3+). Some newer Regions are *opt-in*. Not every service exists in every Region; prices differ. |
| 6/7 | Console navigation | AWS updates the console UI often; menu positions can differ from screenshots. Teach *concepts + search box*. |
| 7 | Accountant "Billing only" | Billing pages for IAM users must be enabled by the account owner (*IAM access to Billing*). |
| 7 | IAM users for team | Modern AWS guidance prefers **IAM Identity Center (SSO)** for humans and IAM *roles* for workloads; IAM users + keys are fine for learning. |
| 8 | Access keys for apps & CI/CD | Correct, but prefer **roles** (EC2/ECS/Lambda) and **OIDC** (GitHub Actions) so no long-lived keys exist. |
| 9 | Key leak response | In real incidents **revoke first**, clean history later. AWS may quarantine leaked keys it finds in public repos. |
| 10 | `.env` for credentials | Good for local development. On servers use IAM roles / Parameter Store / Secrets Manager; `.env` is not deployed. |
| 11 | Access keys stored in Parameter Store | Teaches the mechanism; in production the app uses a role, so you store *settings and app secrets*, not AWS keys (bootstrap problem). Secrets Manager adds rotation. |
| 12 | Workflow uses static AWS secrets | Works; discuss OIDC as the next step. Action versions (`@v4`) evolve — check current majors. |
| 13 | Hard-coded AMI IDs, `t2.micro` | AMI IDs are per-Region and expire — use an SSM public parameter or data source (our code does). Free-Tier-eligible instance types vary by account/Region. The two slide versions differ only in example detail and Terraform version (1.6.0 vs 1.5.7). |
| 13 | State file | Introduce remote state (S3 backend + locking) before teaching teams. |
| 14 | `main:app` in Dockerfile | Our layout uses `app.main:app`. Also: EC2 must authenticate to ECR (done via instance role). SSH deploys need port 22 reachable from the runner — **SSM Run Command** or ECS/CodeDeploy are safer. |
| 15 | EC2 metrics | Memory and disk-space metrics need the CloudWatch Agent. Alarm e-mails need SNS subscription confirmation. |
| All | Sample keys | `AKIAIOSFODNN7EXAMPLE` / `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY` are AWS's published documentation examples (not real). Tell students never to paste real keys into slides. |

## Suggested class flow (per lesson, 90 min)
1. 10 min — Meera's question (read the story aloud).
2. 25 min — Walk the infographic panel by panel.
3. 35 min — Live hands-on (students follow the numbered steps).
4. 10 min — Quiz (cold-call, then reveal answers).
5. 10 min — Cleanup + assignment briefing.

## Safety checklist before every lab
- [ ] Students use **IAM users**, not root · [ ] Budget alerts exist · [ ] Same Region for everyone
- [ ] `.env` is ignored by Git · [ ] Cleanup commands are shown **before** the lab starts
