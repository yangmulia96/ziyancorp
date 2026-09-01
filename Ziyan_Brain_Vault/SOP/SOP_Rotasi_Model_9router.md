# SOP Rotasi Model LLM — Proxy 9router

**Tujuan:** Bila model yang dipakai kena `402` / `429` / *timeout*, otomatis pindah ke
model *free* lain yang terverifikasi jalan. Ini mencegah beban numpuk di satu model
saja dan menjaga sesi chat tidak putus karena limit.

**Endpoint:** `http://127.0.0.1:20128/v1`
**API Key:** env `HERMES_CUSTOM_9ROUTER_API_KEY` (jangan di-hardcode / di-print).

---

## 1. Mengapa rotasi perlu?

- **Limit bulanan di `kr/*` dan `kimi/*`** → balasan `402 Payment Required`.
  Model ini pakai kuota berbayar/bulan; kalau kehabisan, semua call gagal.
- **Rate limit `429`** → terlalu banyak request dalam waktu singkat ke satu model
  (mis. `poolside/laguna-xs`, `laguna-m`). Rotasi menyebar beban.
- **Timeout model berat** → model besar (`nemotron-3-ultra-550b`, dll.) lambat
  menjawab dan sering melebihi batas waktu, memutus sesi.
- Rotasi = sebar traffic ke beberapa model *free* yang sudah terbukti jalan,
  sehingga tidak ada satu model yang kehabisan kuota / kena throttle sendirian.

---

## 2. Model free terverifikasi JALAN (urut prioritas)

Tes langsung: `max_tokens=30`, prompt `"Halo"` → respons tidak kosong.

| # | ID (pakai ini di API) | Catatan |
|---|------------------------|---------|
| 1 | `google/gemma-4-31b-it:free` | Prioritas utama, cepat & stabil |
| 2 | `google/gemma-4-26b-a4b-it:free` | Alternatif gemma, ringan |
| 3 | `poolside/laguna-s-2.1:free` |Reasoning, andal |
| 4 | `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free` | Nano + reasoning |
| 5 | `nvidia/nemotron-3-super-120b-a12b:free` | Super, lebih berat |
| 6 | `nvidia/nemotron-3-nano-30b-a3b:free` | Nano, ringan |
| — | `groq/llama-3.3-70b-versatile` | **Cadangan** (bukan free, lewat groq) |

> Urutan di atas = urutan yang dicoba script `rotasi.sh`. Groq ditaruh terakhir
> sebagai *fallback* bila semua free habis.

---

## 3. Model yang HARUS DIHINDARI + alasan

| Model | Alasan |
|-------|--------|
| `kr/*` (semua, mis. `kr/auto`, `kr/claude-*`, `kr/deepseek-*`, `kr/glm-*`) | Limit bulanan → `402`. Kuota berbayar, cepat habis. |
| `kimi/*` (mis. `kimi/k3`, `kimi/kimi-k2.*`, `kimi/kimi-for-coding*`) | Limit bulanan → `402`. |
| `nvidia/nemotron-3-ultra-550b*` (mis. `nemotron-3-ultra-550b-a55b`) | Timeout — terlalu berat, sering lewat batas waktu. |
| `poolside/laguna-xs*` (mis. `laguna-xs-2.1`) | `429` rate limit — kecil & sering throttle. |
| `poolside/laguna-m*` (mis. `laguna-m.1`) | `429` rate limit. |

Jangan masukkan model di atas ke daftar rotasi otomatis.

---

## 4. Script rotasi otomatis (`rotasi.sh`)

Script di bawah ini: loop model dari daftar prioritas §2, kirim test call kecil,
lanjut ke model berikutnya bila gagal (`402`/`429`/timeout/empty), dan cetak
`MODEL_OK: <id>` lalu `exit 0` bila berhasil.

```bash
#!/usr/bin/env bash
# rotasi.sh - Cari model free yang LANGSUNG JALAN di proxy 9router
set -u

BASE_URL="${NINEROUTER_BASE_URL:-http://127.0.0.1:20128/v1}"
API_KEY="${HERMES_CUSTOM_9ROUTER_API_KEY:-}"
TIMEOUT="${ROTASI_TIMEOUT:-20}"
MAX_TOKENS=30

if [ -z "$API_KEY" ]; then
  echo "ERROR: env HERMES_CUSTOM_9ROUTER_API_KEY kosong. Export dulu." >&2
  exit 2
fi

MODELS=(
  "google/gemma-4-31b-it:free"
  "google/gemma-4-26b-a4b-it:free"
  "poolside/laguna-s-2.1:free"
  "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free"
  "nvidia/nemotron-3-super-120b-a12b:free"
  "nvidia/nemotron-3-nano-30b-a3b:free"
  "groq/llama-3.3-70b-versatile"
)

test_model() {
  local model="$1"
  local http_out code body content
  http_out=$(curl -sS --max-time "$TIMEOUT" -w '\n__HTTP__%{http_code}' \
    "$BASE_URL/chat/completions" \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d "$(python3 -c "import json; print(json.dumps({'model':'''$model''','messages':[{'role':'user','content':'Halo'}],'max_tokens':$MAX_TOKENS}))")" 2>/dev/null)
  code=$(printf '%s' "$http_out" | sed -n 's/.*__HTTP__//p')
  body=$(printf '%s' "$http_out" | sed '/__HTTP__/d')
  [ -z "$code" ] && { echo "TIMEOUT/NO_RESPONSE ($model)"; return 1; }
  if [ "$code" = "402" ] || [ "$code" = "429" ]; then echo "HTTP $code ($model)"; return 1; fi
  if [ "$code" != "200" ]; then echo "HTTP $code ($model)"; return 1; fi
  content=$(printf '%s' "$body" | python3 -c '
import sys, json
try: d = json.load(sys.stdin)
except Exception: print(""); sys.exit(0)
if d.get("error"): print(""); sys.exit(0)
try: c = d["choices"][0]["message"]["content"]
except Exception: print(""); sys.exit(0)
print(c if c is not None else "")')
  [ -z "$content" ] && { echo "EMPTY ($model)"; return 1; }
  echo "OK"; return 0
}

for m in "${MODELS[@]}"; do
  reason=$(test_model "$m")
  if [ "$reason" = "OK" ]; then echo "MODEL_OK: $m"; exit 0; fi
  echo "SKIP $m -> $reason" >&2
done
echo "NO_MODEL_AVAILABLE: semua model gagal" >&2
exit 1
```

File script juga tersimpan di `C:\Users\arija\rotasi.sh` (sudah executable-ready).

---

## 5. Cara pakai

```bash
# 1. Export key (jangan hardcode di script)
export HERMES_CUSTOM_9ROUTER_API_KEY="<isi_key_9router>"

# 2. Jalankan rotasi untuk dapat model hidup
bash /c/Users/arija/rotasi.sh
# Contoh output:  MODEL_OK: google/gemma-4-31b-it:free

# 3. Ambil id tersebut, lalu pakai di tugas / chat Anda, mis.:
export MODEL_LIVE=$(bash /c/Users/arija/rotasi.sh | grep '^MODEL_OK:' | cut -d' ' -f2)
echo "Pakai model: $MODEL_LIVE"
```

**Rutin:** jalankan `bash rotasi.sh` **sebelum mulai tugas** (atau bila sesi tiba-tiba
drop / dapat `402`/`429`/timeout) supaya selalu pakai model yang sedang hidup, bukan
model yang sudah kehabisan kuota.
