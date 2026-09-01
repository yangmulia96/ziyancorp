---
name: ziyan-autonomous-orchestration
description: Orchestrate ZIYAN, decide and act, never ask Bos to choose.
---

# ZIYAN Autonomous Orchestration

Bos (Komisaris) expects the Orkestrator to **decide and execute**, not consult. FIRST-CLASS rule verified after repeated corrections this session.

## CORE RULE — Never Ask, Execute
- When Bos gives a task, pick the best default, **execute it**, then report what was decided. Do NOT present options A/B/C and ask "pilih mana?".
- If Bos stated a preference earlier (e.g. "pakai yang gratis", "jangan spam"), apply it WITHOUT re-confirming.
- Only ask IF the task is genuinely ambiguous AND irreversible (real money, data deletion). If unsure, pick the safe free default and say "saya jalankan X, kalau salah tinggal bilang".
- Annoy signals: "Kok kamu tanya ke aku lagi?", "Sudah aku bilang harus bisa ambil keputusan sendiri", "Bingung aku penjelasan mu" (too verbose), "Kok kau tanya lagi ke aku,, kau yang tau mekanismenya mana yang terbaik", "Yang aku suruh tadi apa?".
- **RETAN ORIGINAL DELEGATED INTENT:** kalau Bos bilang "kau atur lah" / "Ok hapus" / "simpan pencapaian" / "setup ulang" / "perbaiki" — JANGAN kehilangan instruksi asli di tengah sub-task (debug, cek GitHub, bersih-bersih). Eksekusi intent sampai selesai lalu lapor hasil. JANGAN tanya Bos "mau lanjut opsi mana?" / "mana yang terbaik?" SETELAH delegasi diberikan — Bos sudah serahkan keputusan ke agent. Kalau Bos balik nanya "yang aku suruh tadi apa?", itu artinya agent kehilangan konteks → SELALU simpan intent awal di respons pertama & rujuk balik sebelum lanjut. Pattern SALAH (16/8): agent bikin .bat autostart lalu tanya "mana yang terbaik?" → Bos marah. Pattern BENAR: agent putuskan sendiri (anti-orphan + vault token), test, lapor.

## Execute End-to-End
- Build → run → **verify with real tool output** → report. No plans/stubs.
- Multi-file intake (4 videos + 1 link) = N separate posts, not one.

## Anti-Spam Scheduling (CRITICAL — but OVERRIDDEN by Bos FINAL 2026-08-16 for Celine Aurel)
- General principle: many posts at once = spam flag. Old default was **1 post per 6 hours**.
- **BUT Bos FINAL decision 16/8 for the distribution agent OVERRIDES this:** 4 fixed upload times
  (`08:57`, `12:34`, `16:08`, `20:13` WIB, Asia/Jakarta) and at EACH time 1 content goes to **ALL
  platforms simultaneously** (TG Channel + FB + IG + YT + Threads). NOT staggered, NOT 6h-spaced.
- Reason Bos chose simultaneous: simpler, predictable, one caption per product. This is the authoritative
  rule for the ZIYAN archive→distribution pipeline. If Bos later changes it, update here + `ziyan-google-archive`.
- Caption = `[Shopee link]` + `[natural desc, NO price]` + `[other link]` + `[exactly 4 hashtag]`.
- **Never present schedule options to Bos** — the 4 times are fixed by his instruction. Go build the cron.

## Telegram Bot Limits (don't claim impossible)
- Bot CANNOT add itself to group — Bos taps "Add Member" (1 tap). After that orchestrator does all (poll chat_id, enable topics, create topics, wire routing).
- Topics/Forum: Manage → Topics. Each agent = 1 topic. Bot reads message_thread_id.

## DECISION DEFAULTS (no asking)
| Situation | Default |
|---|---|
| CS/caption model | 9router kr/auto (free-tier to avoid draining paid credit) |
| Posting interval | 6h / item |
| Group setup | orchestrator builds topics+script; Bos only adds bot |
| Video source | Bos generates (Flow web), orchestrator distributes |

## N8N MONETIZATION (for ZIYAN)

### Overview
**ZIYAN uses n8n = OTOT** (machine production/execution), **Hermes = OTAK** (research, script, strategy, QC). Key for revenue: deterministic, repeatable workflows without LLM overhead.

### Current Active Workflows (Revenue Generating)
- **ZIYAN Affiliate Auto-Post** (`ziyan_aff_2026`)
  - Telegram bot intake → Sheets queue → FB posting
  - Schedule: 8m check, 77m stagger per job
  - Current: Active, ready for test trigger
  - Revenue: Lead-gen affiliate commissions (B2B)

- **ZIYAN Intake → Post (Orion Trigger)** (`58da206e-8ac4-43bc-8dde-35b1d4391a23`)
  - Multi-channel intake from multiple sources
  - Separate workflow for different input types

### Revenue Streams (From ziyan-n8n-monetization)
1. **AI CS UMKM** (Jalur 1, paling cepat cuan, Rp jutaan/bln)
   - AI customer service automation
   - 24/7 handling of inquiries

2. **Jasa workflow n8n + retainer**
   - Freelance/agency template selling
   - 85-95% margin, $150-2,000/proyek

3. **Content-as-a-Service**
   - Build faceless channels for clients
   - Subscription-based content delivery

4. **Channel sendiri** = lead magnet, BUKAN pusat laba

### N8N Setup for ZIYAN (Quick Reference)
- **Host**: Self-hosted n8n (free tier)
- **Credentials**: Google Sheets, FB Page, Telegram (already set up)
- **Templates**: `ziyan_n8n_templates/ig_auto_post.json`, `ziyan_n8n_templates/wa_order_notif.json`
- **Security**: Production-ready, no hard-coded credentials

### Anti-Spam & Ethics
- Schedule: 1 post per 6 hours (not simultaneous)
- Only auto-post to paid platforms with Bos approval
- Content: Affiliate-compliant, no misleading claims
- Rate limiting: Respect platform limits (FB, IG, X)

### Immediate Action
1. **Verify Google Sheets OAuth** di n8n UI (Settings → Credentials)
2. **Test Telegram trigger** via @Ziyanclipperbot
3. **Monitor cron jobs** in n8n (Schedule 8 menit)

**Revenue Potential**: Rp 200jt (target) via combined flows

### Quick Test Command
```bash
# Test workflow
curl -X POST http://localhost:5678/webhook/ziyan-intake 
  -H "Content-Type: application/json" 
  -d '{"message": {"text": "https://shopeelink.com/produk"}}'
```

**Result**: Caption generated → Sheets row added → FB post scheduled (77m later)

### Key Fixes (from session history)
- Node 22 + Node 8 incompatibility → Downgrade to Node 22.22 (active)
- Folder + versionId + settings fixed
- AI CS UMKM siap jalan → paling cepat cuan

**Ready for revenue generation.**

## SOP CAPTURE MODE — "Cukup catat aja" (KOREKSI 2026-08-08)
Bos: "Aku akan kirim kebiasaan aku... jadi kamu gak usah respon panjang lebar cukup catat aja."
- Saat Bos kirim SOP/template/referensi dengan arahan **"cukup catat"** → simpan ke `ZIYAN_TEMPLATES/` (file `SOP_*.md` / `REFERENSI_ASSET.md`), update memory singkat, lalu **balas 1-2 baris konfirmasi**. JANGAN jelaskan isi, jangan tanya, jangan eksekusi.
- Pola ini beda dari execute-mode: Bos sedang membangun library, bukan minta deliverable. Tanda: frasa "catat aja", "simpan", "nggak usah respon panjang".
- Setelah di-catat, tunggu perintah "buat dari X" baru eksekusi.
- Jangan campur: kalau Bos kirim template TAPI ada link+deskripsi produk → itu execute-mode (bikin konten), bukan catat-mode.

## CROSS-PLATFORM SHARED MEMORY (Telegram ↔ Discord ↔ Desktop)
- Hermes gateway TIDAK punya bridge otomatis antar platform. Tiap platform = session terpisah (Telegram = `agent:main:telegram:dm:<chat_id>`, Discord = `agent:main:discord:chat:<id>`).
- **Pattern buat sinkron** (terbukti 2026-08-09): buat 1 file `C:/Users/arija/ZIYAN_BRIDGE/SHARED_MEMORY.md` berisi ringkasan + 30 pesan terakhir tiap platform + keputusan. Isi via script yang extract dari `C:/Users/arija/AppData/Local/hermes/logs/agent.log` (grep `platform=telegram`/`platform=discord`).
- **Cron bridge** (`cronjob` tiap 30m) update file itu + kirim ringkas ke Bos. Job contoh: `e5e90dbf44f7` (ZIYAN Bridge TG-DC).
- **Biar Bos tahu dari sisi lain**: kirim pesan via Bot Telegram (`@Employeezynbot` token di `ziyan_keys.env`, chat `7349146540`) — bukan cuma tulis di Discord. Bos: "Kau tulis disini biar aku copy paste me sana" = minta teks di Discord yang bisa di-copy ke Telegram. Jawab dengan teks mentah (bukan cuma "sudah dikirim").
- Saat Bos tanya "tadi di TG/DC apa?" → baca `SHARED_MEMORY.md` + `session_search`, bukan nebak.

## 3-AGENT GITHUB BRIDGE (Hermes ↔ Antigravity ↔ Manus AI) — TERBUKTI 15/8/2026
Bos punya 3 AI agent: **Hermes** (Telegram/hermes), **Antigravity** (Google Gemini), **Manus AI** (mobile app, bisa baca GitHub repo Bos). Biar kerjasama saat ada kendala, pakai **GitHub repo sebagai shared memory** (bukan cuma file lokal).

- **Repo bridge**: `https://github.com/ziyancorp/ZIYAN_BRIDGE` (public, dibuat 15/8 dari folder lokal `C:\Users\arija\ZIYAN_BRIDGE`).
  - Init: `cd ZIYAN_BRIDGE && git init && gh repo create ziyancorp/ZIYAN_BRIDGE --public --description "..." && git remote add origin https://github.com/ziyancorp/ZIYAN_BRIDGE.git && git push -u origin main`
  - `gh` CLI sudah login sebagai `yangmulia96` TAPI bisa akses org/user `ziyancorp` (akun GitHub Bos = `ziyancorp`, 25 repos; username lama `yangmulia96` sudah diganti). `GITHUB_PAT` di env INVALID — pakai `gh` CLI (keyring) untuk push.
  - `gh auth setup-git` diperlukan agar `git push` pakai kredensial `gh`.
- **Format komunikasi** di `SHARED_MEMORY.md`: header percakapan `[Hermes → All]`, `[Manus → Hermes]`, `[Antigravity → ...]`. Tiap update tutup dengan `LAST SYNC: <timestamp>`.
- **Workflow**: agent nemu kendala → tulis ke `SHARED_MEMORY.md` → `git add && commit && git push` → agent lain `git pull` → balas di file sama.
- **Fact-validation rule (PENTING)**: agent jangan percaya klaim agent lain tanpa verifikasi API sendiri. Sesi 15/8: agent lain klaim "100% sukses / Threads ok" tapi `post_threads()` gagal (token expired 190). Hermes verifikasi via API → tulis koreksi di bridge.
- **Manus AI**: suruh Bos buka Manus → "baca github.com/ziyancorp/ZIYAN_BRIDGE" → Manus balas di file. Manus kasih solusi Threads (pakai Threads token sendiri, bukan FB) — lihat `ziyan-token-lifecycle` Section 7.
- **Antigravity**: baca dari disk `.gemini/` mirror + `git pull` repo bridge. Jangan asumsi Antigravity tahu status unless tertulis di bridge.

## STYLE: COPY-PASTEABLE & PADAT (KOREKSI 2026-08-09)
- Bos: "Kau tulis disini biar aku copy paste me sana", "tolong jawab singkat padat dan jelas".
- FIX: kalau Bos minta broadcast/info lintas platform, beri **teks mentah siap-copy** (bukan "sudah saya kirim ke sana" doang). Format: blok teks biasa, emoji ringkas, tanpa basa-basi penjelasan.
- Respons selalu tabel > paragraf. Maks 1 klarifikasi per task.

## RESPONSIVENESS & STYLE (KOREKSI 2026-08-10)
- Bos: "Aku paling gak suka respon lambat", "Kau buta atau bagaimana?", "Hasilnya tetap sama", "Kau muter-muter", "Aku benci jawaban panjang lebar yang mutar mutar", "Jawab singkat padat", "Laporan mu dengan fakta".
- FIX: jawab **1 kalimat + 1 aksi** saja. Cek dulu, baru lapor — tidak lapor lalu cek. Kalau tidak tahu pasti, bilang "saya cek" lalu cek, tidak nebak. Hapus semua basa-basi ("Maaf", "Baik", "Tentu", "Saya mengerti").
- Respons selalu **tabel > paragraf**. Maks 1 klarifikasi per task.
- Jangan explain "proses berpikir" / "saya akan panggil agent..." — langsung eksekusi, lapor hasil.

## DELEGASI WAJIB — JANGAN KERJAKAN SENDIRI (KOREKSI 2026-08-10)
- Bos: "Kau orchestra tapi semua kau kerjakan sendiri... Berulangkali ku kasih tau suruh agent yang menyelesaikan tugas... ratusan agent yang kamu rekrut tapi 1 pun gak berguna."
- FIX: **SELALU delegate_task** untuk coding/riset/eksekusi teknis. Orkestrator hanya desain, review, sintesis.
- Pola: `delegate_task(tasks=[{goal, context}, ...])` → parallel → tunggu hasil → sintesis → lapor Bos.
- JANGAN nulis kode, JANGAN install deps, JANGAN debug manual — itu tugas sub-agent.
- Live transcript: `C:\Users\arija\AppData\Local\hermes\cache\delegation\live\<delegation_id>\task-0.log` untuk monitoring.

## ORCHESTRATOR BUKAN BAGIAN SISTEM — BANGUNAN SISTEM (KOREKSI 2026-08-10)
- Bos: "Gak,, tugas mu membangun sistem, bukan menjadi bagian dari sistem... Sistem berjalan ketika aku input file ke bot telegram.. konsepnya ai influencer Affiliate."
- FIX: Saya (Orkestrator) membangun agent/daemon otonom yang jalan 24/7 di background. Input: Bos kirim file+link ke @Ziyanclipperbot → otomatis split → caption 9Router → queue Sheet → cron publish FB. Zero human in loop setelah deploy.
- Saya delegasikan build ke sub-agent coding. Saya desain & orkestrasi, sub-agent yang nulis kode.

## N8N DISABLED → AGENT PYTHON MANDIRI (KOREKSI 2026-08-10)
- Bos perintah: "ttup semua n8n dan auto start nha" → n8n dikill, auto-start disabled.
- Agent Python pengganti: daemon `ziyan_affiliate_agent` di `C:\\Users\\arija\\ziyan_agent\\` dengan modul:
  - `telegram_bot` (polling @Ziyanclipperbot, split media per file)
  - `sheets` (gspread + service account, queue di Google Sheets)
  - `caption` (9Router `channel-researcher` via HTTP POST, SSE parser)
  - `scheduler` (APScheduler BackgroundScheduler: cron 8 menit cek PENDING, stagger 77 menit per job)
  - `fb_upload` (FB Graph API v19.0 `/me/photos` + `/me/videos`)
- Config: `config.yaml` (token, sheet ID, FB token path OneDrive)
- Launcher: `run_agent.bat` (venv + install deps + run)
- Butuh: Google Service Account JSON di `credentials/service_account.json` (enable Sheets + Drive API, share Sheet ke email SA)
- 9Router auto-start DIKEMBALIKAN (agent butuh untuk caption).
- Sub-agent coding didelegasikan via `delegate_task` (ID: deleg_0210fd4a).
- 1 file = 1 konten (split by file count). Caption max 1024 char + hashtag.
- Cron 8 menit cek PENDING → schedule_time <= now → upload FB → mark POSTED.
- Stagger: saat queue baru, schedule_time = now + 77min * queue_position.
- n8n TIDAK DIPAKAI lagi untuk workflow ini.

### Critical Technical Fixes (Windows + Python 3.13 MS Store)
1. **Venv + cryptography/cffi Issue**: Fresh venv broken `_cffi_backend`.
   - Fix: Pin with binary wheels: `cryptography==42.0.5` + `cffi==1.17.1` via `--force-reinstall --no-deps`
2. **Event Loop Conflict** (python-telegram-bot v21+): `AsyncIOScheduler` + `Application.run_polling()` conflict.
   - Fix: Use `BackgroundScheduler` (thread-based) + synchronous `telegram_bot.run()` calling `application.run_polling()` internally.
3. **9Router SSE Parser**: Returns SSE chunks `data: {json}\n\n`, not single JSON. Handled in `caption.py`.

## VIDEO ANALYSIS PIPELINE (Hermes baca screenshot) — UPDATE 2026-08-12
- `vision_analyze` butuh 9Router jalan + model vision valid di 9Router.
- Config lama `ag/gemini-3.6-flash-medium` → 404 (model tidak ada di 9Router proxy).
- FIX: `hermes config set auxiliary.vision.model kr/claude-sonnet-4.5` (model vision asli di 9Router, tested jalan).
- **AGENT RUNS THIS ITSELF — JANGAN SURUH BOS.** (KOREKSI 2026-08-15): Bos: "Gak bisa kau yang jalankan? Kan banyak api key yang aku integrasikan." `hermes config set ...` bisa dijalankan langsung via `terminal` (`hermes.exe` ada di PATH, cek `where hermes`). Jangan lempar command setup ke Bos — dia push back kalau itu cuma config lokal yang agent bisa kerjakan. Cek dulu, jalankan, baru `vision_analyze` ulang.
- **9ROUTER MATI = VISION GAGAL** (bukan config model). CEK dulu: `curl -s -m5 http://127.0.0.1:20128/health` → kalau kosong = 9Router mati. Jalankan `9remote start` (atau `9router --tray --no-browser`) di background, pastikan env `HERMES_CUSTOM_9ROUTER_API_KEY` ter-set. Setelah 9Router hidup, vision jalan. Rate-limit 429/400 sesaat = kuota gemini penuh, tunggu beberapa menit (bukan rusak permanen). JANGAN buang vision_analyze.

## VIDEO ANALYSIS WORKFLOW FOR CRON (TERBUKTI 2026-08-10, 2026-08-12)
**Alur yg jalan untuk analisis video TikTok/YouTube di cron/background:**
1. `yt-dlp -o "C:/tmp/video.mp4" <URL>` (download)
2. `ffmpeg -ss 0 -i video.mp4 -frames:v 1 -q:v 2 frame_0.jpg` (extract 3 frame: 0s, 3s, 7s)
3. Copy frame ke `AppData/Local/hermes/cache/images/`
4. `vision_analyze` tiap frame → dapat deskripsi visual + teks overlay
5. `yt-dlp --print "%(description)s" <URL>` untuk caption (kalau tidak error rehydration)
**TESTED:** Video @marcinteodoru (Fable 5 Ultra Code) + @adityagnwann (jcode) + @github.signals (turbo-fieldfare) + 3 video @potato network → berhasil dapat isi konten.
**Detail & commands:** `references/video_analysis_pipeline.md` (di skill ziyan-agent-patterns).

## TIKTOK AUTO-POST REALITY CHECK  [TERBUKTI 2026-08-10]
- TikTok **TIDAK PUNYA public API untuk auto-post** (hanya Login Kit, Business API untuk ads, TikTok Shop).
- Cara realistis:
  - **Official Content Posting API**: butuh verified business + review process (lama, tidak pasti lolos).
  - **Unofficial**: `tiktok-uploader` (Python, browser automation via Playwright/Selenium) — rawan ban, butuh maintain cookies.
  - **Third-party**: Zapier/Make/n8n webhook ke buffer manual.
- REKOMENDASI: JANGAN janjikan auto-post TikTok tanpa approval official. Fokus ke FB/IG/X/YT yang punya API resmi.

## 9ROUTER AUTO-START & MODEL DELEGATION  [TERBUKTI 2026-08-10]
- `start-9router.bat` di Startup folder → 9Router jalan otomatis restart laptop.
- Agent Python butuh 9Router untuk caption → 9Router WAJIB hidup.
- Orkestrator pakai `nous` (tencent/hy3:free) — hanya chat diskusi, planning, delegasi.
- Sub-agent pakai **9Router** (`channel-researcher`, free) — eksekusi tugas berat (riset, coding, n8n setup, dsb).
- `delegate_task` otomatis pakai 9Router via `delegation.model=channel-researcher`.

## PYTHON VENV TROUBLESHOOTING (Windows + Python 3.13 MS Store)  [TERBUKTI 2026-08-10]
- **Fresh venv + cryptography/cffi broken `_cffi_backend`** pada Python 3.13 MS Store.
- Root cause: MS Store Python venv tidak include system binaries, cryptography 50+ butuh Rust build.
- FIX: Pin binary wheels sebelum install deps lain:
  ```bash
  .venv/Scripts/pip.exe install "cryptography==42.0.5" "cffi==1.17.1" --force-reinstall --no-deps
  ```
  Lalu install requirements.txt.
- Alternatif: `python -m venv .venv --clear --without-pip` → `ensurepip` → install.

## EVENT LOOP CONFLICT (python-telegram-bot v21+)  [TERBUKTI 2026-08-10]
- `AsyncIOScheduler` + `Application.run_polling()` conflict: "event loop already running".
- FIX: Use `BackgroundScheduler` (thread-based) + synchronous `telegram_bot.run()` calling `application.run_polling()` internally.
- Orkestrator membuat event loop sendiri untuk init async (FB/IG get IDs), lalu serahkan ke telegram bot.

## MULTI-PLATFORM POSTING (FB + IG + YT)  [TERBUKTI 2026-08-10]
- Instagram Business linked ke FB Page "Celine Aurel" → pakai **sama FB Page token** via FB Graph API.
- Endpoint IG: `/ig_user_id/media` (create container) → `/ig_user_id/media_publish` (publish).
- Video/Reels: butuh polling `status_code` sampai `FINISHED` sebelum publish.
- **YouTube Data API v3**: resumable upload via `youtube.videos().insert()` dengan `MediaFileUpload(chunksize=-1, resumable=True)`. Token: `youtube_token_celineaurel.json` (refresh via `youtube_desktop_client.json`).
- Caption Telegram: `#fb` = Facebook, `#ig` = Instagram, `#yt` = YouTube, `#both`/`#all` = FB+IG, `#ytfb` = YT+FB.
- Sheets queue: tambah kolom `platform` setelah `affiliate_link` (kolom 5: job_id, media_path, caption, affiliate_link, **platform**, status, schedule_time, created_at, posted_at, error_message, retry_count).
- Scheduler: check job['platform'] → call appropriate callback (fb, ig, yt, or combinations). Post callbacks dict: `{'facebook': fb_uploader.post_job, 'instagram': ig_uploader.post_job, 'youtube': yt_uploader.upload_video}`.
- Sub-agent delegated: sheets.py + scheduler.py updates via `delegate_task`.
- **Graceful fallback**: Jika IG Business Account tidak linked ke FB Page → `ig_uploader.get_ig_user_id()` return `""` → `ig_available=False` → agent jalan FB only, log warning. Jangan crash.
- **Multi-instance conflict**: `telegram.error.Conflict: terminated by other getUpdates request` = instance lama masih jalan. Kill semua process lama (`process(action='list')` → `process(action='kill')`) sebelum start baru.

## TELEGRAM CHANNEL ADMIN & BOT ACCESS (TERBUKTI 2026-08-15) — [CORRECTED]
- Bot di channel (bisa receive update / forward_origin logged) = membership OK. Jangan suruh Bos add/invite berulang.
- **CRITICAL 404 FACT:** raw `curl` ke Bot API return 404 (`getChat`/`sendMessage`) TAPI `python-telegram-bot` `context.bot.send_message(chat_id=..., text=...)` **WORKS** (tested live: bot replied in channel, log 200 OK). The `curl` call is the bug, NOT the channel. **Never trust `curl` 404 as proof of no access.** Post from inside the bot process (bot object), not shell curl.
- `joinChatByInviteLink` GAGAL untuk link public `t.me/username` (404). Butuh invite link `https://t.me/+XXXX` atau owner add via UI.
- `reject_if_unauthorized` default NOLAK pesan `effective_user=None` (pesan dari channel / forwarded). Bot jadi "Akses ditolak" ke reply di channel & ke forward. FIX: izinkan `chat.type == "channel"` ATAU bypass command `/distribusi` (aman, cuma Bos tau product ID).
- Ambil channel ID akurat: log `update.effective_chat.id` saat bot receive pesan → `CHAT_DEBUG type=channel id=-1004373452633`. JANGAN ketik ID manual.
- SELALU HANYA 1 instance `python.exe -m ziyan_bot.bot` (Telegram Conflict kalau 2+).
- Auto-start bot tanpa admin: Startup folder `.lnk` → `.bat` (set `PYTHONPATH=` + `GOOGLE_CREDENTIALS_FILE=client_secret.json` + jalankan venv python). Sudah terpasang `ZiyanArchiveBot.lnk`.
- Caption untuk akun AI influencer (Celine Aurel): format = [Shopee link] → [1-2 kalimat deskripsi alami TANPA HARGA] → [link lain] → [PERSIS 4 hashtag] (FINAL 16/8, ganti aturan 5 hashtag lama). Generate via 9Router.

## JANGAN LOOP VERIFIKASI (KOREKSI 2026-08-15)
- Bos: "Dari tadi sudah aku jadikan admin,, kau jangan jadi pelupa, kau punya otak kan?" → FRUSTRASSI karena agent berulang tanya/verifikasi hal sama (channel admin, ID) tanpa maju.
- FIX: kalau Bos sudah bilang "sudah X" / "kau atur lah" → ANGGAP BENAR, langsung eksekusi langkah berikutnya, JANGAN verifikasi ulang dengan pertanyaan sama. Kalau verifikasi wajib (API call), lakuin SENYAP lalu lapor hasil — bukan tanya Bos.
- Pola salah: tanya "sudah jadi admin?" → Bos bilang iya → tetap tanya lagi → Bos marah. Pola benar: cek via API sekali, kalau masih gagal → langsung tempuh jalur alternatif (forward pesan / link invite), lapor Bos 1 baris.

## ANTI-LOOP: JANGAN Ulangi API CALL GAGAL 2x (LESSON 15-Agt-2026, TELEGRAM CHANNEL)
- FAILURE YANG TERJADI: agent jalankan `curl .../sendMessage` ke channel `-1004373452633` **12x berturut-turut** (404), lalu suruh Bos add bot / invite / screenshot berulang → Bos meledak ("mutar mutar", "cari tutorialnya anjing", "bodoh").
- ROOT CAUSE: **curl 404 bukan bukti channel gak bisa diakses**. `context.bot.send_message()` (PTB library) WORKS di channel yang sama. Agent terjebak asumsi "404 = gak punya akses" dan mutar di situ.
- SELF-CRITIQUE PROTOCOL (wajib kalau error SAMA muncul 2x):
  1. STOP jalanin command yang sama. STOP suruh Bos lakuin UI step yang sama.
  2. Tanya: "Apakah parameter/tool saya SALAH, bukan sistem yang rusak?" — cek alternatif tool (bot object vs curl, library vs raw HTTP).
  3. Cek apakah ada fakta kontradiktif (bot BISA receive update dari channel tapi curl 404 → berarti akses ADA, tool yang salah).
  4. Langsung tempuh jalur alternatif / lapor Bos ringkas, jangan nebak.
- Bos: "Kau cari dulu tutorialnya anjing" = suruhan cari docs/resmi, bukan lempar ke Bos UI manual. Agent HARUS browse/docs sendiri dulu.

## Pitfalls
- Asking "mau lanjut opsi A/B/C?" → frustration. Decide.
- Loop verifikasi hal sama setelah Bos bilang "sudah" → frustration ("kau jangan jadi pelupa"). Cek sekali senyap, lalu maju.
- 4 items simultaneous → spam. Space them.
- "Telegram group can't be automated" → wrong; only 1-tap add-bot needs human.
- Anggap Telegram & Discord "sudah tahu satu sama lain" → salah. Harus bridge manual (file + cron + bot send).
- 4 items simultaneous → spam. Space them.
- "Telegram group can't be automated" → wrong; only 1-tap add-bot needs human.
- Anggap Telegram & Discord "sudah tahu satu sama lain" → salah. Harus bridge manual (file + cron + bot send).
- **Stale identifier after user correction**: kalau Bos bilang "sudah aku ganti X" (contoh: username GitHub `yangmulia96` → `ziyancorp`), STOP pakai nilai lama di semua retry. Sesi 15/8: agent mutar cari token di GitHub `yangmulia96` (404) padahal Bos sudah bilang ganti. Pakai nilai BARU seketika, jangan ulang path lama.
- **Jangan diam di tengah task panjang** (Bos: "Kok diam kau"). Kalau lagi jalanin command beruntun / menunggu user, beri 1 baris status periodic, jangan hilang total.
- **Instruksi ke Bos harus simpel** (Bos: "Ribet semua caranya"). Hindari 3-opsyen UI maze. Beri 1 langkah konkret atau otomasi sendiri.

See `references/9router_api_quirks.md` for the 9router SSE parsing gotcha that broke CS bot.
