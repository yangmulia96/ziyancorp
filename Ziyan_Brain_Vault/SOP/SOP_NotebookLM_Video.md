# SOP – Membuat Video Short & Long di Google NotebookLM (Gemini Notebook)

**Versi:** 1.0
**Tanggal:** 31 Juli 2026
**Untuk:** Tim non-teknis
**Sumber acuan:** Dokumentasi resmi Google Support (Gemini Notebook / NotebookLM)

> ⚠️ **Catatan Penting (Rebranding):** Per 2026, layanan ini berganti nama dari **NotebookLM** menjadi **Gemini Notebook**. URL lama `notebooklm.google.com` masih mengarah ke layanan yang sama. Sepanjang dokumen ini, "NotebookLM" dan "Gemini Notebook" merujuk pada produk yang sama.

---

## 1. Ringkasan & Hal-Hal Krusial (Baca Dulu)

Sebelum mulai, pahami 3 batasan yang paling sering membuat orang bingung:

| Hal | Fakta |
|---|---|
| **Format "Short"** | Hanya ~60 detik, **Bahasa Inggris saja**, usia **18+** |
| **Format "Cinematic"** | Imersif/sinematik, **Bahasa Inggris saja**, usia **18+** |
| **Format "Explainer"** | Komprehensif & lebih panjang, **mendukung banyak bahasa** (termasuk Indonesia) |
| **Gaya Visual** (Classic, Whiteboard, Watercolor, dll) | Hanya untuk pengguna **18+**, **tidak** berlaku untuk format Cinematic & Short |
| **Waktu generate** | Bisa **> 30 menit**. Jalan di *background* — Anda bisa menutup tab dan kembali nanti |
| **Akun** | Butuh **Akun Google** (email @gmail atau Workspace) |

**Definisi "Short" vs "Long" di NotebookLM:**
- **Video PENDEK** = format **"Short"** (~60 detik).
- **Video PANJANG** = format **"Explainer"** (ringkasan komprehensif, durasi mengikuti banyaknya isi sumber) atau **"Cinematic"** (lebih sinematik). NotebookLM **tidak punya mode "long-form 10–30 menit"** secara native — lihat **Bagian 4 & 6** untuk workaround long-form.

---

## 2. Daftar Istilah

- **Notebook** = "buku" berisi kumpulan sumber untuk satu proyek.
- **Sumber (Source)** = file/dokumen/URL yang Anda unggah sebagai bahan video.
- **Studio** = panel di sebelah kanan tempat Anda memicu pembuatan Video/Audio/Mind Map/Slide/Infografis.
- **Video Overview** = fitur pembuat video otomatis dari isi notebook.
- **Steering Prompt** = instruksi tambahan untuk mengarahkan isi video (mis. "fokus ke bagian keuangan").

---

## 3. Bagian 0 – Prasyarat

- Perangkat dengan browser (Chrome/Edge disarankan) dan koneksi internet.
- Akun Google aktif (lihat Bagian 1 jika belum punya).
- Usia **18 tahun ke atas** untuk fitur Short, Cinematic, dan Gaya Visual.
- Bahan berupa file atau tautan (PDF, DOCX, TXT, URL web, teks, dll — lihat Bagian 2).

---

## 4. Bagian 1 – Buat/Akses Akun Google & NotebookLM

### Jika BELUM punya Akun Google:
1. Buka `https://accounts.google.com/signup`.
2. Isi nama, pilih alamat email `@gmail.com`, buat kata sandi.
3. Verifikasi nomor HP (untuk keamanan).
4. Selesaikan langkah verifikasi → Akun Google siap.

### Akses NotebookLM:
1. Buka `https://notebooklm.google.com` (atau cari "Gemini Notebook" / "NotebookLM" di Google).
2. Klik **Sign in / Masuk** dan pilih Akun Google Anda.
3. Jika pertama kali, terima persyaratan layanan. Anda masuk ke beranda NotebookLM.

---

## 5. Bagian 2 – Buat Notebook Baru & Upload Sumber

1. Di beranda, klik **"Create new notebook" / Buat notebook baru**.
2. Pada jendela popup, klik **"Upload a source" / Unggah sumber**.
3. Pilih sumber yang ingin diunggah (lihat jenis di bawah), lalu **Open / Buka**.
   - Untuk menambah lagi nanti: klik **"+ Add"** di panel Sources.
4. Tunggu proses ingest selesai (ikon sumber muncul di panel kiri).
5. (Opsional) Klik emoji notebook untuk mengganti ikonnya.

### Jenis Sumber yang Didukung
- **File lokal:** PDF, DOCX (Word), TXT, MD (Markdown), CSV, PPTX (PowerPoint), ePub.
- **Google Drive:** Google Docs, Google Slides (maks 100 slide), Google Sheets (maks 100k token) — otomatis sync.
- **Teks:** copy-paste langsung.
- **URL Web:** artikel/laman web (hanya teks; gambar/video embedded tidak diambil). PDF via URL dianggap PDF.
- **YouTube URL:** video publik ber-subtitle (hanya transkrip teks yang diambil).
- **Audio:** MP3, WAV, M4A, dll (ditranskrip otomatis).
- **Gambar:** JPG, PNG, WEBP, GIF, HEIC, dll.

### Batasan Sumber
- Setiap sumber: maks **500.000 kata** atau **200 MB** (untuk file unggahan).
- Jumlah sumber: maks **50 sumber** untuk pengguna **Free** (lebih banyak untuk paket berbayar/AI Premium).
- Hindari mengunggah dokumen yang tidak Anda miliki hak atasnya.

---

## 6. Bagian 3 – Memicu Pembuatan Video (Studio → Video Overview)

1. Pastikan notebook sudah punya ≥1 sumber.
2. Di panel **Studio** (sebelah kanan), klik **"Video Overview"**.
3. Sebelum generate, Anda bisa mengkustomisasi (lihat opsi di bawah). Jika dilewati, NotebookLM membuat video dengan pengaturan default.
4. Klik **"Generate" / Buat**.
5. Video diproses di *background*. Anda boleh pindah tab, menutup jendela, atau membuat artifact lain — nanti kembali ke notebook untuk melihat hasilnya.
   - Tip: Nyalakan **Web notifications** (Settings → Notifications → Web notifications → Allow) supaya dapat pemberitahuan saat selesai.

### Opsi Kustomisasi Video
- **Format:** `Cinematic` (imersif) | `Explainer` (komprehensif) | `Short` (~60 detik).
- **Language / Bahasa:** pilih bahasa narasi (Explainer mendukung banyak bahasa; Short & Cinematic hanya Inggris).
- **Visual Style / Gaya Visual:** `Classic, Whiteboard, Watercolor, Retro Print, Heritage, Paper-craft, Kawaii, Anime`, **Auto** (biarkan AI pilih), atau **Custom** (tulis deskripsi gaya sendiri). *Hanya 18+, tidak untuk Cinematic & Short.*
- **Steering Prompt (opsional):** pilih topik tersirat atau tulis topik sendiri, mis. "Buat video fokus ke langkah-langkah onboarding pelanggan."

---

## 7. Bagian 4 – Perbedaan & Cara Hasilkan Video SHORT vs LONG

### A. Video PENDEK (Short)
- **Cara:** Di opsi Format pilih **"Short"**.
- **Hasil:** video ~60 detik, ringkas, ambil poin kunci sumber.
- **Syarat:** Bahasa **Inggris**, usia **18+**. Tidak bisa ganti gaya visual.
- **Cocok untuk:** ringkasan cepat, konten sosial media, hook pembuka.

### B. Video PANJANG (Explainer / Cinematic)
NotebookLM tidak punya tombol "long". "Long" = pakai format **Explainer** (atau **Cinematic**):

- **Explainer** (DISARANKAN untuk konten Indonesia):
  - Ringkasan terstruktur & komprehensif, menyambungkan titik-titik antar sumber.
  - **Mendukung banyak bahasa** → pilih **Bahasa Indonesia** di opsi Language.
  - Mendukung **Gaya Visual** (Classic, Whiteboard, Watercolor, dll).
  - Durasi mengikuti keluasan isi sumber (umumnya beberapa menit).
- **Cinematic**:
  - Pengalaman sinematik/imersif, visual & storytelling lebih kaya.
  - **Hanya Bahasa Inggris**, usia **18+**, tanpa gaya visual kustom.

**Cara hasilkan Long:**
1. Pilih Format = **Explainer** (atau Cinematic).
2. Pilih **Language = Indonesian** (untuk Explainer).
3. Pilih **Visual Style** (mis. *Whiteboard* atau *Classic*) — opsional.
4. (Opsional) isi **Steering Prompt** agar video fokus ke bagian tertentu.
5. Klik **Generate**.

### Batasan Durasi Asli NotebookLM & Mengapa Perlu Workaround
- NotebookLM **tidak mempublikasikan batas durasi tetap**; video dirancang ringkas (Short ~60 dtk, Explainer/Cinematic beberapa menit tergantung isi).
- **Tidak ada mode native 10–30 menit.** Jika Anda butuh video panjang betulan (mis. tutorial 15 menit), pakai **workaround** di Bagian 6.

---

## 8. Bagian 5 – Download / Export Video ke File Lokal

1. Setelah Video Overview selesai, buka video tersebut di panel Studio (klik judul Video Overview → pemutar video terbuka).
2. Di dalam pemutar video, klik tombol **"Download"** (ikon panah ke bawah).
3. File video (umumnya `.mp4`/`.mov`) akan tersimpan ke folder **Download** di komputer Anda.
4. Video siap dibagikan / di-upload ke platform.

**Cara berbagi lain (jika tidak download):**
- **Share link:** klik **Share** di pemutar → pastikan notebook "Anyone with the link" & akses "full notebook" → salin tautan.
  - ⚠️ Link publik **hanya untuk akun konsumer** (@gmail). **Dimatikan** untuk akun Workspace Enterprise/Education.
- **Share notebook utuh:** orang lain bisa memutar video lewat panel Studio.

---

## 9. Bagian 6 – Workaround LONG-FORM (Video Panjang Betulan > Beberapa Menit)

Karena NotebookLM tidak membuat video 10–30 menit sekaligus, gunakan salah satu cara berikut:

### Cara A – Potong Menjadi Beberapa Notebook + Gabung (Paling Mudah)
1. Bagi materi jadi bab/bagian (mis. Bagian 1, 2, 3).
2. Buat **notebook terpisah** untuk tiap bagian, unggah sumber yang sesuai.
3. Generate **Explainer** untuk masing-masing → download tiap klip.
4. Gabungkan klip dengan *video editor* gratis (lihat Bagian 7) menjadi 1 video panjang.

### Cara B – Kombinasi Audio Overview + Slide/Infografis
1. Generate **Audio Overview** (format podcast narasi panjang dari sumber).
2. Generate **Slide Deck** atau **Infographic** sebagai visual pendamping.
3. Rekam/impor audio ke editor video, pasang slide berganti sebagai visual → jadi video panjang bergaya presentasi.

### Cara C – Gunakan Tools Lain untuk Long-Form
Jika Anda butuh narasi panjang otomatis: buat naskah di NotebookLM Chat, lalu produksi video di tools seperti **Google Vids**, **Canva**, **HeyGen**, atau **Captions.ai** yang menerima teks/naskah panjang.

---

## 10. Bagian 7 – Ringkasan Tools Pendukung (untuk Long-Form)

| Tool | Fungsi | Gratis? | Platform |
|---|---|---|---|
| **CapCut** | Potong, gabung klip, tambah subtitle/musik | Ya (dengan watermark opsional) | Win/Mac/Android/iOS/Web |
| **Clipchamp** (bawaan Windows) | Edit & gabung video | Ya | Windows/Web |
| **Google Vids** | Buat video dari teks/naskah & slide | Termasuk Google Workspace | Web |
| **Canva Video** | Template video + narasi | Ada versi gratis | Web |
| **HeyGen / Captions.ai** | Video AI dari naskah panjang (avatar/voice) | Freemium | Web |
| **FFmpeg** (teknis) | Gabung banyak file video lewat perintah terminal | Ya (open source) | Win/Mac/Linux |
| **HandBrake** | Kompres ukuran file video hasil download | Ya (open source) | Win/Mac/Linux |

**Contoh perintah FFmpeg (gabung klip):** satukan daftar file `list.txt` lalu:
`ffmpeg -f concat -safe 0 -i list.txt -c copy gabungan.mp4`

---

## 11. Bagian 8 – Tips Praktis & Batasan Nyata

**Tips:**
- Semakin banyak & terstruktur sumber, video makin akurat. Gunakan ≥1 sumber berkualitas baik.
- Untuk bahasa Indonesia, **selalu pakai format Explainer** (Short & Cinematic hanya Inggris).
- Pakai **Steering Prompt** supaya video tidak terlalu umum ("Fokus ke 3 risiko utama").
- Nyalakan **Web notifications** agar tahu saat video selesai (bisa >30 menit).
- Cek "View custom prompt" (titik tiga pada artifact) untuk melihat prompt yang dipakai & merevisi.
- Video & visual **dihasilkan AI** → bisa ada ketidakakuratan/glitch audio. Selalu review sebelum publikasi.

**Batasan nyata:**
- Short & Cinematic: **Inggris + 18+** saja.
- Gaya Visual: **18+**, tidak untuk Cinematic & Short.
- Generate bisa **>30 menit**; tidak ada garansi durasi tetap.
- Tidak ada long-form native (butuh workaround Bagian 6).
- Link publik dinonaktifkan untuk akun Workspace Enterprise/Education.
- Hanya pemilik/editor notebook yang bisa menjadikan video publik.
- Video yang dihapus → tautan share ikut mati.
- Batas sumber: 50 untuk Free; per file 200 MB / 500.000 kata.

---

## 12. Checklist Cepat (One-Pager)

```
[ ] Punya Akun Google (18+ untuk fitur video penuh)
[ ] Buka notebooklm.google.com → Sign in
[ ] Create new notebook → Upload source (PDF/DOCX/URL/teks)
[ ] Panel Studio → klik "Video Overview"
[ ] Pilih Format:
      • SHORT  → "Short"  (Inggris, 18+)
      • LONG   → "Explainer" (bisa Indonesia) / "Cinematic" (Inggris)
[ ] Atur Language & Visual Style (Explainer) + Steering Prompt (opsional)
[ ] Klik Generate → tunggu (bisa >30 mnt, jalan di background)
[ ] Buka video → klik Download → file tersimpan di folder Download
[ ] (Long-form > beberapa mnt) Gabung klip dengan CapCut/Clipchamp (Bagian 6)
```

---

*SOP ini disusun berdasarkan dokumentasi resmi Google Support (Gemini Notebook / NotebookLM) per Juli 2026. Fitur AI dapat berubah; jika antarmuka berbeda, cari tombol "Studio" → "Video Overview".*
