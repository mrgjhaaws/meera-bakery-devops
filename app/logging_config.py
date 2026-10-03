"""Application logging - Lesson 15.

Logs go to stdout in a simple format. On EC2/ECS/Docker, CloudWatch collects stdout:
  * Docker:  --log-driver=awslogs --log-opt awslogs-group=/aws/app/meera-bakery
  * EC2:     install the CloudWatch Agent and point it at the log file
"""
import logging
import sys


def setup_logging(level: int = logging.INFO) -> logging.Logger:
    root = logging.getLogger()
    if not root.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(
            logging.Formatter("%(asctime)s %(levelname)-5s %(message)s", "%Y-%m-%d %H:%M:%S")
        )
        root.addHandler(handler)
    root.setLevel(level)
    return logging.getLogger("meera-bakery")
