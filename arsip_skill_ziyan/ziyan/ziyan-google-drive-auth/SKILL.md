---
name: ziyan-google-drive-auth
description: ZIYAN Drive/Sheets auth — SA can't upload, use OAuth token.
version: 1.0.0
author: ZIYAN Orchestrator
---

# ZIYAN Google Drive / Sheets Auth

## When to use
- Building any ZIYAN tool that reads/writes Google Drive/Sheets.
- Debugging `403 storageQuotaExceeded`.
- Google auth setup on this Windows machine (Hermes + project venv coexisting).

## CRITICAL: SA CANNOT upload to Drive
Free GCP SA (`*.iam.gserviceaccount.com`) has Drive quota = 0.
- READ: works if Bos shares folder/sheet to SA as Editor (`canEdit=True`).
- WRITE/UPLOAD: FAILS `403 storageQuotaExceeded` even into a shared folder. Google bills quota to the SA.
- FIX (writes): use OAuth user `token.json`, NOT SA. `google_workspace.py` auto-uses `token.json` if present. For any write path, ship `client_secret.json` + run OAuth flow.

> NOTE: older `ziyan-google-archive` says "Prefer SA + shared folder" — true ONLY for READ. SA cannot WRITE. Use OAuth for uploads.

## OAuth Desktop client setup
1. Console → Credentials → Create OAuth client ID → Desktop app → download `client_secret.json`.
2. Console → OAuth consent screen → Test users → ADD Bos Google account. Skip → `invalid_grant` at exchange.
3. `env -u PYTHONPATH GOOGLE_CREDENTIALS_FILE=client_secret.json ./venv/Scripts/python.exe scripts/google_auth.py` (background, laptop listener).
4. Browser on SAME laptop (redirect `http://localhost:PORT`). Phone-open → redirect not caught → manual exchange.

## Manual OAuth code exchange
Pipe full redirect URL to a script calling `flow.fetch_token(code=...)`. Code single-use, expires ~30s. See `references/oauth_manual.md`.

## PYTHONPATH pollution
Global PYTHONPATH → Hermes venv. Always `env -u PYTHONPATH ./venv/Scripts/python.exe ...`. Pip too: `./venv/Scripts/python.exe -m pip install` with `env -u PYTHONPATH`.

## SAFE PROCESS KILLS (lesson 2026-08-15)
Never `taskkill` an unverified PID. Guessing "PID 4180 = manual bot" killed 9router/gateway → vision+AI down.
- Identify first: `powershell -NoProfile -Command "Get-CimInstance Win32_Process -Filter \"CommandLine LIKE '%keyword%'\" | Select ProcessId,CommandLine"`
- Count REAL bot: filter `Name='python.exe' AND CommandLine LIKE '%ziyan_bot.bot%'` (LIKE also matches your own shell cmd string).
- Prefer killing via `process` tool using `session_id` of background tasks you started.

## Verify before "done"
Process start (`Application started`) ≠ feature works. For archive bot, proof = file in Drive + row in Sheets. Exercise end-to-end before reporting.

## Pitfalls
- SA+shared = READ ok, UPLOAD fails. Use OAuth for writes.
- `invalid_grant` = missing Test User or expired code.
- Telegram `TELEGRAM_ALLOWED_USER_IDS` = sender user ID, NOT bot token prefix (`8684...` is bot). Log `user_id` on reject.
- Multiple bot instances → Telegram `Conflict`. Keep exactly ONE `python.exe -m ziyan_bot.bot`.
