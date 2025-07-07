import subprocess
import sys

try:
    result = subprocess.run(
        [sys.executable, "main.py"],
        stdin=sys.stdin,
        stdout=sys.stdout,
        stderr=sys.stderr,
        timeout=5
    )
except Exception as e:
    print(e)