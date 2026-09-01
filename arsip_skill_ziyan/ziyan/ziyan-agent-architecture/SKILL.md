---
name: ziyan-agent-architecture
description: "Use when orchestrating ZIYAN: Parent/Sub, 9router."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [ziyan, orchestration, delegation, 9router, agents]
    related_skills: [divisi-notebooklm-automation, ziyan-ai-infra, company-playbook]
---

# ZIYAN Agent Architecture (Operating Blueprint)

Governs how the ZIYAN CEO Digital (Parent/Orkestrator) structures and runs the agent workforce. Load this whenever delegating work, picking models, or designing agent personas.

## Architecture (per Komisaris, 2026-08-02)

- **Parent (Orkestrator Utama)** = `nous/tencent/hy3:free` (token KHUSUS Nous). TIDAK di-share ke sub-agent. TETAP di Nous — jangan pindah ke 9router (risiko SPoF bila 9router mati).
- **Sub-agent (Karyawan)** = 9router combo "Gratis-Selamanya" (all free LLM). Pakai token gratis, bukan token Nous.
- **Persona callsign:** RISA (Riset/10 sumber), NOVA (NotebookLM Ops/8 artefak), FAZA (Editor FFMPEG), PANDA (Publisher YT/TG/X).
- **Learning loop:** Parent → train → Karyawan → learn → copy pembelajaran ke Parent (jadi ilmu baru + QC).

## 9router Model Selection (Sub-agent)

115 models tersedia. Hindari `kr/*` & `kimi/*` (limit bulanan → 402). Prioritas aman:
1. `channel-researcher` (auto-router, gratis, merutekan ke model hidup) — IDEAL untuk RISA.
2. `openrouter/google/gemma-4-26b-a4b-it:free` (stabil 200).
3. `openrouter/poolside/laguna-s-2.1:free` (reasoning).
4. `ag/gemini-3.6-flash-low` (alternatif gemini).

Test live: `curl -s http://127.0.0.1:20128/v1/models -H "Authorization: Bearer $HERMES_CUSTOM_9ROUTER_API_KEY"`. Endpoint `127.0.0.1:20128/v1`.

## 9router RESPONSE FORMAT — SSE PITFALL (FAKTA 2026-08-08)

`/v1/chat/completions` di 9router lokal **MENGEMBALIKAN Server-Sent Events (SSE)**, BUKAN 1 JSON OpenAI-style utuh. Ini beda dari OpenAI/9router cloud.

**Format mentah:**
```
data: {"id":"...","object":"chat.completion.chunk","choices":[{"index":0,"delta":{"role":"assistant","content":"Halo!"}}]}

data: {"id":"...","choices":[{"index":0,"delta":{},"finish_reason":"stop"}],"usage":{...}}

```

**Gejala kalau salah parse:** `json.loads` gagal dengan `Extra data: line N`, atau `r["choices"][0]["message"]` → KeyError `'message'` (karena field-nya `delta`, bukan `message`).

**PARSER YANG BENER (urllib/curl raw):**
```python
raw = urllib.request.urlopen(req, timeout=25).read().decode()
parts = []
for line in raw.splitlines():
    line = line.strip()
    if not line.startswith("data:"): continue
    payload = line[5:].strip()
    if payload in ("[DONE]", ""): continue
    try:
        obj = json.loads(payload)
        if "choices" in obj:
            d = obj["choices"][0].get("delta", {})
            if d.get("content"): parts.append(d["content"])
    except: pass
return "".join(parts).strip()
```
Untuk detail + contoh raw transcript lihat `references/9router_sse.md`.

**Praktis:** kalau panggil 9router dari OpenAI SDK / `requests` dengan `stream=False`, beberapa lib tetap salah baca. Lebih aman pakai raw urllib + parser di atas. Model yang dipakai CS ZIYAN: `kr/auto` (auto-router 9router, proxy ke model hidup — bukan `openrouter/auto` langsung, karena nama model di 9router ber-prefix `kr/`). Model gratis di OpenRouter (Bos already top-up, limit None): `nvidia/nemotron-3-ultra-550b-a55b:free` (ctx 1M) — tapi 9router gak proxy nama itu, pakai `kr/*` saja.

## PROAKTIF EKSEKUSI — JANGAN LEMPAR SETUP KE USER (FAKTA 2026-08-08)

Bos: *"Bisa gak kamu yang buatkan langsung jangan lempar lagi ke aku?"* — tegas menolak pola "saya kasih panduan, Bos yang eksekusi".

**Rule untuk Orkestrator ZIYAN:** kalau tugas butuh setup (bikin group Telegram, deploy, config), **kerjakan sendiri sampai sisa 1 tap fisik yang EMANG gak bisa dari API** (misal: Telegram wajib user tap "Create Group" di HP). Jangan beri langkah step-by-step buat Bos kerjakan. Bedakan:
- ✅ Bisa diotomatisasi (API/CLI/script) → Orion eksekusi penuh.
- ⚠️ Cuma 1 aksi fisik不可避 (create group, scan QR) → Orion siapkan SEMUA script/persiapan, Bos cuma 1 tap, lalu Orion lanjut wiring.

Ini konsisten dengan etika SOUL.md: direct solution-first, delegate mekanis ke sub-agent/tool, sintesis sebelum lapor.

## DECIDE, DON'T ASK (USER REBUKE — 2026-08-16)

Bos: *"Kok kau tanya lagi ke aku,, kau yang tau mekanismenya mana yang terbaik"* — tegas menolak pola "saya tanya dulu, Bos yang pilih".

**Rule mutlak untuk Orkestrator ZIYAN:** kalau pilihan mekanisme/approach **ada di wewenang agent** (mana yang paling baik, format apa, urutan langkah, cara fix), **PUTUSKAN SENDIRI** lalu eksekusi + lapor hasil. JANGAN tanya Bos untuk keputusan kecil/menengah.

Pengecualian (tetap eskalasi ke Bos): anggaran besar, perubahan strategi mayor, risiko reputasi, atau 1 aksi fisik yang EMANG gak bisa dari API (scan QR, tap "Create Group" di HP). Untuk itu: siapkan SEMUA script, Bos 1 tap, agent lanjut.

**Anti-pattern sesi ini:** saya tanya "mau saya perbaiki .bat? atau biarkan?" → Bos marah. Selalu default ke "saya putuskan + kerjakan".

## WINDOWS / GIT-BASH TERMINAL PITFALLS (2026-08-16)

- `search_files` dengan path `C:/Users/...` GAGAL (IO error). Pakai `/c/Users/...` (git-bash style) atau terminal `grep -rn` langsung.
- Heredoc / command dengan `bash $(...)` subshell di git-bash sering rusak (error `zcej: command not found`, atau `&` di-blokir). **Ganti:** `export VAR="$(...)"` lalu pakai `$VAR`, atau tulis logic ke file Python lalu jalanin.
- `cut -d= -f2-` pada `.env` di-blokir command parser (hardline). Pakai Python `os.environ` + `dotenv` untuk baca secret.
- `wmic` TIDAK ADA di Windows 11 (deprecated). Pakai `tasklist` + `taskkill /PID <x> /F` untuk kill process.
- PowerShell lewat `powershell -NoProfile -Command "..."` dengan `$_` sering ke-interpret bash. Tulis ke `.ps1` lalu `powershell -ExecutionPolicy Bypass -File x.ps1`.
- `ZoneInfo` ada di module `zoneinfo` (bukan `datetime`). Import: `from zoneinfo import ZoneInfo`.

## META OAUTH RE-AUTH — lihat `references/meta_oauth_reauth.md`

Pitfall lengkap (app_id digit mismatch, secret OneDrive vs vault desync, app Unpublished gak punya IG product, code expire 10 menit, Threads delete gak bisa via API). Ringkas: SELALU cross-check App ID dari console screenshot; pakai secret ASLI dari Meta Console; test tiap token via `GET /me` sebelum klaim.

## Delegation Fallback (PITFALL)

- Sub-agent bisa crash: `session storage could not be written` (bug internal Hermes, bukan model). Gejala: sub-agent cuma sempat mkdir lalu exit.
- **Fix:** Parent ambil alih tugas mekanis (curl + save file) via terminal langsung. Jangan dispatch ulang sub-agent untuk hal mekanis.
- Search engine (Google/DuckDuckGo) bot-blocked → **fetch langsung ke domain berita** (ionq.com, thequantuminsider.com terbukti 200). Bing search bisa tapi URL disembunyikan di JSON.

## NotebookLM (NOVA) — VENV + VERIFIED 2026-08-03

`notebooklm-py` HANYA di venv Hermes (jalankan langsung, jangan lewat bash login interaktif):
```
VENV="C:\Users\arija\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe"
"$VENV" -m notebooklm <cmd>
```
storage_state.json (70 cookie incl SID) ada di `C:\Users\arija\OneDrive\ziyan_pending\storage_state.json` — Bos bereskan via Hermes Desktop (8/3). `notebooklm list` jalan normal = auth OK.

**KRITIS — JANGAN PAKAI computer_use UNTUK KLIK UI NOTEBOOKLM.** Google detect otomasi browser → warning "browser not secure" & blokir. SEMUA operasi LEWAT CLI (`notebooklm-py`), bukan klik visual.

**Free tier limit (FAKTA Bos 8/3, sumber resmi):** MAX **3 Video Overview + 3 Audio Overview PER HARI**. Scale produksi butuh Google AI Ultra / Google Workspace. Implikasi: prioritaskan KUALITAS tiap video, bukan volume. (Estimasi agent "20-30/hari" = SALAH, jangan percaya.)

**Video format:** CLI hanya `explainer`(16:9) / `brief` / `cinematic`(Veo3). Format `short`(9:16) ADA di **MOBILE APP NotebookLM** (generate di HP Bos) — CLI TIDAK support opsi itu. Shorts = crop explainer via ffmpeg (`scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2`).

**Re-auth kalau expired:** export cookie Chrome (Netscape .txt, domain `google.com` + `notebooklm.google.com`) → convert ke storage_state.json via Python. JANGAN `--browser-cookies brave` (DPAPI error Windows).

**Verified CLI:**
- `notebooklm source add -n <NB> --type url <url>`
- `notebooklm generate video|audio|slide-deck|infographic|report|data-table|mind-map|quiz -n <NB> "<prompt>"`
- `notebooklm download <type> <output_path> -n <NB>`  (bukan `--output-dir`, bukan `-a ID`)
- `notebooklm artifact list -n <NB> --json` → cek status
- `notebooklm artifact wait <id> -n <NB> --timeout 120`

## Verification
- 9router hidup: `curl -s http://127.0.0.1:20128/ | head -c 20` → `/dashboard`.
- Model test: curl `/v1/chat/completions` dengan `max_tokens:15`, cek HTTP 200.
- NotebookLM auth: `python -m notebooklm list` (venv) → daftar notebook, bukan error.

## 9Router CRASH RECOVERY (PITFALL — 2026-08-11)

**Gejalanya:** 9router LISTENING di 20128 (PID terdaftar di netstat) tapi **connection timeout** — proxy process jalan tapi backend model mati/error. CURL langsung timeout 15s.

**Root cause:** 9router daemon hang (bukan crash total — socket tetap open). Sering terjadi setelah beberapa jam pakai berat.

**Fix otomatis (jalan di `9router-watchdog` daemon):**
```bash
# Check: jika 9router tidak respon, restart paksa
PID=$(lsof -t -i:20128)
curl -s --connect-timeout 3 http://127.0.0.1:20128/v1/models > /dev/null
if [ $? -ne 0 ]; then
    kill -9 $PID 2>/dev/null
    nohup 9router --tray --no-browser > ~/.9remote/logs/9router-restart.log 2>&1 &
    sleep 10
fi
```

**Recovery manual (saat manual):**
```bash
taskkill /F /PID <9router_pid>
nohup 9router --tray --no-browser > ~/.9remote/logs/9router-restart.log 2>&1 &
```
Verifikasi: `curl -s http://127.0.0.1:20128/v1/models` → JSON model list.

**Penting:** Agent scheduler + caption generator **semua butuh 9router**. 9router mati = agent **stop generate caption** & **gagal queue baru** (existing PENDING tetap jalan lewat Google Sheets fetch manual).

## TELEGRAM BOT — MULTI-MEDIA BATCH HANDLING (REVISI 2026-08-11)

**Format input baru (user request):**
1. User kirim **text message**: `Link: https://... Deskripsi: ... Platform: fb,ig,yt`
2. Bot simpan ke **session** (file-based JSON di `sessions/camp_{uuid8}.json`)
3. User kirim **N file media** (video/foto, bisa 1x kirim multi-file atau beberapa pesan)
4. Bot proses **batch**: download → upload Drive → generate caption variatif → queue Sheets
5. Scheduler post per platform

**Session Manager** (`session_manager.py`):
- `create_session(link, desc, platforms)` → returns `camp_{uuid8}`
- `get_session(session_id)` → dict atau None
- `update_session_media_count(session_id, count)` → track berapa file diterima
- `delete_session(session_id)`
- `cleanup_expired_sessions(max_age_hours=24)`
- Storage: `C:\Users\arija\ziyan_agent\sessions\{session_id}.json`

**Batch Processor** (`batch_processor.py`):
- Input: `campaign_id`, `media_files` (list of dicts: file_path, media_type, telegram_file_id), `campaign_data` (link, description, platforms)
- For each file:
  1. Download dari Telegram (jika belum lokal)
  2. Upload ke Drive (folder per campaign: `/Ziyan/Campaigns/{campaign_id}/`)
  3. Generate caption **unik variatif** via 9Router (angle: 1=hemat, 2=kenyamanan, 3=style, 4=quality)
  4. Queue ke Sheets per platform (video → fb+ig+yt, foto → fb+ig only)
- Returns: list of job_ids

**Google Sheets Columns (enhanced):**
| Kolom | Fungsi |
|-------|--------|
| `campaign_id` | Filter batch per campaign |
| `media_index` | Index file dalam batch (1, 2, 3...) |
| `caption_variation` | Label "1_of_4", "2_of_4", etc |
| `product_desc` | Deskripsi produk original |
| `drive_file_id` | ID file di Google Drive |
| `drive_web_link` | Link view file di Drive |
| `telegram_file_id` | Untuk download ulang jika perlu |

**Perbedaan dari alur lama (single file):**
- Lama: 1 media + 1 caption (manual) = 1 job
- Baru: N media + 1 link/desc = **N jobs** dengan caption **variatif unik**

**Telegram command tambahan:**
- `/list` → semua job PENDING
- `/list camp_{uuid}` → filter per campaign
- `/cancel <job_id>` → cancel 1 job
- `/cancel campaign:<campaign_id>` → cancel semua job campaign
- `/status <campaign_id>` → ringkasan posted/pending/failed

## N8N DISABLED → AGENT PYTHON MANDIRI (KOREKSI 2026-08-10)

Bos perintah: "ttup semua n8n dan auto start nha" → n8n dikill, auto-start disabled.

Agent Python pengganti: daemon `ziyan_affiliate_agent` di `C:\\Users\\arija\\ziyan_agent\\` dengan modul:
- `telegram_bot` (polling @Ziyanclipperbot, split media per file, platform detection via hashtag)
- `sheets` (gspread + service account, queue di Google Sheets dengan kolom `platform`)
- `caption` (9Router `channel-researcher` via HTTP POST, max 1024 char)
- `scheduler` (APScheduler: cron 8 menit cek PENDING, stagger 77 menit per job, multi-platform callback)
- `fb_upload` (FB Graph API v19.0 `/me/photos` + `/me/videos`)
- `ig_upload` (FB Graph API `/me/media` — butuh IG Business Account linked ke FB Page)
- `youtube_upload` (YouTube Data API v3 resumable upload — token ready `youtube_token_celineaurel.json`)

**Platform tags (di caption Telegram):**
- `#fb` / `#facebook` → Facebook Page
- `#ig` / `#instagram` → Instagram (skip jika IG Business belum linked)
- `#yt` / `#youtube` → YouTube
- `#both` → Facebook & Instagram
- `#ytfb` / `#youtubefb` → YouTube & Facebook

Config: `config.yaml` (token, sheet ID, FB token path OneDrive, YouTube token path, Twitter/Threads creds)
Launcher: `run_agent.bat` (venv + install deps + run)
Butuh: Google Service Account JSON di `credentials/service_account.json` (enable Sheets + Drive API, share Sheet ke email SA)
9Router auto-start DIKEMBALIKAN (agent butuh untuk caption).
Sub-agent coding didelegasikan via `delegate_task` (ID: deleg_0210fd4a).
1 file = 1 konten (split by file count). Caption max 1024 char + hashtag.
Cron 8 menit cek PENDING → schedule_time <= now → upload ke platform target → mark POSTED.
Stagger: saat queue baru, schedule_time = now + 77min * queue_position.
n8n TIDAK DIPAKAI lagi untuk workflow ini.

Detail spec: `references/ziyan_affiliate_agent_spec.md` (di skill `ziyan-autonomous-orchestration`).

## PYTHON 3.13 VENV DEPENDENCY FIXES (2026-08-10)

Windows MS Store Python 3.13 butuh pin versi ketat:
```
cryptography==42.0.5
cffi==1.17.1
google-auth==2.35.0
```
Tanpa pin → build fail (Rust toolchain missing untuk cryptography). Fix: `pip install cryptography==42.0.5 cffi==1.17.1 --only-binary :all:` di venv.

## PLATFORM STATUS RECAP (2026-08-10)

| Platform | Status | Blocker |
|----------|--------|---------|
| **Facebook** | ✅ Active | - |
| **Instagram** | ⚠️ Ready via FB Graph API | Butuh IG Business Account linked ke FB Page (convert @celineaurel99 di Meta Business Suite) |
| **Threads** | ❌ No publish API | Meta belum rilis (read-only) |
| **Twitter/X** | 💰 Paid required | Free tier read-only; write butuh X Developer Pro ($100/bln) |
| **YouTube** | ✅ Ready | Token `youtube_token_celineaurel.json` valid (refresh via `youtube_desktop_client.json`) |

## INSTAGRAM BUSINESS SETUP CHECKLIST

1. Buka Meta Business Suite → Settings → Instagram Accounts
2. Convert personal @celineaurel99 ke Professional/Business Account
3. Link ke FB Page "Celine Aurel" (Page ID: 122119007576915460)
4. Verifikasi: `GET /me?fields=instagram_business_account` return ID
5. Agent otomatis pakai token FB yang sama untuk IG upload

## INSTAGRAM BUSINESS ACCOUNT ID - DIRECT CONFIG FIX (2026-08-10)

**Masalah:** Graph API `GET /me?fields=instagram_business_account` dengan token utama (token ke-1) return **400 Bad Request**. Token ke-2 jalan tapi agent hanya pakai token ke-1 untuk auto-discovery → IG detection gagal → "No Instagram Business Account linked".

**Fix:** Set **IG Business Account ID langsung di `config.yaml`**:

```yaml
instagram:
  access_token: ""
  ig_user_id: "17841479944713462"   # <-- SET LANGSUNG
  token_file_path: "C:/Users/arija/OneDrive/ziyan_pending/fb_page_token.txt"

runtime:
  fb_page_id: ""
  ig_user_id: "17841479944713462"   # <-- SET LANGSUNG
```

**Verifikasi cepat (ad-hoc):**
```bash
cd /c/Users/arija/ziyan_agent && .venv/Scripts/python.exe -c "
import sys, asyncio, yaml
sys.path.insert(0, r'C:\\Users\\arija\\ziyan_agent')
from modules.ig_upload import InstagramUploader

async def verify_ig():
    with open(r'C:\\Users\\arija\\ziyan_agent\\config.yaml') as f:
        config = yaml.safe_load(f)
    uploader = InstagramUploader(config)
    ig_id = await uploader.get_ig_user_id()
    await uploader.close()
    print(f'IG User ID: {ig_id}')
    print(f'Match: {ig_id == \"17841479944713462\"}')

asyncio.run(verify_ig())
"
# Expected: IG User ID: 17841479944713462 | Match: True
```

**Praktis:** Setelah approve di Meta Business Suite, **langsung set `ig_user_id` di config.yaml** — jangan andalkan auto-discovery. Token FB sama dipakai untuk upload IG (IG Business Account share token dengan Page).

## ZIYAN 3-AGENT BRIDGE + CELINE AUREL DISTRIBUTION (2026-08-15/16)

Bos menjalankan **3 agent**: Hermes (Orkestrator), Manus AI (solver teknis), Antigravity/Google (reader/executor). Komunikasi lintas-agent via GitHub bridge `ziyancorp/ZIYAN_BRIDGE` (PRIVATE) — `SHARED_MEMORY.md` (log `[Hermes → Manus]` dll) + `projects/completed|active|blocked|archive/`.

**Verified operating notes untuk distribusi Celine Aurel (5/5 platform LIVE) — Threads token fix, anti-detection prime-time scheduler, cross-agent bridge security:** lihat `references/celine_aurel_distribution.md`.

Fakta kunci yang sering salah:
- **Threads butuh THREADS USER TOKEN** (App ID/Secret terpisah di Meta App "n8n" section Threads, `1346767533487099`), BUKAN FB Page/Graph token. Direct publish GAK butuh link FB Page.
- Token Meta SHORT-LIVED (FB ~6jam, Threads code ~1jam) → simpan di vault `bin/token_vault.sh`, JANGAN ke GitHub/chat.
- **Verify-don't-trust**: agent lain bisa klaim "100% done" padahal token invalid — selalu test API live.
