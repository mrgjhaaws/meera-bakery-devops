# Lesson 16 · Next Topic — Auto Scaling and High Availability
**Keep Your Bakery Always Online** *(infographic not yet in this project)*

`Part 2 · Preview` · The last slide of Lesson 15 announces this lesson.

## Why Meera needs it
One EC2 server (Lesson 14) is still a **single point of failure** and cannot handle a festival spike (Lesson 1 simulation!). Lesson 16 fixes both.

## Topics to expect
| Topic | Idea |
|-------|------|
| **Multi-AZ design** | Run servers in 2+ Availability Zones (Lesson 5) |
| **Application Load Balancer (ALB)** | One URL, traffic spread over many servers, health checks |
| **Launch template** | Blueprint of the server (AMI, type, role, user-data) |
| **Auto Scaling Group (ASG)** | Keeps N healthy servers; adds/removes with demand |
| **Scaling policies** | e.g. "keep average CPU near 50 %" (uses CloudWatch metrics — Lesson 15) |
| **Health checks & self-healing** | Unhealthy instance replaced automatically |
| **RDS Multi-AZ** | Database failover |

## Prepare now
- Re-read Lessons 1, 5 and 15.
- Practice: extend `terraform/` with a launch template (reuse the AMI lookup, security group, IAM profile and `user_data`).
- Try the idea in Python: change `REQUESTS` in `scripts/lesson01_capacity_simulation.py` and compute how many servers you would need each hour.

When the infographic for Lesson 16 is available, add it as `images/lesson-16-auto-scaling.png`
and create the lesson document with the same template as the others.

⬅️ [Lesson 15](15-cloudwatch.md)
