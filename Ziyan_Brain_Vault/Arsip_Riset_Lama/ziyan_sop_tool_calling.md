# SOP ZIYAN — Tool-Calling Handal di Model Gratis
Sumber pola: DeepLearning.AI #5 "Functions, Tools & Agents with LangChain" (Harrison Chase). Kita TIDAK pakai LangChain — pola-nya direplika ke skill/tools Hermes.

---

## 1. Ringkasan Pola Tool-Calling (materi publik)

Kursus ini 6 modul, intinya:

1. **OpenAI Function Calling** — model tidak mengeksekusi fungsi, model hanya mengembalikan *nama fungsi + argumen JSON*. Eksekusi tetap di sisi kita.
2. **Schema definition (Pydantic → JSON Schema)** — deklarasikan tool sebagai objek: `name`, `description`, `parameters` (JSON Schema: type/properties/required/enum). Description adalah *prompt*, bukan dokumentasi: model memilih tool berdasarkan description.
3. **Tagging & Extraction** — kasus paling andal: paksa model output terstruktur dengan satu schema wajib (`tool_choice` dipaksa) alih-alih membiarkan model bebas memilih.
4. **Tool routing** — banyak tool → model memilih satu → parser mengubah argumen jadi call → hasil dikembalikan ke model sebagai pesan role `tool`/`function`.
5. **Parsing & error handling** — 4 lapis:
   - parse JSON gagal → repair (strip fence, ambil balanced braces) → retry
   - schema validation gagal → kirim pesan error validasi ke model → retry (self-heal)
   - tool raise exception → kembalikan error sebagai observasi, bukan crash
   - loop guard: max iterasi (biasanya 5–10), anti tool-call berulang identik
6. **Agent loop (conversational agent)** — while: LLM → tool call? → eksekusi → append observasi → ulang; berhenti saat model jawab tanpa tool call atau limit tercapai.

**Aturan emas dari kursus yang paling relevan buat model kecil:** semakin sedikit tool, semakin datar schema, semakin eksplisit description → semakin tinggi success rate.

---

## 2. Map ke ZIYAN

| Konsep kursus | Padanan ZIYAN |
|---|---|
| Tool / function | Tool bawaan Hermes (`terminal`, `write_file`, `search_files`, `browser_*`) |
| Toolkit khusus domain | Skill di `~/AppData/Local/hermes/skills/` (SKILL.md = description + SOP) |
| Agent executor | Loop agent Hermes |
| Sub-agent dengan tool sendiri | `delegate_task` — subagent leaf dapat subset tool, konteks bersih |
| Output parser + retry | Wrapper kita: validasi hasil tool, re-prompt kalau invalid |
| Model backend | 9router (gemma / nemotron / tencent-hy3) + Gemini sebagai fallback berbayar-gratisan |

### Titik lemah kita
Model gratis di 9router sering: (a) menulis tool call sebagai teks biasa, (b) halusinasi nama tool, (c) argumen JSON rusak (trailing comma, fence ```json), (d) nested object terlalu dalam → argumen kosong.

### Penguatan
- **Prompt engineering**: satu blok "TOOLS" di awal, tiap tool 1 baris + contoh call konkret. Selalu sertakan 1 few-shot call yang benar.
- **Schema ketat**: flat, ≤5 field, semua string/number/enum, `required` diisi penuh, hindari `anyOf`/nested array-of-object.
- **Delegasi**: pakai `delegate_task` agar tiap subagent cuma lihat 3–6 tool relevan, bukan 30.
- **Fallback model**: jika 2× gagal parse → naik ke model lebih kuat (Gemini) untuk langkah tool-calling saja, lalu turun lagi untuk generasi teks (hemat kuota).

---

## 3. SOP: Tool-Calling Handal di Model Gratis

**Langkah 0 — Cek dukungan native.** Sebelum pakai model baru di 9router, tes 1 tool sederhana (`get_time`). Kalau model balas JSON di dalam teks (bukan field `tool_calls`), tandai model itu **text-mode** → wajib pakai protokol teks (langkah 3).

**Langkah 1 — Kurasi tool.** Maksimal 5–7 tool per agent. Sisanya pindah ke subagent via `delegate_task`.

**Langkah 2 — Tulis schema ketat.**
```json
{"name":"cari_harga","description":"Cari harga produk di katalog ZIYAN. Pakai saat user menyebut nama produk.",
 "parameters":{"type":"object","properties":{"produk":{"type":"string"},"kota":{"type":"string","enum":["jakarta","bandung"]}},"required":["produk","kota"]}}
```
Aturan: description mulai dengan kata kerja + "Pakai saat ..."; tanpa nested object; enum untuk semua pilihan tertutup.

**Langkah 3 — Protokol teks untuk model text-mode.** Paksa format tunggal:
```
<tool>{"name":"cari_harga","arguments":{"produk":"X","kota":"jakarta"}}</tool>
```
Parser: regex ambil isi `<tool>...</tool>` → `json.loads` (strict=False). Instruksi keras: "Keluarkan HANYA blok <tool> tanpa penjelasan bila butuh tool."

**Langkah 4 — Repair sebelum retry.** Urutan: strip ```fence → potong sampai brace seimbang → ganti kutip tunggal → hapus trailing comma. Baru kalau tetap gagal, retry ke model.

**Langkah 5 — Retry berlapis (maks 3).**
1. Retry-1: kirim balik pesan `ERROR: JSON tidak valid. Keluarkan ulang HANYA blok <tool>.`
2. Retry-2: kirim schema lagi + 1 contoh benar (few-shot injeksi).
3. Retry-3: switch model (fallback ladder di bawah), suhu 0.

**Langkah 6 — Validasi argumen.** Cek `required` ada, tipe cocok, enum valid. Kalau nama tool halusinasi → balas daftar tool valid, jangan crash.

**Langkah 7 — Eksekusi & observasi.** Bungkus try/except; error dikirim balik sebagai observasi singkat (≤300 char) agar model bisa self-heal, bukan traceback penuh.

**Langkah 8 — Loop guard.** Max 8 iterasi; kalau 2 tool call identik berurutan → hentikan, minta model menyimpulkan.

**Langkah 9 — Log & evaluasi.** Catat per model: `tool_call_success_rate`. Ganti default model bila <80% pada 20 percobaan.

**Fallback ladder:** tencent/hy3 → nemotron → gemma → Gemini (hanya untuk step tool-call).

**Setting wajib:** temperature 0–0.2, max_tokens cukup besar (argumen terpotong = JSON rusak), stop sequence `</tool>`.

---

## 4. Tabel Ringkas

| Teknik | Implementasi ZIYAN | Model gratis yang cocok |
|---|---|---|
| Native function calling (field `tool_calls`) | Panggil langsung via API 9router | tencent/hy3, nemotron (cek per-versi) |
| Protokol teks `<tool>{...}</tool>` | Parser regex + `json.loads` di wrapper Hermes | gemma (paling aman di sini), model text-mode apa pun |
| Schema flat + enum + required penuh | Definisi tool di skill / SKILL.md | semua |
| Description sebagai prompt ("Pakai saat...") | Frontmatter description skill Hermes | semua, kritikal untuk gemma |
| Few-shot 1 contoh call benar | Prepend di system prompt agent | gemma, nemotron |
| JSON repair sebelum retry | Util `repair_json()` dipakai semua agent | semua |
| Retry berlapis 3 tingkat | Loop wrapper: error msg → few-shot → ganti model | semua |
| Forced single-tool (extraction mode) | Task 1-tool: parsing dokumen, tagging | gemma, tencent/hy3 |
| Kurasi ≤6 tool + `delegate_task` | Subagent leaf punya toolset sendiri | wajib untuk semua model gratis |
| Loop guard + anti-repeat | Max 8 iterasi di orchestrator | semua |
| Fallback ke model kuat | Gemini hanya untuk step tool-call | Gemini (cadangan) |
| Temperature 0 + stop sequence | Config per-agent 9router | semua |

---
*Dokumen internal ZIYAN. Tidak memuat kredensial.*
