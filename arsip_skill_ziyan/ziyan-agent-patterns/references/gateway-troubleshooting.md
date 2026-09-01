# Hermes Gateway Troubleshooting - Discord + Telegram 24/7 on Windows

Sumber: Session 2026-08-12 - Gateway process tidak persistent, token caching issue, missing Python deps.

---

## Root Cause Analysis

### 1. Gateway Process Mati Segera (No Persistent Process)
**Gejala:** `hermes gateway start` → exit code 0 tapi tidak ada PID di `ps aux`
**Penyebab:** Missing Python dependencies (`python-dotenv`, `pyyaml`, `aiohttp`, `httpx`, `pydantic`, `rich`, `tenacity`, `urllib3`, `websockets`, `cryptography`, `pyjwt`, `packaging`, `pathspec`, `prompt_toolkit`)
**Fix:** Install system-wide via `python3 -m pip install <packages>`

### 2. Token Caching di adapter.py
**File:** `AppData/Local/hermes/hermes-agent/plugins/platforms/discord/adapter.py`
**Issue:** `_config_value("DISCORD_BOT_TOKEN")` → `get_env_value()` → `load_env()` dengan `_env_cache` global
**Problem:** Cache tidak invalidated saat `.env` berubah → gateway baca token lama/kosong
**Workaround:** Set env var EXPLICIT di shell sebelum start: `export DISCORD_BOT_TOKEN="..."`

### 3. Scheduled Task VBS Wrapper
**File:** `AppData/Local/hermes/gateway-service/Hermes_Gateway.vbs` → calls `Hermes_Gateway.cmd`
**Issue:** CMD window keluar segera, tidak hold process
**Fix:** Power settings High Performance + no sleep + cron health check 5 menit

---

## Working Configuration (Validated 2026-08-12)

### Environment Variables (WAJIB di shell sebelum start)
```bash
export HERMES_HOME="C:/Users/arija/AppData/Local/hermes"
export DISCORD_BOT_TOKEN="MTUzNjk0MTQyOTc5NTA3MDA5Mg.GcW3ai.rFlpS4GFQ2HN8djZMEIrO3V4QYU4Njxv8MUj9I"
export PYTHONPATH="C:/Users/arija/AppData/Local/hermes/hermes-agent"
export PYTHONIOENCODING="utf-8"
export HERMES_GATEWAY_DETACHED="1"
```

### Start Command
```bash
python3 -m hermes_cli.main gateway run
```

### Verified Logs (Success Indicators)
```
2026-08-12 20:46:41,426 INFO [Telegram] Connected to Telegram (polling mode)
2026-08-12 20:46:44,321 INFO gateway.run: ✓ telegram connected
2026-08-12 20:46:51,774 INFO [Discord] Connected as Ceo#5499
2026-08-12 20:46:51,831 INFO gateway.run: ✓ discord connected
2026-08-12 20:46:51,956 INFO gateway.run: Gateway running with 2 platform(s)
```

---

## Auto-Restart Mechanism (Deployed)

### 1. Scheduled Task: `Hermes_Gateway_Auto`
- Trigger: Daily, repeat every 30 minutes
- Action: VBS wrapper → CMD → python gateway run
- Purpose: Restart jika gateway mati

### 2. Cron Job: `Hermes_Gateway_Health` (job_id: via cronjob tool)
- Schedule: Every 5 minutes
- Action: Health check → restart jika down
- `attach_to_session=true` untuk persistence

### 3. Power Settings (Windows 11, 8GB RAM)
```powershell
powercfg /change monitor-timeout-ac 10
powercfg /change monitor-timeout-dc 10
powercfg /change standby-timeout-ac 0
powercfg /change standby-timeout-dc 0
powercfg /change hibernate-timeout-ac 0
powercfg /change hibernate-timeout-dc 0
# PCIe ASPM off, USB selective suspend off, High Performance scheme
```

---

## Discord Bot Setup (Clean Slate)

### Masalah: 15x reset token tapi salah aplikasi
- **Application ID lama:** `1532650020841586690` (Hermes_bot#6835)
- **Bot User ID di server:** `1349811063872553031` (MISMATCH)

### Fix: Clean Slate
1. Hapus aplikasi lama di Discord Developer Portal
2. Buat aplikasi baru → Bot → Reset Token
3. Invite dengan **Application ID** (bukan Bot User ID): `https://discord.com/oauth2/authorize?client_id=<APP_ID>&permissions=8&scope=bot+applications.commands`
4. Token baru VALID via REST API: `curl -H "Authorization: Bot <TOKEN>" https://discord.com/api/v10/users/@me`

### Current Working Bot
- **Name:** Ceo#5499
- **Application ID:** `1536941429795070092`
- **Guild:** Arjal Meutuwah's server (`1524820179047940216`)
- **Channel:** #hq (`1532759261610774768`)

---

## Common Pitfalls & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `ModuleNotFoundError: dotenv` | Missing deps | `pip install python-dotenv pyyaml aiohttp ...` |
| `DISCORD_BOT_TOKEN not set` | Env var not in process | Export explicitly before start |
| `WebSocket 4001: Invalid token` | Token lama/corrupt | Clean slate: new app, new token |
| `Gateway connected but no response` | Agent failure in session | Check `gateway.run: Transient agent failure` in log |
| `Scheduled task runs but no process` | VBS exits immediately | Use cron job health check + explicit env vars |

---

## Verification Checklist (Post-Restart)

- [ ] `ps aux | grep hermes` → shows gateway process
- [ ] `tail -f logs/gateway.log` → shows "Gateway running with 2 platform(s)"
- [ ] `hermes send -t discord:<CHANNEL_ID> "test"` → "sent"
- [ ] `hermes send -t telegram:<CHAT_ID> "test"` → "sent"
- [ ] Discord: Bot shows "Online" in member list
- [ ] Telegram: Bot responds to /start