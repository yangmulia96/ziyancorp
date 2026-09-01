---
name: ziyan-infra
description: Setup/tes sumber model AI gratis ZIYAN.
category: ziyan
---

# ZIYAN Infrastruktur AI Lokal

Orkestrator ZIYAN kelola banyak sumber model gratis agar beban tersebar & tidak kena limit. Semua di laptop Bos (Windows, home `C:\Users\arija`).

## Sumber (semua sudah terverifikasi jalan per 2026-07-31)
## 9ROUTER LOCAL JSON PARSE QUIRK (terbukti 2026-08-08)
- Endpoint lokal `http://127.0.0.1:20128/v1/chat/completions` balikin respons dengan **leading whitespace/newline di awal** + suffix `data: [DONE]` di akhir (bukan JSON murni).
- `json.load()` LANGSUNG GAGAL: `Extra data: line X column Y (char Z)`.
- **FIX wajib di semua script Python yang panggil 9router langsung**:
  ```python
  raw = urllib.request.urlopen(req, timeout=25).read().decode().strip()
  s = raw.find("{")      # cari kurung JSON pertama
  e = raw.rfind("}")     # kurung terakhir
  r = json.loads(raw[s:e+1])
  content = r["choices"][0]["message"]["content"].strip()
  ```
- JANGAN `json.load(raw)` utuh. Pattern ini sudah dipakai di `ziyan_corp_cs_bot.py` (CS bot Telegram).
- Base URL benar untuk script lokal = `http://127.0.0.1:20128/v1` (bukan `https://9router.noes.chat` yang gak resolve di host ini).

## GITHUB PAGES USER-SITE DEPLOY (terbukti 2026-08-08)
- **User site** = repo bernama `<username>.github.io` → live di `https://<username>.github.io/` (root, base `/`).
- **Project site** = repo biasa → live di `https://<username>.github.io/<repo>/` (base `/<repo>/`).
- **Ganti username GitHub** → semua URL project-site ikut berubah (`yangmulia96.github.io/ziyancorp` → `ziyancorp.github.io/ziyancorp`), yang lama jadi 404.
- **Vite base path**: `vite.config.js` → `base: '/'` untuk user-site, `base: '/ziyancorp/'` untuk project-site. Salah base = asset 404 → blank white page.
- Deploy: `npm run build` → copy `dist/*` ke clone repo pages → `git add -A && git commit && git push`.
- `gh` CLI sudah login sebagai `yangmulia96` (redirect otomatis ke `ziyancorp` setelah rename — normal).
- Buat user-site repo: `gh repo create ziyancorp.github.io --public`.

## 9ROUTER: CARA JALAN & WATCHDOG
- **CARA BENAR**: `9router --tray --no-browser` (system tray daemon, STABIL). JANGAN `9router` polos → langsung exit sendiri (bukan daemon).
- **WATCHDOG (0 token)**: cronjob script-only jalan `ziyan_watchdog_9router.sh` (di `~/.hermes/scripts/`, `no_agent=true`) tiap 5 mnt: cek `curl 127.0.0.1:20128/v1/models` → kalau mati `taskkill /F /IM 9router.exe` lalu `start "" 9router --tray --no-browser`. Bos protes watchdog agent-based boros token → SELALU pakai script-only untuk cron berulang.
- **MANDAT AGENT-ONLY**: Bos mau agent selesaikan SEMUA tanpa langkah manual Bos. Kalau tool butuh login Bos (mis. NotebookLM), cari jalur agent-only (computer_use+9router, n8n, OpenCut) atau katakan JUJUR + beri opsi. JANGAN asumsikan "wajib Bos yg lakukan".
- Sub-agent WAJIB pakai 9router untuk TTS/image (Gemini/OpenRouter) via `curl http://127.0.0.1:20128/v1/...` dengan header `Authorization: Bearer $HERMES_CUSTOM_9ROUTER_API_KEY`.
   - Endpoint: `/v1/models` (chat), `/v1/models/tts`, `/v1/models/stt`, `/v1/models/image`, `/v1/models/embedding`, `/v1/models/web` (search/fetch, bisa kosong).
   - Skill capability sudah terpasang di `AppData\Roaming\hermes\skills\9router*` (chat, image, video, tts, stt, embeddings, web-search, web-fetch).
2. **Gemini** — key Bos di `C:\Users\arija\ziyan_keys.env` (`GEMINI_KEY=`), loader `.bashrc` -> `$GEMINI_KEY`. Tes: `bash test_gemini.sh`.
3. **Antigravity** (Google) — IDE coding agent, tier Individual $0. Terinstall `AppData\Local\Programs\antigravity\Antigravity.exe`. OAuth connected: Gemini, OpenRouter, Kimi, Kiro. Buka & login Google (jangan saya yang ketik password).
4. **NotebookLM** — video overview HANYA lewat browser login (computer_use Brave Bos). Tidak ada API publik.
   - **PITFALL (2026-08-02)**: computer_use TIDAK bisa detect window Brave di laptop ini (cua-driver `list_windows` tidak munculkan Brave, `capture app=Brave` gagal match). Launch via `start`/`cmd /c start` juga crash silent. Solusi: BOS yang buka Brave manual (klik 2x icon), login, generate → taruh file di `OneDrive/ziyan_pending/` → agent ambil & upload. JANGAN habiskan waktu coba computer_use buka Brave.

## 9router model FREE yang LANGSUNG JALAN (rotasi)
**STATUS 2026-08-10 (terverifikasi via curl langsung)**:
- ✅ MASIH JALAN: `kgw/nvidia/nemotron-3-ultra-550b-a55b:free` (KGW/Kilo Gateway), `kgw/kilo-auto/free`, `kilo-gateway/kilo-auto/free`, `openrouter/nvidia/nemotron-3-ultra-550b-a55b:free`.
- ❌ MATI/ERROR: `openrouter/deepseek/deepseek-r1:free` (jadi **PAID** 404 `unavailable for free`), `groq/*` (API key invalid di .env), `cf/@cf/*` (Cloudflare key expired/auth error), `gemini/*` & `antigravity/*` (429 quota habis), `kimi/*` (402 membership), `vertex` (401 API key not supported), `nvidia/*` via OpenRouter sering 32/32 worker limit.
- Cadangan: `kr/claude-sonnet-4.5`, `kr/claude-opus-4.7` (lewat Kilo, bukan cloud — gratis kalau kuota ada).
- **PITFALL rotasi OpenRouter**: model `:free` di OpenRouter sering di-mutasi jadi paid (deepseek-r1:free → paid 2026-08-10). Selalu tes `:free` sebelum masuk combo.
- Procedure diagnosis + repair combo via SQLite: `references/9router_diagnostic.md`.

## 9ROUTER $0 HARDENING (terbukti 2026-08-09 — penyebab saldo OpenRouter kepotong $0.11)
- **AKAR MASALAH**: Combo 9Router (DB `C:\Users\arija\AppData\Roaming\9router\db\data.sqlite`, table `combos`, kolom `models` = JSON array) awalnya campur **125 model BERBAYAR** + `:free`. Kalau model `:free` gagal/limit, 9Router **fallback ke berbayar** → tembus OpenRouter cloud (key `sk-or-...` di `providerConnections`) → saldo kepotong.
- **FIX combo jadi 100% :free** (script Python, jalan di laptop):
  ```python
  import sqlite3, json
  db='C:/Users/arija/AppData/Roaming/9router/db/data.sqlite'
  c=sqlite3.connect(db); cur=c.cursor()
  cur.execute('SELECT id, models FROM combos')
  for rid, m in cur.fetchall():
      models=json.loads(m)
      only_free=[x for x in models if ':free' in x]   # filter gratis
      if not only_free: only_free=DEFAULT_FREE_LIST   # isi kalau kosong
      cur.execute('UPDATE combos SET models=? WHERE id=?', (json.dumps(only_free), rid))
  c.commit(); c.close()
  ```
  Lalu **restart 9Router** biar DB dibaca ulang (lihat bawah).
- **CARA RESTART 9ROUTER LEWAT TERMINAL** (bukan `node 9router` — itu gagal karena 9router adalah BASH SCRIPT, bukan node app):
  ```bash
  PID=$(netstat -ano 2>/dev/null | grep ":20128" | head -1 | awk '{print $5}')
  [ -n "$PID" ] && taskkill /F /PID $PID
  bash "C:/Users/arija/AppData/Roaming/npm/9router" --tray --no-browser
  ```
  Jangan pakai `cmd /c start` (timeout di background bash). Tunggu ~14 dtk, cek `curl 127.0.0.1:20128/v1/models`.
- **MODEL GRATIS TERBANYAK per provider** (dari 123 model, 120 GRATIS): `kr/` (Kilo) = 44, `ag/`=13, `cf/`=13, `openrouter/:free`=11, `kimi`=10, `nvidia`=8. **CUMA 3 BERBAYAR**: `openrouter/google/lyria-3-pro-preview`, `lyria-3-clip-preview`, `openrouter/openrouter/free` (music/aneh). `kr/claude-*` TIDAK berbayar (lewat Kilo, bukan OpenRouter cloud).
- **Paling pintar gratis** (urutan combo): `ag/claude-opus-4-6-thinking` → `kr/gpt-5.6-terra` → `kr/claude-sonnet-5`/`4.5` → `gc/gemini-3-pro-preview` → `kr/deepseek-3.2` → `openrouter/nvidia/nemotron-3-ultra-550b-a55b:free`.

## 9ROUTER DIAGNOSTIC & COMBO REPAIR (terbukti 2026-08-10)
Ketika dashboard `Usage & Analytics` (browser `http://localhost:20128`) node provider MERAH / routing error, jangan asumsi "auto-switch gagal". Diagnosis DB dulu:
```bash
DB="$APPDATA/9router/db/data.sqlite"
sqlite3 "$DB" "SELECT provider, testStatus, errorCode, backoffLevel, substr(lastError,1,90) FROM providerConnections;"
sqlite3 "$DB" "SELECT models FROM combos WHERE name='channel-researcher';"
```
**Penyebab umum 'error' di dashboard**:
- Provider kena `429`/`402`/`401` = kuota/akun gratis habis atau salah auth → BUKAN bug routing.
- `backoffLevel>0` = provider di-lock sementara (exponential backoff) → nunggu timer.
- Model `:free` OpenRouter jadi paid → 404 `unavailable for free`.

**FIX procedure** (backup dulu!):
```bash
cp "$DB" "$DB.bak_diag_$(date +%Y%m%d_%H%M%S)"
sqlite3 "$DB" "UPDATE providerConnections SET isActive=0 WHERE provider IN ('antigravity','gemini','kimi','nvidia','vertex');"
sqlite3 "$DB" "UPDATE combos SET models='[\"kgw/nvidia/nemotron-3-ultra-550b-a55b:free\",\"kgw/kilo-auto/free\",\"kilo-gateway/kilo-auto/free\",\"openrouter/nvidia/nemotron-3-ultra-550b-a55b:free\",\"kr/claude-sonnet-4.5\",\"kr/claude-opus-4.7\",\"kr/deepseek-3.2\"]', updatedAt='$(date -u +%Y-%m-%dT%H:%M:%S.000Z)' WHERE name='channel-researcher';"
```
**Verifikasi** (JSON 9Router ada whitespace + suffix `data: [DONE]` — pakai grep):
```bash
curl -s http://localhost:20128/v1/chat/completions -H "Authorization: Bearer $KEY" \
  -d '{"model":"channel-researcher","messages":[{"role":"user","content":"ibu kota Indonesia?"}],"max_tokens":20}' \
  | tr '\r' '\n' | grep '^{' | tail -1 | python3 -c "import sys,json;d=json.load(sys.stdin);print(d['choices'][0]['message']['content'] if 'choices' in d else d)"
```
Detail + daftar model live: `references/9router_diagnostic.md`.

## AUTO-FALLBACK & DELEGATION PITFALL (krusial $0)
- **Request `model:"channel-researcher"` (NAMA COMBO) → 9Router round-robin auto-fallback antar :free kalau 1 model limit/429.** Request model SPESIFIK (mis. `nemotron-3-ultra...free`) → TIDAK auto-fallback, gagal kalau model itu limit. Jadi bot/sub-agent HARUS request nama combo, bukan model spesifik.
- **PITFALL `delegation.model: openrouter` (BARE) = BOCOR KE CLOUD BERBAYAR**: 9Router TIDAK punya route `openrouter` (error "No active credentials for provider: openai") → Hermes fallback ke OpenRouter cloud langsung pakai key `sk-or-...` → SALDO KEPOTONG. **WAJIB** `delegation.model: channel-researcher` (atau model `:free` eksplisit). Set via `hermes config set delegation.model channel-researcher` (agent TIDAK bisa edit config.yaml langsung — refused sebagai security-sensitive).
- **Verifikasi $0**: request model `:free` → cek `usage.cost == 0` di response. Kalau `cost:0` = aman. Model `:free` bisa kena rate-limit harian (mis. Nvidia 32/32) → itu quota, BUKAN saldo; 9Router fallback ke :free lain.
- **BOT CLIPPER**: `sonnet()` di `clip_test/bot.py` pakai `model:"channel-researcher"` (bukan nemotron spesifik) → auto-fallback pintar gratis.

## MODEL `gc/*` (DITAMBAHKAN DARI GEMINI-CLI) — PERLU GOOGLE AI STUDIO KEY
- Bos pernah tambah model `gc/*` (mis. `gc/gemini-2.5-flash`, `gc/gemini-3-pro-preview`) lewat gemini-cli ke 9Router Proxy dashboard.
- **TES 2026-08-07**: `gc/gemini-2.5-flash` balas **403** ("HTTP 403 reset after 2m") karena **belum ada Google AI Studio API key** di konfigurasi 9Router untuk channel itu.
- **FIX kalau Bos mau pakai**: masukkan `GEMINI_API_KEY` (GRATIS dari aistudio.google.com, batas 50 req/hari untuk 2.5-flash) ke 9Router → `gc/*` jadi gratis.
- **JANGAN salah kaprah**: `ag/*` (Antigravity) SUDAH GRATIS & jalan tanpa key tambahan — itu jalur utama. `gc/*` cuma alternatif kalau Bos sudah pasang key Studio. Bedakan saat Bos tanya "model dari gemini-cli gratis?" → jawab: `ag/*` gratis, `gc/*` butuh key Studio (belum terpasang → 403).
- Cek daftar: `curl 127.0.0.1:20128/v1/models` → filter `gemini`/`ag/`/`gc/`.

## FIX VISION 404 (HERMES vision_analyze) — TERBUKTI 2026-08-11
- **Gejala**: `vision_analyze` error 404 atau model provider failed. Penyebab: `auxiliary.vision.provider: custom` dengan model `kr/claude-sonnet-4.5` (paid/rate limited).
- **FIX**: Ganti ke model gratis via 9Router: `gemini/gemini-3.6-flash` (atau `ag/gemini-3.6-flash-medium`).
- **Config yang JALAN** (`config.yaml` → `auxiliary.vision`):
  ```yaml
  auxiliary:
    vision:
      provider: custom
      model: gemini/gemini-3.6-flash
      base_url: http://127.0.0.1:20128/v1
      api_key: ${HERMES_CUSTOM_9ROUTER_API_KEY}
      key_env: ''
  ```
- **Apply**: `hermes config set auxiliary.vision.model gemini/gemini-3.6-flash` → restart Hermes Desktop App (bukan cuma gateway).
- **Verifikasi**: `hermes send -t discord:... "test"` → response normal, tidak ada "model provider failed".

## ARSITEKTUR TOKEN ZIYAN (KEPUTUSAN FINAL 2026-08-02)
- **Parent (Orkestrator/CEO) = Nous `tencent/hy3:free` dengan TOKEN KHUSUS** — TIDAK di-share ke sub-agent.
- **Sub-agent (karyawan/divisi) = 9router combo 'Gratis-Selamanya'** — token gratis ALL LLM di 9router (BUKAN token nous). Delegation model = `channel-researcher` (auto-router, lihat bawah).
- **Config yang BENAR** (`config.yaml`):
  ```yaml
  provider: nous
  model: tencent/hy3:free
  delegation:
    model: channel-researcher
    provider: 9router
  ```
  (Agent TIDAK bisa tulis config.yaml — edit manual via `hermes config set` atau Notepad, lalu RESTART Hermes Desktop App.)
- **PITFALL SPoF (KOREKSI BOS 2026-08-02)**: JANGAN pindah parent ke 9router. Awal sesi sempat disarankan `provider: 9router` (karena throttle nous), tapi Bos TOLAK TEGAS: kalau 9router mati, parent + karyawan sama-sama mati → perusahaan lumpuh. Parent di nous = isolasi risiko. Sub-agent mewarisi model parent saat spawn, jadi parent di nous + delegation di 9router = aman.
- **Setelah ubah provider/model**: RESTART HERMES DESKTOP APP (bukan cuma gateway).

## CHANNEL-RESEARCHER (AUTO-ROUTER 9ROUTER — STANDAR DELEGATION SUB-AGENT)
- `channel-researcher` = alias abstrak di 9router, BUKAN model fisik. Saat dipanggil, 9router otomatis merutekan ke model terbaik di pool 'Gratis-Selamanya'.
- **Bukti**: request riset "IonQ SkyWater" → backend `nvidia/nemotron-nano-12b-v2-vl:free`, `is_byok:false` (pakai token 9router, bukan nous).
- **Keuntungan**: auto-fallback kalau 1 model 429/402, zero-config sub-agent, gratis. Tidak perlu whitelist manual gemma/laguna.
- **Pakai untuk**: delegation model semua sub-agent ZIYAN (RISA/NOVA/FAZA/PANDA).
- **Verifikasi**: `curl 127.0.0.1:20128/v1/chat/completions -H "Authorization: Bearer $HERMES_CUSTOM_9ROUTER_API_KEY" -d '{"model":"channel-researcher","messages":[{"role":"user","content":"Cari fakta IonQ"}]}'` → 200 + konten.
- **Catatan**: ping "Halo" bisa return whitespace kosong, tapi prompt nyata menghasilkan teks (test: fakta IonQ Bahasa Indonesia, 100 token OK).

## SEJARAH: INSIDEN THROTTLE NOUS (2026-08-02 — SUDAH REVERT KE NOUS)
- Insiden: provider utama `nous` (tencent/hy3:free) sempat di-throttle → bot Discord `#hq` nyangkut loop `⏰ rate-limiting`, gateway crash. Sempat disarankan failover ke 9router, TAPI Bos putuskan parent TETAP nous (token khusus) untuk hindari SPoF. Sub-agent tetap di 9router `channel-researcher`.

## RESTART HERMES (urutan benar)
1. `hermes gateway restart` → restart gateway (baca config.yaml baru, TAPI tidak reload .env ke app).
2. **Tutup penuh Hermes Desktop** (klik kanan tray → Quit, atau Task Manager End Task) → buka lagi dari Start Menu. Ini yang bikin `.env` kebaca session chat.
- Cek: `hermes gateway status` → "gateway process running". 9router: `curl $NINEROUTER_URL/api/health` → 200.

## MATIKAN DELL BLOATWARE (PENYEBAB KIPAS BERISIK)
- Service auto-start yg bikin panas: `DDVCollectorSvcApi`, `DDVDataCollector`, `DDVRulesProcessor`, `DellClientManagementService`, `SupportAssistAgent`, `Dell Digital Delivery Services`, `Dell SupportAssist Remediation`. Ini telemetry Dell, BUKAN file sistem → aman dimatikan.
- **Terminal agent TIDAK punya admin** → `sc config` / `Set-Service` gagal `Access Denied (5)`. Bos harus jalankan `.bat` as **Administrator**.
- File `.bat`: `C:\Users\arija\disable_dell_services.bat` (loop `sc config <svc> start= demand` + `sc stop <svc>`). Bos: right-click → Run as Admin → restart laptop.
- **JANGAN matikan**: `Dell Hardware Support` (driver keyboard/battery), `SecurityHealth` (Defender), `RtkAudUService`/`WavesSvc` (audio).
- Startup folder bersihkan via Task Manager → Startup apps (disable Copilot/Chrome/Edge/OneDrive/TelegramBot). Sudah dilakukan: sisakan `Hermes.lnk`, `9router_startup.bat`, `ZIYAN_9router.bat`.

## PROTOKOL KEAMANAN KEY (PENTING)
- **JANGAN** eksekusi perintah berisi literal API key (Bos pernah leak Gemini key ke chat → suruh revoke di aistudio.google.com/apikey).
- Key simpan di `ziyan_keys.env`, skrip baca `$VAR` (key tidak pernah saya lihat/ketik).
- **TRAP CRLF**: `.env` Windows pakai CRLF → bash membaca key ikut `\r` → Google tolak `API_KEY_INVALID`. Selalu strip: `KEY=$(printf '%s' "$GEMINI_KEY" | tr -d '\r' | tr -d '\n' | xargs)`.
- Shortcut edit key: `C:\Users\arija\OneDrive\Desktop\ZIYAN_Keys.lnk` (buka Notepad -> ziyan_keys.env).

## Alur umum (delegate ke sub-agent untuk hemat token)
- Tes fitur 9router (TTS/STT/image/embeddings) → delegate_task leaf, simpan ke disk, JANGAN kirim file ke chat kecuali Bos minta.
- Generate video NotebookLM → computer_use Brave (Bos login). Klik Video Overview → format → Generate → tunggu >30 mnt → klik Download (dialog Save As, arahkan ke `C:\Users\arija\`).
- Video Jalur B gratis (tanpa NotebookLM) → sub-agent: edge-tts/9router-tts + Pillow bg + ffmpeg. Hasil statis (bukan animasi).

## Verifikasi
- `curl $NINEROUTER_URL/api/health` → `{"ok":true}`
- `curl $NINEROUTER_URL/v1/models` → daftar chat
- Jangan pernah claim "selesai" sebelum cek state/file sungguhan.

## HIGGSFIELD CLI (berbayar - agregator model komersial)
- **Install fix Windows**: `npm i -g @higgsfield/cli` GAGAL di postinstall (path backslash corrupt ke tar). Fix: `--ignore-scripts` lalu manual download tarball dari GitHub Releases + `tar -xzf`. Detail: `references/free_image_pipeline.md`.
- **Skills companion**: `npx skills add higgsfield-ai/skills --yes` (LOKAL, tanpa `--global` — PromptScript tolak global). Tersimpan `~/.agents/skills/higgsfield-*`.
- **Auth**: `higgsfield auth login` buka browser; per 2026-08-07 GAGAL server-side: "The requested scope is invalid ... 'user:org:read'" (bug Clerk Higgsfield). Tunggu fix mereka sebelum pakai. CLI sendiri jalan (`higgsfield --version` -> 1.1.20).
- Status: berbayar (credit), bukan opsi gratis ZIYAN.

## Pitfalls
- `find /` di git-bash Windows = hang 60s (timeout). Pakai `search_files` atau path langsung.
- PowerShell `$ws.CreateShortcut` path Desktop HARUS `C:\Users\arija\OneDrive\Desktop` (bukan `C:\Users\arija\Desktop`).
- Web search/fetch 9router bisa kosong di proxy ini — pakai tools sendiri (browser/terminal) sebagai ganti.

## MODEL 9ROUTER YANG KONFIRMASI JALAN (tes 2026-08-01)
- **TTS Indonesia**: `edge-tts/id-ID-ArdiNeural` (HTTP 200, MP3 valid). `openrouter/*-tts` & `gemini/*-tts` DI proxy ini rusak (502 / key invalid) → jangan pakai.
- **Image GRATIS & JALAN (default 2026-08-07)**: `cf/@cf/black-forest-labs/flux-2-dev` (Cloudflare Workers AI, 200, return JPEG base64 ~248KB). Alternatif: `flux-2-klein-4b`, `flux-1-schnell`, `leonardo/phoenix-1.0`, `stabilityai/stable-diffusion-xl-base-1.0`. ✅ PAKAI Flux sebagai jalur gratis utama — terbukti via `ziyan_tools/genimg_free.py`.
- **Image (Nano Banana 2)**: `ag/gemini-3.1-flash-image` (HTTP 200, base64 ~560KB PNG). Setara Google Flow, gratis lewat proxy Antigravity. Pakai kalau butuh gaya Nano Banana.
- **Image (MATI)**: channel `gemini/*-image` (mis. `gemini/gemini-2.5-flash-image`, `gemini/gemini-3.1-flash-image-preview`) → 429 "quota exceeded" (free tier limit=0) → JANGAN pakai `gemini/` untuk image. `GEMINI_KEY` Bos juga quota=0.
- **Script reusable**: `C:\Users\arija\ziyan_tools\genimg_free.py` — generate gambar gratis via 9router (default Flux). Detail + recipe Higgsfield CLI: `references/free_image_pipeline.md`.
- **Auth wajib**: 9router kini butuh header `Authorization: Bearer $HERMES_CUSTOM_9ROUTER_API_KEY`. Tanpa header → 401 Unauthorized (dulu pernah jalan tanpa key). Script Python HARUS set header ini.
- Endpoint TTS: `POST $NINEROUTER_URL/v1/audio/speech`. Endpoint image: `POST $NINEROUTER_URL/v1/images/generations`.
- Script bulk image gratis ZIYAN: `C:\Users\arija\gen_img.py` (baca prompt, loop via ag/, simpan ke `ziyan_generated/`).
- Hasil tes tersimpan: `C:\Users\arija\test_tts.mp3`, `C:\Users\arija\test_img.png`, `C:\Users\arija\ziyan_generated\athlete_fictional_01.png`.

## NVIDIA NIM DIRECT API — MODEL YANG TERSEDIA vs YANG SUDAH ADA DI 9ROUTER
- **API key NVIDIA `nvapi-...` bisa valid untuk listing model** (`/v1/models` → 200 OK, ~87 model), **TAPI inference via `/v1/chat/completions` return 404** untuk akun/tier ini. Artinya model tidak bisa dijalankan langsung dari Hermes via provider `nvidia-nim` walaupun config sudah benar.
- **Implicasi**: jangan tambah provider `nvidia-nim` langsung ke Hermes `config.yaml` untuk inference. Model-model NVIDIA yang dibutuhkan ZIYAN sudah tercakup via 9router/OpenRouter.
- **Model tambahan dari NVIDIA NIM yang BELUM ada di 9router** (per 2026-08-13): `nemotron-3.5-lightning-30b-a3b` (agentic), `riva-translate-4b-instruct-v2` (translation 37 bahasa), `nemotron-3-embed-1b` (embedding RAG), `inkling` (multimodal MoE). Untuk saat ini **tidak bisa dipakai** karena endpoint inference 404.
- **Downloadable**: abaikan untuk laptop 8GB RAM kecuali model <7B.
- **Daftar model lengkap + status endpoint**: lihat `references/nvidia_nim_catalog_2026-08-13.md`.
- **FACT VALIDATION RULE**: Jika NVIDIA inference masih 404, jangan revisi config Hermes lagi. Endpoint ini masih ditutup untuk akun ini. Pakai 9router/OpenRouter sebagai gantinya.

## HERMES DESKTOP THEMING
- Hermes Desktop punya sistem tema built-in + slash command `/skin` untuk pilih tema.
- Marketplace themes bisa diinstall, termasuk tema gelap/futuristik.
- **Tidak ada preset "Jarvis" secara native** — gaya futuristik bisa dicapai dengan custom tema gelap + aksen neon.
- Requirements: Hermes Desktop app (`hermes desktop`), bukan CLI-only.

## WINDOWS 11 → MACOS 27 UI (video @unknown.tech)
- Tools: **Windhawk + Rainmeter** (2 aplikasi gratis, tanpa coding).
- **Tidak cocok untuk laptop 8GB RAM**: Rainmeter + banyak skin bisa makan +300-600MB RAM.
- Rekomendasi: test dengan skin minimal dulu, monitor via Task Manager. Jika baseline >70% RAM, gunakan Windhawk saja (tanpa Rainmeter).

## GOOGLE FLOW / LABS / NANO BANANA (status 2026-08-01)
- **Google Flow** (flow.google): web UI berbayar (butuh langganan Google AI Pro/Ultra). TIDAK ada API publik → agent cuma bisa akses via `computer_use` Brave (boros token, butuh login Bos). Model "Nano Banana 2" di Flow = `ag/gemini-3.1-flash-image` di 9router (hasil setara, GRATIS, tanpa langganan).
- **Google Labs**: sebagian web UI (NotebookLM, Stitch, dll), NotebookLM Enterprise ada API (butuh GCP billing). Sisanya browser automation.
- **Gemini Omni Flash**: model VIDEO preview (`gemini-omni-flash-preview`), bukan teks. Tidak ada di 9router.
- **Nano Banana**: NB1=`gemini-2.5-flash-image`, NB2=`gemini-3.1-flash-image` (ada di /v1/models/image 9router), NB Pro=`gemini-3-pro-image`. Untuk ZIYAN pakai `ag/gemini-3.1-flash-image` (gratis lewat proxy).
- Riset lengkap: `C:\Users\arija\ziyan_riset_google_tools.md`.
- ETIS: JANGAN generate gambar "facial identity lock" ke foto referensi orang nyata (risiko deepfake/non-consensual). Pakai karakter fiksi.

## ORGANISASI CREDENTIAL & KEY
- **`C:\Users\arija\ziyan_keys.env`** = tempat API key eksternal (GEMINI_KEY, OPENAI_KEY, ELEVENLABS_KEY, GOOGLE_KEY, YOUTUBE_KEY, GITHUB_TOKEN). Loader `.bashrc` → `$VAR`. Shortcut edit: `OneDrive\Desktop\ZIYAN_Keys.lnk`.
- **`C:\Users\arija\ziyan_credentials\`** = OAuth client_secret JSON (mis. `google_client_secret.json`, project `lofty-layout-504106-n4` milik Bos). PISAHKAN dari `ziyan_keys.env` (beda format, bukan env var).
- YouTube upload butuh **Desktop/Installed OAuth client** (bukan Web). Web client TOLAK `urn:ietf:wg:oauth:2.0:oob` ("must contain a domain"). File benar: `ziyan_credentials/youtube_desktop_client.json` (project `lofty-layout-504106-n4`, redirect `http://localhost`). Detail: skill `ziyan-youtube` → references/youtube_oauth.md.
- JANGAN kirim key/credential ke chat Discord (insiden leak Gemini key). Bos isi lewat shortcut desktop di laptop, atau simpan ke OneDrive lalu buka di laptop.

## GITHUB SETUP (status 2026-08-01)
- `gh auth status` → **belum login** (tidak ada token). `git config --global` pakai user `Yang Mulia` / `arizalkempo@gmail.com` (bukan `mziyan266`).
- FIX agar bisa clone/push: Bos generate **GitHub PAT** (read/write) → simpan ke `ziyan_keys.env` baris `GITHUB_TOKEN=***` (JANGAN ke chat). Lalu `gh auth login --with-token` atau `git clone https://$GITHUB_TOKEN@github.com/...`.
- Skill open-source menarik buat ZIYAN: `TomGranot/watch-video` (agent paham video lokal/URL), `TencentEdgeOne/multimodal-file-assistant-agent` (proses PDF/Word/Excel/gambar/video).

## TEKNIK BACA LINK SHARE GEMINI
- `web_extract` tool TIDAK tersedia. `curl` ke share link sering diblokir parser.
- CARA JALAN: `browser_navigate` ke `https://share.gemini.google/...` → auto-redirect ke `gemini.google.com/share/...` → `browser_snapshot(full=true)` → isi chat ada di element `heading "You said"` + `StaticText`. (Bukti: sesi ini berhasil baca chat "AI Agent Lamaran Kerja".)

## REFERENSI ARSITEKTUR VIDEO
- **OpenMontage = GAGAL & DIHAPUS (pelajaran pahit 2026-08-02)**. Dicoba generate 1 video butuh 27 mnt, API imagen 404, Gemini image 429, Google TTS 401 (butuh GCP project), video_gen berbayar tidak ada → hasil cuma image stills (bukan video AI). TIDAK EFISIEN. JANGAN pakai lagi.
- **NotebookLM TIDAK ADA API** → agent TIDAK bisa generate video darinya. Bos pernah mau generate manual, lalu putus: "agent yang selesaikan semua". Jalur agent-only buat video: (a) `n8n`+API berbayar (ElevenLabs/Suno/FAL) = kualitas tinggi tapi butuh biaya, (b) computer_use+9router (TTS image/audio gratis) untuk render lokal, (c) OpenCut (open-source CapCut alt, 80K★) sedang dipertimbangkan sebagai editor gratis.
- **n8n untuk TEMPLATE (jalur cuan utama, bukan konten)**. Riset: uang terbesar = JASA (workflow $150-2000/proyek, retainer $200-1500/klien/bln), BUKAN konten. 3 draf template ZIYAN di `ziyan_n8n_templates/` (wa_cs_umkm $39, leadgen_maps $49, faceless_engine $59-99). Jual via Gumroad + n8n.io (lite gratis) + X/Twitter + grup WA/Telegram ID.
- **INSTALL n8n**: `npm install n8n` di folder KOSONG (mis. `n8n_server/`), JANGAN di `~`/`C:\Users\arija` yang punya `package.json` → shell bocor baca JSON sebagai command (`OAuth: command not found`) & npx gagal. Jalankan `npx n8n` (port 5678) di folder itu. Docker tdk terinstall di laptop ini.
- **Riset keyword**: pakai `pytrends` (venv uv, jangan global py3.14 — urllib3 v2 error). Rate-limit Google Trends agresif → max 8-10 seed/sesi, jeda 20-30 dtk. Nich ZIYAN tolak topik geek ("71 free AI models"), mau demand tren nyata (cuan/side hustle/passive income).
- **YouTube policy**: Jan 2026 YPP cabut 16 channel via Inauthentic Content Policy (overposting/template/slideshow statis). Wajib: Judge agent (quality gate), upload random (bukan serentak), publish Private→flip, disclosure sintetis. Ukur like-rate/retention bukan jumlah video.
- Detail OpenMontage (arsip): `references/openmontage.md`.
