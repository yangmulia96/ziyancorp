# Spesifikasi Resmi — Workflow Affiliate Auto-Post ZIYAN (`948713af`)

Workflow ID: `948713af-fbe5-4e74-af74-3f2d69815d70`
Nama DB: `ZIYAN Shopee Affiliate -> FB Page Carousel (Firestore + 9router + PIL)`

Ini item yang PALING SERING diminta Bos (diulang >6x dalam 1 hari, 2026-08-09).
Sebelum kerja apa pun di sini, baca `C:\Users\arija\ZIYAN_BRIDGE\SHARED_MEMORY.md`
section `## BACKLOG AKTIF` + `## KEPUTUSAN`.

---

## 1. Spesifikasi verbatim dari Bos

Diambil dari **session DB** (`session_search`), BUKAN dari `agent.log` — log memotong
pesan di 80 karakter dan ekor kalimat hilang.

> "Aku kirim link Affiliate dan file foto atau video baik 1 file maupun banyak file
> walaupun 1 link.. ke telegram bot.
>
> Jika filenya banyak (misalnya 2 file) dan link nya 1. Maka jadi 2 konten yang akan
> di post. Lengkap dengan caption seperti yang telah aku ajarkan...
>
> Dari bot telegram masuk ke sheet dan disimpan disitu, per 8 menit sekali di upload
> dan di schedule di sosmed per 77 menit sekali publish."

**REVISI Bos (24 menit kemudian, sesi yang sama):**

> "Bot bisa simpan filenya dan upload per 33 menit sekali lalu di schedule kan per 77 menit?"

→ Interval generate/upload **8 menit DIBATALKAN, jadi 33 menit**. Publish tetap **77 menit**.

## 2. Alur target

```
Bot Telegram (1 link + N file foto/video)
      │
      ├─ simpan N file ke disk
      └─ tulis N row ke Google Sheet  (link, file_path, status_post=FALSE, platform)
                │
   Schedule 33 mnt → ambil row FALSE → generate caption + aset → tandai "ready"
                │
   Schedule 77 mnt → ambil row "ready" → publish FB / X / YouTube → tandai TRUE
```

Aturan turunan:
- **1 link + N file = N konten terpisah.** Bukan 1 post carousel, kecuali Bos minta.
- Video (mp4/mov/webm/mkv) → FB Video + YT Shorts. Foto → FB Photo/Carousel (skip YT).
- Notifikasi hasil balik ke Telegram Bos.

## 3. Format caption — WAJIB `SOP_caption_ig_fb.md`

Bos mengoreksi tegas: **"Sop ku bukan 3 narasi. Kamu lupa format caption yang aku ajarkan?"**

```
[LINK affiliate persis, di baris paling atas]
[caption natural + HARGA + fitur, ringkas, gaya teman bukan sales]
[maksimal 5 hashtag kreatif]
```

- Harga **WAJIB** ada. Link **WAJIB** persis sama, tidak dipendekkan/diubah.
- SOP **3-narasi** (`SOP_konten_tiktok.md`) HANYA untuk TikTok. Jangan dipakai di sini.

## 4. Status nyata (audit 2026-08-09, dibaca langsung dari sqlite)

Workflow `active=1` tapi **tidak bisa jalan otomatis**. Isi nyata **9 node**:

| # | Node | Tipe |
|---|------|------|
| 1 | Telegram: Input Link+File | telegramTrigger |
| 2 | Split N File -> Rows | code |
| 3 | Sheet: Append Rows | googleSheets |
| 4 | Parse Sheet Row | code |
| 5 | Sheets: Mark Posted | googleSheets |
| 6 | FB: Post Photo + Link | httpRequest |
| 7 | FB: Upload Video | httpRequest |
| 8 | X: Post Tweet | code |
| 9 | YouTube: Upload Shorts | httpRequest |

**Blocker terbuka:**
1. Node `Schedule Generate (33m)` & `Schedule Publish (77m)` **TIDAK ADA** — script yang
   mestinya menambahkannya kena `IndexError` dan tidak pernah commit (lihat PITFALL #21).
   Tanpa trigger jadwal, workflow tidak akan pernah jalan sendiri.
2. `documentId` Google Sheet masih `SHEET_ID_PLACEHOLDER`.
3. Generator caption belum memakai format SOP di atas.
4. `Split N File -> Rows` belum tersambung ke handler file Telegram sungguhan.

Catatan: pernah dilaporkan ke Bos sebagai "17 node" — **itu keliru**. Selalu verifikasi
dengan SELECT sebelum lapor.

## 5. Perintah keras Bos untuk workflow ini

- "Work flow apa lagi yang kau buat? Kan udh ada di n8n itu? **Tinggal kamu edit aja**"
- "**langsung kau edit.. banyak kali kau tanya**"

→ DILARANG bikin workflow baru. DILARANG minta konfirmasi. Edit in-place `948713af`,
verifikasi, lalu minta Bos restart n8n (satu kali, sebutkan alasannya).

## 6. Pertanyaan Bos yang belum terjawab

- "Yang mengelola sheet siapa? Apa perlu AI agent?" — jawab singkat, jangan node-by-node
  (Bos pernah bilang "Bingung aku penjelasan mu" saat uraian terlalu teknis).
