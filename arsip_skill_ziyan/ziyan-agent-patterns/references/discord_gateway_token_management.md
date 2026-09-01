# Discord Gateway Token Management (Verified 2026-08-12)

## Problem
- Token valid via REST API (`curl -H "Authorization: Bot <token>" https://discord.com/api/v10/users/@me` → 200 OK)
- BUT Hermes gateway process fails with `Improper token has been passed` / `401 Unauthorized`
- Gateway process caches token at startup and doesn't reload `.env` changes

## Root Cause
1. Gateway process reads `DISCORD_BOT_TOKEN` from `os.environ` at startup (via `_getenv()` in `gateway/config.py`)
2. Token update in `.env` file doesn't propagate to running gateway process
3. Scheduled task VBS wrapper doesn't pass updated env vars

## Fix Pattern (Verified Working)
```bash
# 1. Kill ALL gateway processes
powershell.exe -NoProfile -Command "Get-Process | Where-Object {$_.ProcessName -like '*python*' -and $_.CommandLine -like '*gateway*'} | Stop-Process -Force"

# 2. Export token in current shell BEFORE starting gateway
export DISCORD_BOT_TOKEN="MTUzNjk0MTQyOTc5NTA3MDA5Mg.GcW3ai.rFlpS4GFQ2HN8djZMEIrO3V4QYU4Njxv8MUj9I"
export HERMES_HOME="C:/Users/arija/AppData/Local/hermes"

# 3. Start gateway with token in process environment
python -m hermes_cli.main gateway run
```

## Permanent Solution: Process Supervision
Gateway needs proper process supervision (NSSM/PM2) with:
- Environment variables baked into service definition
- Auto-restart on crash
- Health check endpoint monitoring

## Scheduled Task Fix (Applied)
- Created `Hermes_Gateway_Auto` task (trigger every 30 min daily)
- Created cron `Hermes_Gateway_Health` (every 5 min) → calls `hermes gateway status` + restart if down
- VBS wrapper in Startup folder as fallback

## Token Validation Checklist
Before assuming token works:
- [ ] REST API test: `curl -H "Authorization: Bot <token>" https://discord.com/api/v10/users/@me` → 200
- [ ] Bot User ID matches server member (check Developer Portal → Bot → Copy ID)
- [ ] Bot is IN the target server (check server member list)
- [ ] All 3 Privileged Gateway Intents enabled (Presence, Server Members, Message Content)
- [ ] Gateway process restarted AFTER token update

## Common Pitfall
**Token valid via API ≠ Gateway connected.** Gateway process must be restarted with new token in its environment. `.env` file update alone is insufficient.