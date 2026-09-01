# Session 2026-08-10 Pitfalls Summary

**Date**: 2026-08-10 | **Focus**: n8n silent crash, vision_analyze fix, agent Python build, Discord 502 diagnosis

## Key Pitfalls Discovered

### 1. n8n Silent Crash on Node v24 (PITFALL #38/#52/#60)
- **Symptom**: `n8n start` exits silently, no logs, port 5678 not listening, healthz returns 000
- **Root Cause**: Node v24.16.0 incompatible with n8n 2.33
- **Fix**: Node 22.22 LTS portable ZIP (no-admin) side-by-side
  ```bash
  curl -L -o node22b.zip "https://nodejs.org/dist/v22.22.0/node-v22.22.0-win-x64.zip"
  unzip -q node22b.zip -d node22b
  ```
- **Verification**: `netstat -ano | findstr 5678` MUST show LISTENING + `curl -s -o /dev/null -w '%{http_code}' localhost:5678/healthz` MUST return 200

### 2. 9Remote = CLI, not Start Menu App (PITFALL #34/#39)
- **Wrong**: "Buka Start Menu → cari 9Remote"
- **Correct**: `9remote start` di terminal → QR + URL + Key → HP buka 9remote.cc/login
- Browser di remote HP = browser laptop, `localhost:5678` BENAR (bukan IP LAN)
- Jangan suruh Bos ganti localhost jadi IP saat remote

### 3. Vision_analyze Fixed (Not Broken) (PITFALL #43/#53)
- **Problem**: 404 / "Missing API key" / "Unable to process input image"
- **Root Cause**: 9Router process mati (bukan config model)
- **Fix Order**:
  1. `curl -s -m5 http://127.0.0.1:20128/health` → kosong = 9Router mati
  2. `9remote start` (background) + env `HERMES_CUSTOM_9ROUTER_API_KEY`
  3. `hermes config set auxiliary.vision.model kr/claude-sonnet-4.5`
  4. Test vision_analyze → jalan
- Rate-limit 429/400 sesaat = kuota gemini, tunggu (bukan rusak permanen)

### 4. Discord Gateway 502 = Nous Provider Overload (PITFALL #46/#56)
- **Symptom**: Discord screenshot `HTTP 502: Bad gateway` from Cloudflare
- **Root Cause**: Provider `nous` (tencent/hy3:free) overload → Cloudflare 502
- **NOT** Discord gateway error
- **Fix**: Ganti default model ke 9Router: `hermes config set model.provider 9router` + `model.default channel-researcher`

### 5. Workflow Not Showing in n8n UI (PITFALL #49)
- **Root Cause**: Missing `parentFolderId` + `activeVersionId` = `publishedVersionId`
- **Fix**: Create folder, assign workflow, create published_version, set versionId=activeVersionId=publishedVersionId, fix None fields

### 6. Credential "Found credential with no ID" (PITFALL #50)
- **Cause**: `node.credentials` = bare string `{'telegramApi': 'custom_id'}`
- **Fix**: Object with real DB ID: `{'telegramApi': {'id': '<DB_ID>', 'name': '<DB_NAME>'}}`
- Always `SELECT id FROM credentials_entity` first

### 7. Computer_use Cannot Control Browser Keyboard (PITFALL #55)
- Windows blocks UIAccess/foreground for background automation
- Browser tool cannot access localhost:5678 (sandbox)
- **Workaround**: Edit DB directly → Bos restart n8n in cmd → UI reload

### 8. 9Router Auto-start via Startup Folder (PITFALL #54/#58)
- File: `C:\Users\arija\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\start-9router.bat`
- Contains `HERMES_CUSTOM_9ROUTER_API_KEY` + `--tray --no-browser`
- n8n auto-start DISABLED (`start-n8n.bat.disabled`)

### 9. Python Agent Replaces n8n (PITFALL #61)
- Daemon at `C:\Users\arija\ziyan_agent\`
- Modules: telegram_bot, sheets (gspread), caption (9Router), scheduler (APScheduler), fb_upload (Graph API)
- Config: `config.yaml` with all tokens
- Launcher: `run_agent.bat` (venv + deps + run)
- Needs: Google Service Account JSON in `credentials/service_account.json`

### 10. TikTok Auto-post Reality Check
- NO public API for auto-post
- Official: Content Posting API (verified business + review)
- Unofficial: tiktok-uploader (browser automation, ban risk)
- Don't promise TikTok auto-post without official approval

## Environment State After Session

| Component | Status |
|-----------|--------|
| n8n | KILLED, auto-start disabled |
| 9Router | RUNNING, auto-start enabled |
| Python Agent | BUILT at `C:\Users\arija\ziyan_agent\` |
| Discord Gateway | WORKING (502 was Nous, not gateway) |
| Vision | WORKING (kr/claude-sonnet-4.5 via 9Router) |
| FB Token | In OneDrive/ziyan_pending/fb_page_token.txt |
| Google Sheets | Ready (needs Service Account JSON) |
| Telegram Bot | @Ziyanclipperbot token in config |

## Commands for Next Session

```bash
# Start agent
cd C:\Users\arija\ziyan_agent && run_agent.bat

# Verify 9Router
curl http://127.0.0.1:20128/v1/models

# Check vision
vision_analyze(image_url="C:\Users\arija\AppData\Local\hermes\cache\images\test.jpg", question="What's in this?")

# Check n8n if needed (Bos must start manually)
# n8n start (in cmd.exe)
```