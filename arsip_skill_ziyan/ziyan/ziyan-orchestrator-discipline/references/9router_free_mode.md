# 9Router → $0 Mode (Free Tier Lockdown) — VERIFIED 2026-08-09

Bos marah saldo OpenRouter kepotong ($0.11, 279M token, 5K req). Root cause: 9Router
lokal proxy punya `providerConnections` ke OpenRouter cloud (key `sk-or-...` di LIVE config),
dan combo isinya campur model BERBAYAR → fallback nembus OpenRouter berbayar.

## FAKTA PENTING (koreksi dari klaim salah "cuma openrouter yg gratis")
Dari 123 model di 9Router Bos:
- **120 model GRATIS**, cuma **3 model BERBAYAR** (semua `openrouter/*` tanpa `:free`):
  - `openrouter/google/lyria-3-pro-preview` (music gen)
  - `openrouter/google/lyria-3-clip-preview` (music gen)
  - `openrouter/openrouter/free` (aneh, terdeteksi berbayar)
- Provider `kr/` (Kilo), `kgw/` (kwaipilot), `ag/` (Antigravity), `cf/`, `gemini/`,
  `groq/`, `kimi/`, `nvidia/`, `vx/`, `gc/` = **SEMUA GRATIS** (gateway Bos sendiri,
  TIDAK tembus OpenRouter cloud). `kr/claude-haiku-4.5` AMAN gratis — jangan takut pakai.
- OpenRouter `:free` (11 model, mis. `nemotron-3-ultra-550b-a55b:free`) = gratis + quota harian.

## LIVE CONFIG = SQLite (bukan JSON backup)
- Backup `9router-backup-*.json` = HANYA snapshot (baca saja, jangan edit sbg sumber).
- Config nyata: `C:\Users\arija\AppData\Roaming\9router\db\data.sqlite`
- Table `combos`, kolom `models` = JSON array of model-ID strings.
- Table `providerConnections` = daftar provider + key (JANGAN hapus openrouter di sini,
  cukup filter model di combo).

## RECIPE: 1 combo isinya SEMUA model gratis, openrouter :free paling atas
```python
import sqlite3, json
db = r'C:\Users\arija\AppData\Roaming\9router\db\data.sqlite'
c = sqlite3.connect(db); cur = c.cursor()
# Ambil daftar model gratis dari endpoint /v1/models (curl 127.0.0.1:20128)
# free = semua model KECUALI openrouter/* tanpa :free
free = [m for m in all_models if not (m.startswith('openrouter/') and ':free' not in m)]
# Pindahkan nemotron :free ke posisi 1 (prioritas utama)
target = 'openrouter/nvidia/nemotron-3-ultra-550b-a55b:free'
free = [x for x in free if x != target]; free.insert(0, target)
cur.execute('SELECT id FROM combos'); ids = [r[0] for r in cur.fetchall()]
main = ids[0]
cur.execute('UPDATE combos SET models=? WHERE id=?', (json.dumps(free), main))
for i in ids[1:]:
    cur.execute('DELETE FROM combos WHERE id=?', (i,))
c.commit(); c.close()
```

## CARA JALANKAN 9ROUTER (kritikal — jangan salah)
- `9router` adalah **BASH SCRIPT**, BUKAN node app. `node "C:/.../npm/9router"` GAGAL
  (SyntaxError `basedir=$(dirname...)`).
- **BENAR**: `bash "C:/Users/arija/AppData/Roaming/npm/9router" --tray --no-browser`
  (jalankan di background terminal, BUKAN foreground `node`). TERBUKTI jalan (PID listen 20128).
- Setelah edit DB: KILL PID di port 20128 lalu launch ulang via bash di atas.

## VERIFIKASI $0
```bash
curl -s -m 25 http://127.0.0.1:20128/v1/chat/completions \
  -H "Authorization: Bearer $HERMES_CUSTOM_9ROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"openrouter/nvidia/nemotron-3-ultra-550b-a55b:free","messages":[{"role":"user","content":"hai"}],"max_tokens":10}'
# cari "cost":0 di JSON -> gratis. Juga cek "provider":"Nvidia" (bukan OpenRouter cloud)
```

## AUTO-FALLBACK (round-robin antar :free) — WAJIB untuk bot & sub-agent
Request model **spesifik** (mis. `nemotron-3-ultra-550b-a55b:free`) GAGAL auto-switch kalau
model itu kena rate-limit (429/ResourceExhausted). Request **nama combo** → 9Router coba
model satu-satu sampai dapat yang jalan.
- Nama combo default di DB: `channel-researcher` (cek: `SELECT name FROM combos`).
- **BOT CLIPPER & SUB-AGENT HARUS pakai `"model": "channel-researcher"`**, BUKAN model spesifik.
- Urutan di kolom `models` = prioritas (pintar → ringan). Bos set:
  `ag/claude-opus-4-6-thinking` (top) → `kr/gpt-5.6-terra` → `kr/claude-sonnet-5`
  → `gc/gemini-3-pro-preview` → `kr/deepseek-3.2` → `openrouter/nvidia/nemotron-3-ultra-550b-a55b:free`
  → + sisa 109 model gratis (round-robin).
- Test bukti: `curl ... -d '{"model":"channel-researcher",...}'` → response `model:"claude-opus-4-6-thinking"`.

## SUB-AGENT (delegate_task) JANGAN TEMBUS OPENROUTER BERBAYAR
- Config `hermes config get delegation.model` default = `openrouter` (BARE) → 9Router tidak
  punya route itu → Hermes FALLBACK ke OpenRouter cloud pakai key `sk-or-...` → **BERBAYAR**
  (ini penyebab saldo $0.11 kemarin, bukan cuma bot clipper!).
- **FIX (wajib, via hermes config, bukan edit manual YAML — dilindungi):**
  ```bash
  hermes config set delegation.model "channel-researcher"
  hermes config set delegation.provider 9router
  ```
  Verifikasi: `hermes config get delegation.model` → `channel-researcher`.
- JANGAN set `delegation.model: openrouter` (bare). Pakai nama combo `channel-researcher`
  (lewat 9Router lokal, tidak tembus cloud) atau `kr/claude-haiku-4.5` (Kilo gratis).

## PITFALL (tambahan)
- Edit DB lalu **HARUS restart 9Router** biar reload (kill PID port 20128, lalu bash launch).
- Jangan hapus `providerConnections` openrouter — cukup filter di `combos`.
- `:free` model bisa kena 429 rate-limit harian → punya 120 model gratis memberi fallback luas.
- Model `openrouter/*` tanpa `:free` = BERBAYAR. Jangan masukkan ke combo kalau mau $0.
- **Sub-agent pakai model bare `openrouter` = berbayar**. Selalu arahkan ke `channel-researcher`.
