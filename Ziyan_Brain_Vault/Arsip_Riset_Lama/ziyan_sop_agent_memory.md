# SOP: Sistem Memori ZIYAN
Adaptasi konsep **Letta / MemGPT — "LLMs as OS: Agent Memory" (DeepLearning.AI)**
Status: aktif | Owner: Orchestrator | Versi 1.0

---

## 1. Ringkasan Konsep Memori Agent (MemGPT/Letta)

Ide inti: LLM itu seperti **OS**. Context window = **RAM** (kecil, cepat, mahal). Storage eksternal = **disk** (besar, lambat, murah). Agent bertugas melakukan *paging* sendiri — memindahkan info dari disk ke RAM saat perlu.

**Tingkatan memori:**

| Tier | Nama Letta | Isi | Sifat |
|---|---|---|---|
| In-context | **Core memory** (memory blocks) | Persona agent + fakta kunci user/proyek | Selalu ada di prompt, kecil, bisa di-edit agent sendiri |
| Out-context | **Recall memory** | Riwayat percakapan mentah (event log) | Dicari via `conversation_search` |
| Out-context | **Archival memory** | Fakta/dokumen jangka panjang, vector DB | Ditulis via `archival_memory_insert`, dibaca via `archival_memory_search` |

**Cara agent "mengingat":**
1. Core memory selalu ikut di setiap prompt → identitas & konteks tak pernah hilang.
2. Saat context penuh → **auto-summarization / eviction**: pesan lama diringkas, aslinya turun ke recall memory.
3. Saat butuh info lama → agent memanggil tool search (recall/archival) → hasil disisipkan balik ke context (page-in).
4. **Memory editing**: agent aktif menulis ulang core memory-nya sendiri (self-editing) ketika ada fakta baru yang penting.
5. **Heartbeat / multi-step**: agent boleh lanjut berpikir setelah tool call, bukan hanya sekali balas.

**Self-host**: Letta jalan sebagai server (Docker) + Postgres/pgvector, agent state persist di DB — agent tetap "hidup" antar sesi. Ini poin penting: **agent = state, bukan cuma prompt.**

---

## 2. Pemetaan ke ZIYAN

Kita **TIDAK install Letta**. Kita replika arsitekturnya pakai infra yang sudah ada.

| Konsep Letta | Padanan ZIYAN | Keterangan |
|---|---|---|
| Core memory (in-context) | **Hermes `memory` tool** (persist ke disk, auto-inject) | Fakta stabil: preferensi Bos, identitas ZIYAN, keputusan strategis |
| Recall memory | **Session history Hermes** + `session_search` | Riwayat percakapan lintas sesi, FTS5 |
| Archival memory | **`ZIYAN_COMPANY_LOG.md`** + file riset/output di `C:\Users\arija\` | Dokumen panjang, progres, hasil riset |
| Procedural memory | **Skills** (`skill_manage` / `skill_view`) | "Cara melakukan" — SOP, workflow, command pasti |
| Secrets (bukan memori) | **`ziyan_keys.env`** | Kredensial. JANGAN pernah masuk memory/log/chat |
| Self-editing memory | Orchestrator patch memory + patch skill setelah task | Agent memperbaiki memorinya sendiri |
| Paging / context mgmt | Delegasi ke subagent (leaf) | Riset berat dikerjakan subagent, hanya ringkasan naik ke parent |

**Handoff doc = jembatan antar sesi.** `ZIYAN_COMPANY_LOG.md` berperan seperti archival memory yang human-readable: sesi baru cukup baca log ini untuk tahu posisi perusahaan.

---

## 3. SOP — Apa Disimpan ke Mana

### 3.1 Aturan Routing (wajib)

**→ `memory` tool** (fakta pendek, stabil, sering dipakai)
- Preferensi Bos (bahasa, gaya jawab, jam kerja)
- Identitas & positioning ZIYAN
- Keputusan strategis final ("pakai 9router untuk model gratis")
- Nama file/path penting
- Batas: 1–2 kalimat per entri. Kalau >3 baris → itu archival, taruh di log.

**→ `ZIYAN_COMPANY_LOG.md`** (progres & narasi)
- Apa yang dikerjakan hari ini, hasilnya, status
- Output divisi (riset, konten, produksi)
- Backlog & next action
- Format entri: `## YYYY-MM-DD — <Divisi> — <Judul>` lalu 3–6 bullet: Konteks / Hasil / File / Next.

**→ `ziyan_keys.env`** (rahasia)
- API key, token, password. Format `NAMA=nilai`.
- ATURAN KERAS: tidak pernah di-print, tidak pernah di-echo, tidak pernah masuk memory/log/chat. Referensikan **nama variabel** saja.
- Cek keberadaan pakai `grep -q '^NAMA=' ziyan_keys.env && echo ADA`.

**→ Skills** (pola & prosedur)
- Workflow yang berhasil setelah ≥5 tool call
- Error yang sudah dipecahkan + cara hindarinya (section Pitfalls)
- Command persis, bukan deskripsi
- Kalau skill dipakai lalu ternyata salah/kurang → **langsung patch**, jangan tunggu disuruh.

### 3.2 Siklus Kerja per Task

1. **Sebelum mulai**: baca `ZIYAN_COMPANY_LOG.md` (state) + `skills_list` (prosedur) + `session_search` kalau Bos menyinggung hal lama.
2. **Selama**: kerja di file, bukan di context. Output besar → tulis ke file, laporkan path.
3. **Sesudah** (wajib, "commit memory"):
   - Fakta baru yang stabil → `memory`
   - Progres → append ke `ZIYAN_COMPANY_LOG.md`
   - Key baru → `ziyan_keys.env`
   - Pola baru/perbaikan → `skill_manage`
4. **Compaction bulanan**: ringkas entri log >30 hari jadi 1 paragraf per bulan, arsipkan detail ke `ZIYAN_LOG_ARCHIVE_<bulan>.md`. Ini padanan auto-summarization Letta.

### 3.3 Anti-Pattern
- ❌ Menaruh progres panjang di `memory` → memory jadi bengkak, tiap prompt mahal.
- ❌ Menaruh fakta kunci hanya di chat → hilang saat sesi habis.
- ❌ Menaruh key di log/memory → kebocoran.
- ❌ Menulis ulang prosedur tiap sesi → seharusnya jadi skill.
- ❌ Subagent mengirim transkrip penuh ke parent → kirim ringkasan + path file.

---

## 4. Tabel Akhir

| Jenis Memori | Tempat di ZIYAN | Kapan Diakses |
|---|---|---|
| **Core / fakta kunci** | Hermes `memory` tool | Otomatis, tiap sesi & tiap prompt |
| **Recall / riwayat percakapan** | Session DB Hermes (`session_search`) | Saat Bos menyinggung obrolan lama |
| **Archival / progres & narasi** | `ZIYAN_COMPANY_LOG.md` | Awal sesi (orientasi) & akhir sesi (tulis) |
| **Archival / dokumen & riset** | File `.md` di `C:\Users\arija\` | Saat butuh detail hasil kerja sebelumnya |
| **Procedural / cara kerja** | Skills (`skill_view` / `skill_manage`) | Sebelum eksekusi task berulang |
| **Secrets** | `ziyan_keys.env` | Hanya saat runtime tool butuh; tidak pernah dibaca ke context |
| **Working memory** | Context window sesi aktif | Selama task; dibuang setelah di-commit ke 4 tempat di atas |

> Prinsip tunggal: **apa pun yang tidak ditulis ke disk sebelum sesi berakhir, dianggap tidak pernah terjadi.**
