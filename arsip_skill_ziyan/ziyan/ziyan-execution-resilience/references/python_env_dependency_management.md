# Python Environment & Dependency Management (Verified 2026-08-12)

## Problem
Hermes gateway process crashed on startup with `ModuleNotFoundError` for:
- `dotenv` (python-dotenv)
- `yaml` (PyYAML)
- `aiohttp`, `httpx`, `pydantic`, `rich`, `tenacity`, `urllib3`, `websockets`, `cryptography`, `pyjwt`, `packaging`, `pathspec`, `prompt_toolkit`

## Root Cause
- Hermes agent venv (`AppData/Local/hermes/hermes-agent/venv/`) missing pip and core dependencies
- System Python 3.13 (MS Store) used as fallback but also missing packages
- Gateway process runs in isolated environment without access to user site-packages

## Fix Pattern (Verified Working)
```bash
# Install all required dependencies system-wide (user site-packages)
python3 -m pip install python-dotenv pyyaml aiohttp httpx rich pydantic tenacity urllib3 websockets cryptography pyjwt packaging pathspec prompt_toolkit

# Then run gateway with system Python
export HERMES_HOME="C:/Users/arija/AppData/Local/hermes"
export DISCORD_BOT_TOKEN="<token>"
export PYTHONPATH="C:/Users/arija/AppData/Local/hermes/hermes-agent"
python3 -m hermes_cli.main gateway run
```

## Dependency Categories

### Core Gateway Dependencies (MUST HAVE)
| Package | Purpose | Verified Version |
|---------|---------|------------------|
| python-dotenv | Load .env files | 1.2.2 |
| PyYAML | Config parsing | 6.0.3 |
| aiohttp | Async HTTP client | 3.14.3 |
| httpx | HTTP client (sync/async) | 0.28.1 |
| pydantic | Data validation | 2.13.4 |
| rich | Terminal formatting | 15.0.0 |
| tenacity | Retry logic | 9.1.4 |
| urllib3 | HTTP library | 2.7.0 |
| websockets | WebSocket client | 17.0.1 |
| cryptography | Crypto primitives | 50.0.0 |
| pyjwt | JWT handling | 2.13.0 |
| packaging | Version parsing | 26.3 |
| pathspec | Gitignore patterns | 1.1.1 |
| prompt_toolkit | CLI interaction | 3.0.53 |

### Platform-Specific Dependencies
| Package | Platform | Purpose |
|---------|----------|---------|
| discord.py | Discord | Gateway adapter |
| python-telegram-bot | Telegram | Gateway adapter |
| gspread | Google Sheets | Sheets integration |
| google-auth | Google APIs | Auth |

## Windows-Specific Issues

### MS Store Python 3.13 + venv Problems
- Fresh venv breaks on `cryptography`/`cffi` (`_cffi_backend` missing)
- MS Store Python doesn't include system binaries for native builds
- **Fix**: Pin binary wheels before installing other deps:
  ```bash
  .venv/Scripts/pip.exe install "cryptography==42.0.5" "cffi==1.17.1" --force-reinstall --no-deps
  ```

### Event Loop Conflict (python-telegram-bot v21+)
- `AsyncIOScheduler` + `Application.run_polling()` conflict
- **Fix**: Use `BackgroundScheduler` (thread-based) + synchronous `application.run_polling()`

## Process Environment Propagation
**Critical**: Gateway process MUST have env vars in its process environment at startup:
```bash
export HERMES_HOME="C:/Users/arija/AppData/Local/hermes"
export DISCORD_BOT_TOKEN="<token>"
export PYTHONPATH="C:/Users/arija/AppData/Local/hermes/hermes-agent"
export VIRTUAL_ENV="C:/Users/arija/AppData/Local/hermes/hermes-agent/venv"
export PYTHONIOENCODING="utf-8"
export HERMES_GATEWAY_DETACHED="1"
python3 -m hermes_cli.main gateway run
```

`.env` file alone is NOT sufficient — `os.environ` takes precedence in `_getenv()`.

## Verification Checklist
- [ ] `python3 -c "import dotenv, yaml, aiohttp, httpx, pydantic, rich, tenacity, urllib3, websockets, cryptography, jwt, packaging, pathspec, prompt_toolkit"`
- [ ] `curl -s http://127.0.0.1:20128/v1/models` → JSON (9router)
- [ ] Gateway log shows `✓ discord connected` + `✓ telegram connected`
- [ ] Test send: `hermes send -t discord:<channel_id> "test"` → success

## Prevention
- Document required dependencies in skill
- Use process supervision with baked env vars
- Health check cron validates gateway connectivity
- Don't rely on `.env` file alone for process env vars