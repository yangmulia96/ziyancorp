# ZIYAN Shared Memory Bridge (TG ↔ DC ↔ Desktop) — VERIFIED 2026-08-09 (run ke-2)

Perintah Bos: "Pasang cron bridge dan import semua ingatan ke situ, jadikan ingatan bersama & default."

## MASALAH
Hermes TIDAK punya bridge antar-platform bawaan. Tiap platform = session terpisah:
- Telegram: `agent:main:telegram:dm:7349146540` (user `Yang Mulia`)
- Discord: `agent:main:discord:chat:1532759261610774768` (channel #hq)

Apa yang dibahas di TG tidak otomatis diketahui di DC & sebaliknya.

## ASET DI DISK (sudah ada — JANGAN bikin ulang)
| File | Fungsi |
|---|---|
| `C:\Users\arija\ZIYAN_BRIDGE\SHARED_MEMORY.md` | Ingatan bersama. **Ini juga STATE-nya.** |
| `C:\Users\arija\ZIYAN_BRIDGE\bridge_sync.py` | Sync inkremental, hitung delta, tulis `_sync_state.json` |
| `C:\Users\arija\ZIYAN_BRIDGE\_sync_state.json` | Hasil delta: `last_seen`, `new_total`, `new_inbound_msgs`, `tg_tail`, `dc_tail` |
| `C:\Users\arija\ZIYAN_BRIDGE\build_bridge.py` | Generator awal (one-shot, jarang dipakai lagi) |

Cron: job `e5e90dbf44f7` ("ZIYAN Bridge TG-DC"), tiap 30 menit.

## ALUR KERJA TIAP TICK (urutan yang terbukti)
1. `read_file SHARED_MEMORY.md` — lihat `LAST SYNC` + tail lama.
2. `terminal: cd C:/Users/arija/ZIYAN_BRIDGE && python bridge_sync.py`
   → cetak `new_total` / `new_inbound` / `new_inbound_msgs` + regenerate `_sync_state.json`.
3. `read_file _sync_state.json` → ambil `tg_tail` & `dc_tail` (masing-masing 30 baris siap tempel).
4. `write_file SHARED_MEMORY.md` — tulis ULANG file penuh (header + STATISTIK + ringkasan +
   2 section tail + KEPUTUSAN + BACKLOG). **Redaksi kredensial manual di sini.**
5. `terminal: python bridge_sync.py` lagi → **ini verifikasi**: `last_seen` harus naik ke timestamp
   terbaru yang barusan ditulis, `new_total` turun ke ~0. Kalau `last_seen` tidak berubah, berarti
   format tail yang kamu tulis tidak cocok regex → sync akan mengulang pesan yang sama selamanya.

## STATE ADA DI MARKDOWN, BUKAN DI JSON (paling penting)
`bridge_sync.py` menghitung `last_seen` dengan regex ke **isi SHARED_MEMORY.md**, bukan dari
`_sync_state.json`:
```python
re.findall(r"\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] %s " % plat, old)
```
Konsekuensi:
- Format baris tail WAJIB persis `[YYYY-MM-DD HH:MM:SS] telegram <isi>` / `... discord <isi>`.
  Ubah format = state hilang = duplikasi pesan tiap tick.
- Kalau tail tidak ditulis ke .md, `last_seen` mundur dan delta membengkak.
- `_sync_state.json` cuma laporan, aman dihapus.

## agent.log MEMOTONG PESAN DI 80 KARAKTER (pelajaran keras 2026-08-09)
Baris log gateway:
```
INFO gateway.run: inbound message: platform=telegram user=Yang Mulia chat=7349146540 msg='<80 char pertama>' reply_to_id=None
```
Isi `msg='...'` **dipotong ~80 karakter** — ekor pesan Bos TIDAK ADA di log, tidak bisa direcover
dari `agent.log` maupun `grep` sebanyak apa pun. Baris `agent.turn_context` juga memotong di panjang
yang sama (`msg='...'` + `...`).
- Dampak nyata: Bos mendikte spesifikasi ("Begini alur yang aku inginkan — Aku kirim link Affiliate
  dan file foto atau video …") dan sisanya hilang.
- **Aturan**: kalau pesan terpotong menyangkut keputusan/spesifikasi, TULIS di KEPUTUSAN bahwa
  ekornya hilang + minta Bos ulangi bagian akhir. JANGAN mengarang lanjutan kalimat.
- Untuk isi penuh, sumbernya `session_search`, bukan `agent.log`.

## REDAKSI KREDENSIAL — MANUAL
`bridge_sync.py` **tidak** meredaksi apa pun. `tg_tail` bisa memuat plaintext (pernah kejadian:
X Consumer Key/Secret, n8n API key dikirim Bos via chat). Sebelum `write_file`, ganti jadi
`[REDACTED - <nama kredensial>]`. Catat juga di KEPUTUSAN bahwa `agent.log` masih plaintext →
rekomendasikan rotasi key ke Bos.

## STRUKTUR SHARED_MEMORY.md (pertahankan)
`# judul` → `LAST SYNC:` → `## STATISTIK` → `## RINGKASAN ZIYAN` (per tanggal) →
`## PESAN TELEGRAM TERAKHIR (30)` → `## PESAN DISCORD TERAKHIR (30)` →
`## KEPUTUSAN` (append-only, prefix `- [YYYY-MM-DD HH:MM]`) → `## BACKLOG AKTIF` (bernomor).

## SINYAL YANG WAJIB DIANGKAT KE LAPORAN
- Pesan Bos yang **diulang ≥3x lintas platform** = eskalasi, bukan status biasa
  (contoh: workflow n8n `948713af` diminta 4x dalam 1 jam).
- Bos menyuruh satu platform "kasih tau" platform lain / minta ditulis "biar aku copy paste"
  = Bos sedang jadi kurir manual → bridge gagal dipakai. Tegaskan gateway harus baca file ini duluan.
- Spesifikasi baru dari Bos → masuk `## KEPUTUSAN` + naikkan item `## BACKLOG AKTIF`.

## FORMAT LAPORAN KE BOS (maks 150 kata)
Jumlah pesan baru per platform → topik utama (maks 3) → **BUTUH TINDAKAN**.
JANGAN kirim ulang isi file. Bos hanya mau delta + keputusan.

## PITFALL
- **`patch` fuzzy-match menelan baris tetangga di list bernomor.** Terjadi 2x sesi ini: patch item
  BACKLOG bikin item lain hilang diam-diam. Kalau mengedit list bernomor / baris berurutan,
  masukkan SELURUH blok list ke `old_string` & `new_string`, lalu **`read_file` untuk verifikasi**.
  Kalau menulis ulang banyak section, `write_file` file penuh lebih aman daripada beberapa `patch`.
- `execute_code` DITOLAK di cron (`approvals.cron_mode`) → pakai `terminal` + `write_file` + `patch`.
- JANGAN edit `config.yaml` manual (dilindungi). Pakai `hermes config set ...`.
- Cron `deliver=origin` → lapor ke sesi asal. Mau ke Telegram, set deliver platform.
- Memory Hermes penuh (~2200 char) → konsolidasi dulu sebelum add; `memory replace` sering gagal
  dengan teks panjang → fallback remove+add.
- `skill_manage write_file/patch` DITOLAK kalau SKILL.md belum di-`skill_view` di giliran yang sama
  ("Refusing background curator write_file ... has not been loaded in this review turn").
