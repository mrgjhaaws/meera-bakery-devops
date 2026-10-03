"""Lesson 9 - a tiny teaching scanner that finds AWS keys in your files.
(Real projects should use gitleaks / truffleHog / git-secrets - see docs.)
Run:  python scripts/simple_secret_scan.py [folder]
Exit code 1 if something suspicious is found, so you can use it in CI.
"""
import re
import sys
from pathlib import Path

PATTERNS = {
    "AWS Access Key ID": re.compile(r"\b(AKIA|ASIA)[0-9A-Z]{16}\b"),
    "AWS Secret Key assignment": re.compile(
        r"aws_secret_access_key\s*[=:]\s*['\"]?[A-Za-z0-9/+=]{40}", re.I),
    "Private key block": re.compile(r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----"),
}
SKIP_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__", ".terraform", "images"}
# AWS's own documentation uses this key in examples - it is not real.
KNOWN_EXAMPLES = {"AKIAIOSFODNN7EXAMPLE"}

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
hits = 0
for f in root.rglob("*"):
    if not f.is_file() or SKIP_DIRS & set(f.parts) or f.suffix in {".png", ".zip", ".pyc"}:
        continue
    try:
        lines = f.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        continue
    for n, line in enumerate(lines, 1):
        for label, rx in PATTERNS.items():
            m = rx.search(line)
            if m and not any(ex in line for ex in KNOWN_EXAMPLES):
                print(f"[!] {f}:{n}: {label}")
                hits += 1

print("No secrets found." if hits == 0 else f"\n{hits} possible secret(s) found - rotate them!")
sys.exit(1 if hits else 0)
