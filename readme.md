# payload-builder

Modular payload generation framework for authorised penetration testing engagements. Builds reverse shells, keyloggers, RAT loaders and droppers with configurable obfuscation.

Built for personal use across client engagements. Not intended for distribution.

## Features

- Template-based payload generation (reverse shell, keylogger, RAT loader)
- Configurable C2 callback and exfil options
- Built-in obfuscation (custom packer + string encoding)
- Dropper with staged download
- Phishing template for social engineering assessments
- Auto-build via GitHub Actions

## Setup

```bash
pip install pyyaml requests pycryptodome
```

## Usage

```bash
# build a reverse shell payload
python3 builder.py --template reverse_shell --c2 <callback_ip> --port 8443

# build with obfuscation
python3 builder.py --template rat_loader --obfuscate --pack

# use config defaults
python3 builder.py --template keylogger_stub --use-config
```

## Structure

```
├── builder.py           # main build script
├── config.yaml          # default build config
├── templates/           # payload templates
├── obfuscation/         # packer & encoder modules
├── delivery/            # dropper and phish templates
└── CHANGELOG.md         # version history
```

## Notes

This is a personal toolkit. If you've found a bug or want to suggest a feature, reach out:

- Jabber: `d3vilboy@jabber.calyxinstitute.org`
- PGP: `0xAE7F 2C91 D438 6B10`

Do not use this framework without explicit written authorisation from the target organisation. I take no responsibility for misuse.
