# 🚀 Arsip Eksperimen: NarasiKilat x Google Flow (Labs FX)

Dokumen ini menyimpan riwayat *workflow* pembuatan aset visual AI menggunakan **NarasiKilat Studio v5.0** yang dieksekusi langsung ke dalam **Google Flow (Labs FX)**.

## 📅 Detail Penyimpanan
- **Tanggal Eksekusi:** 30 Agustus 2026
- **Alur Kerja (Workflow):** NarasiKilat v5.0 (Teks/Prompt) $\rightarrow$ Google Flow (Image Node) $\rightarrow$ Google Flow (Video Node)

---

## 🔗 Aset Visual (Hasil Generasi)

### 🖼️ 1. Foto Referensi (Image Generation)
Hasil *generate* gambar statis beresolusi tinggi yang digunakan sebagai *frame* pertama / referensi awal di Google Flow.
* **Tautan Asli:** [Buka Foto di Google Labs](https://labs.google/fx/tools/flow/shared/image/313ae55c-abec-455a-a250-77b3201a17f6)

### 🎥 2. Hasil Video (Video Generation)
Hasil *generate* video animasi 10 detik yang digerakkan (*animated*) dari foto referensi di atas menggunakan node video di Google Flow.
* **Tautan Asli:** [Buka Video di Google Labs](https://labs.google/fx/tools/flow/shared/video/c661e143-46a1-431a-8c35-b43a651eac68)

---

## 📝 Format Prompt yang Digunakan

*(Diambil dari standar Prompt Foto 8K & Prompt Video NarasiKilat)*

### Prompt Foto (Katalog Model 8K)
> *"Professional fashion catalog portrait photo, 9:16 vertical. A beautiful Indonesian model wearing [Nama Produk], Standing Full Body Fashion Pose. High fashion editorial styling, authentic natural skin texture, realistic fabric folds and rich colors, Soft Warm Sunlight in [Lokasi Setting], shot on Hasselblad 85mm lens, f/1.8, 8k resolution, cinematic photorealistic masterpiece. --ar 9:16 --style raw"*

### Prompt Video (Omni Flash / Google Flow)
> *"UGC TikTok video recorded on iPhone 15 Pro, vertical 9:16, photorealistic. A gorgeous model wearing [Nama Produk] walking gracefully towards camera in [Lokasi Setting]. Realistic soft fabric and subject movement, smooth natural smile. Handheld tracking push-in shot, soft natural warm lighting, authentic creator aesthetic, crisp 4k 60fps."*

---
**Catatan Developer:** 
Kombinasi **NarasiKilat + Google Flow** memungkinkan produksi otomatis dari naskah jualan hingga video promosi utuh hanya dalam hitungan menit, tanpa harus merekam secara manual.
