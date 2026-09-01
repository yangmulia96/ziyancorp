---
name: windows-ai-agent-infrastructure
description: Run 24/7 AI agents on Windows with power management.
category: devops
tags: [windows, power-management, hermes, 9router, telegram-bot, 24x7, ai-agents]
---

# Windows AI Agent Infrastructure

**Trigger**: Setting up or troubleshooting AI agents (Hermes, 9Router, n8n, Telegram bots) that must run 24/7 on Windows laptops.

## Power Management (Critical for 24/7)

### Disable Sleep/Hibernate
```powershell
powercfg /setactive f8bf9830-1d5e-4187-a347-96873927865b
powercfg /setacvalueindex scheme_current SUB_SLEEP STANDBYIDLE 0
powercfg /setdcvalueindex scheme_current SUB_SLEEP STANDBYIDLE 0
powercfg /setacvalueindex scheme_current SUB_SLEEP HIBERNATEIDLE 0
powercfg /setdcvalueindex scheme_current SUB_SLEEP HIBERNATEIDLE 0
powercfg /setacvalueindex scheme_current SUB_SLEEP HYBRIDSLEEP 0
powercfg /setdcvalueindex scheme_current SUB_SLEEP HYBRIDSLEEP 0
```

### Network/PCIe/USB Power
```powershell
powercfg /setacvalueindex scheme_current 19cbb8fa-5279-450e-9fac-8a3d5fedd0c1 12bbebe6-58d6-4636-95bb-3217ef867c1a 0
powercfg /setdcvalueindex scheme_current 19cbb8fa-5279-450e-9fac-8a3d5fedd0c1 12bbebe6-58d6-4636-95bb-3217ef867c1a 0
powercfg /setacvalueindex scheme_current SUB_PCIEXPRESS ASPM 0
powercfg /setdcvalueindex scheme_current SUB_PCIEXPRESS ASPM 0
powercfg /setacvalueindex scheme_current 2a737441-1930-4402-8d77-b2bebba308a3 48e6b7a6-50f5-4782-a5d4-53bb8f07e226 0
powercfg /setdcvalueindex scheme_current 2a737441-1930-4402-8d77-b2bebba308a3 48e6b7a6-50f5-4782-a5d4-53bb8f07e226 0
```

### Wake Timers
```powershell
powercfg /setacvalueindex scheme_current SUB_SLEEP RTCWAKE 1
powercfg /setdcvalueindex scheme_current SUB_SLEEP RTCWAKE 1
powercfg /setactive scheme_current
```

## Hermes Gateway Config

### Vision Model (Free)
```yaml
auxiliary:
  vision:
    provider: custom
    model: gemini/gemini-3.6-flash
    base_url: http://127.0.0.1:20128/v1
    api_key: ${HERMES_CUSTOM_9ROUTER_API_KEY}
```

### Model Provider (Free)
```yaml
model:
  default: channel-researcher
  provider: 9router
providers:
  9router:
    base_url: http://127.0.0.1:20128/v1
    model: channel-researcher
    discover_models: true
    key_env: HERMES_CUSTOM_9ROUTER_API_KEY
```

### Health Check Cron
```bash
*/5 * * * * curl -s http://localhost:20128/v1/models || hermes gateway restart
```

## 9Router Free Models
- Use `channel-researcher` (round-robin 120+ free)
- Vision: `gemini/gemini-3.6-flash`
- Avoid `kr/claude-*` (paid/rate limited)

## Telegram Bot Trigger
```python
# Route /influencer -> Sistem 2, /bantuan -> Sistem 3
```

## Google Sheets Tracking
- Sheet ID: `1wLqdaYcjdaxXD1nEXPIv9PHObFhQPCi80cSiUHqEG8w`
- Tabs: AI_Influencer_Content, Help_Log, Job_Listings, Tool_DB, User_Profile

## Pitfalls & Fixes
| Issue | Fix |
|-------|-----|
| Gateway offline on lock | High Performance scheme + disable sleep |
| Vision 502/429 | Use gemini/gemini-3.6-flash |
| Model provider failed | Use channel-researcher |
| n8n port conflict | `taskkill /F /IM node.exe` |
| Discord ack_stale | `heartbeat_ack_max_age_seconds: 300` |
| Discord token invalid | Reset token di **correct Discord Application** (match Bot User ID). Verify: Discord app → Developer Mode ON → right-click bot → Copy User ID → match with Developer Portal Bot tab → 3 dots (⋮) → Copy ID. If mismatch, kick old bot, invite new bot from correct application. |
| TikTok video metadata blocked | Gunakan oEmbed API: `curl "https://www.tiktok.com/oembed?url=https://www.tiktok.com/@user/video/ID"` |
| hermes send CLI gagal | Gateway jalan via VBS scheduled task; CLI connect ke port beda. Pakai VBS wrapper untuk production. |
| Cross-platform context | Discord/Telegram/CLI session terpisah. Shared: memory, skills, config. |
| Discord token reset loop (15x fail) | Bot User ID mismatch. Check: log gateway shows bot User ID. Portal tab Bot → 3 dots → Copy ID. Must match. If not, kick bot, re-invite from correct application. |

## New Techniques This Session
- **TikTok oEmbed API**: Extract caption/metadata tanpa scraping (bypass yt-dlp error). Endpoint: `https://www.tiktok.com/oembed?url=https://www.tiktok.com/@user/video/ID` returns JSON with title/description/author
- **Power settings verified**: High Performance scheme (GUID `f8bf9830-1d5e-4187-a347-96873927865b`) + disable sleep/hibernate/rtcwake = gateway 24/7 survive lock screen
- **Gateway process**: 1 process handle Discord + Telegram via `Hermes_Gateway.vbs` scheduled task
- **9Router models**: 100+ free via `channel-researcher` combo; vision via `gemini/gemini-3.6-flash`; avoid `kr/claude-*` paid
- **Discord bot token reset**: Must reset token in **correct Discord Application** (match Bot User ID). Verify via: Discord app → Developer Mode ON → right-click bot → Copy User ID → match with Developer Portal Bot tab → 3 dots (⋮) → Copy ID. If mismatch, kick old bot, invite new bot from correct application.
- **Cross-platform context isolation**: Discord/Telegram/CLI sessions are separate (different session IDs). Shared: memory, skills, config. NOT shared: conversation history, topic context, temporary state.
- **hermes send CLI limitation**: CLI connects to different port than VBS gateway. For production, use VBS scheduled task; CLI only for testing.

## n8n on Windows (Node 24+) — Critical Fix
**Problem**: Global `n8n` command fails with `Cannot find module 'scripts/os-normalize.mjs'` because the npm wrapper script expects a different directory structure.
**Solution**: Install n8n locally in a clean directory and run via local binary:
```bash
mkdir -p ~/n8n-cli && cd ~/n8n-cli
npm init -y && npm install n8n@2.33.7
# Run via local binary (NOT global n8n command):
N8N_PORT=5678 N8N_HOST=localhost ./node_modules/.bin/n8n start
```
**Verification**: `curl -s http://127.0.0.1:5678/healthz` → `{"status":"ok"}`

## Fact-Validation Discipline (Bos Requirement)
**Rule**: NEVER report status as "working" or "done" without direct tool verification.
- 9Router: verify via `curl localhost:20128/v1/models` → count models, list free ones
- n8n: verify via `curl localhost:5678/healthz` → must return `{"status":"ok"}`
- Workflows: verify via `curl localhost:5678/api/v1/workflows` → count actual workflows
- Google Sheets: verify file exists via Drive API, not just local JSON template
- Discord/Telegram bots: verify via API `/getMe` endpoint
**Consequence of violation**: User loses trust, workflow breaks downstream. Always verify before reporting.

## Discord Bot Token Verification Checklist (Critical)
When Discord gateway fails with `Improper token has been passed`:
1. **Test token via API first**: `curl -H "Authorization: Bot TOKEN" https://discord.com/api/v10/users/@me` → returns bot info (id, username, discriminator)
2. **Extract Bot User ID from token**: First segment of token (before first `.`) is base64-encoded Application ID. Decode: `echo "TOKEN_PART1" | base64 -d`
3. **Match with server bot**: Discord app → Developer Mode ON → right-click bot in server → Copy User ID → must match Bot User ID in Developer Portal (Bot tab → 3 dots → Copy ID)
4. **If mismatch**: Bot in server is from different Application. Fix: Kick old bot from server → Invite bot from correct Application (OAuth2 URL Generator: client_id=APPLICATION_ID, scope=bot+applications.commands) → Reset token in correct Application → Update .env

## Gateway CLI vs VBS Scheduled Task
| Aspect | `hermes send` CLI | VBS Scheduled Task Gateway |
|--------|-------------------|---------------------------|
| Connection | Connects to different port | Runs `python -m hermes_cli.main gateway run` |
| Production | Testing only | **Production (24/7)** |
| Auto-restart | No | Yes (via Task Scheduler every 30min + 5min health cron) |
| Token reload | Manual restart | Via scheduled task restart |
| Debugging | Quick tests | Check `AppData/Local/hermes/logs/gateway.log` |