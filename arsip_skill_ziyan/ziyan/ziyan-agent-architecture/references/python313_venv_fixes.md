# Python 3.13 (MS Store) Venv Dependency Fixes for ZIYAN

## Problem
Windows MS Store Python 3.13 lacks build tools (no Rust toolchain, no MSVC) → `cryptography`, `cffi`, `google-auth` build from source fail.

## Solution: Pin Wheels Only

```bash
# In venv
pip install cryptography==42.0.5 cffi==1.17.1 google-auth==2.35.0 --only-binary :all:
```

### Required Pins
| Package | Version | Reason |
|---------|---------|--------|
| `cryptography` | 42.0.5 | Last wheel with manylinux2014, no Rust needed |
| `cffi` | 1.17.1 | Compatible with cryptography 42.0.5 |
| `google-auth` | 2.35.0 | Avoids transitive cryptography upgrade |

### Full Requirements.txt for ziyan_affiliate_agent
```text
python-telegram-bot==21.7
gspread==6.2.0
google-auth==2.35.0
google-auth-oauthlib==1.2.0
google-api-python-client==2.158.0
httpx==0.28.1
apscheduler==3.11.0
pyyaml==6.0.2
cryptography==42.0.5
cffi==1.17.1
```

### Install Order (matters on 3.13)
```bash
# 1. Core wheels first
pip install cryptography==42.0.5 cffi==1.17.1 --only-binary :all:
# 2. Google auth stack
pip install google-auth==2.35.0 google-auth-oauthlib==1.2.0 --only-binary :all:
# 3. Rest
pip install -r requirements.txt --only-binary :all:
```

## Verification
```bash
.venv/Scripts/python.exe -c "
import cryptography, cffi, google.auth
print('cryptography:', cryptography.__version__)
print('cffi:', cffi.__version__)
print('google-auth:', google.auth.__version__)
"
# Expected: 42.0.5, 1.17.1, 2.35.0
```