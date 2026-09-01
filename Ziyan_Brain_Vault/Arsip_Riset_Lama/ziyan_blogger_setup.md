# Panduan Pasang Tema ZYN AI Corp (Gaya Gemini) di Blogger

Blog: https://ziyancorp.blogspot.com/
File tema: `ziyan_blogger_theme.css` (letakkan di `C:\Users\arija\`)

Tema ini murni CSS — **tanpa JavaScript**. Font Outfit, dark theme, luminous glow,
glassmorphism, gradient aurora bergerak, dan partikel background CSS-only.

---

## Cara A — Lewat Theme > Edit HTML (rekomendasi, full kontrol)

1. Buka **Blogger.com** → pilih blog **ZYN AI co**.
2. Klik menu **Tema (Theme)** di kiri.
3. Klik **Edit HTML** (tombol di kanan atas area pratinjau).
4. Di dalam editor, cari blok:
   ```
   <b:skin><![CDATA[
   ...
   ]]></b:skin>
   ```
5. **SIMPAN DHULU** tema lama (Copy seluruh isi editor → tempel ke Notepad sebagai backup).
6. Tempel **SELURUH isi `ziyan_blogger_theme.css`** tepat **SEBELUM** baris `]]></b:skin>`.
   (Jangan hapus `]]></b:skin>` dan jangan hapus `<b:skin><![CDATA[`.)
7. Cari tag `<body>` dan tambahkan **SATU baris** tepat setelahnya untuk layer partikel ke-2:
   ```xml
   <body>
   <div class='zyn-particles'></div>
   ```
8. Klik **Simpan (Save)**.

## Cara B — Lewat Customize > Advanced > Add CSS (paling mudah)

1. **Tema** → **Sesuaikan (Customize)** → **Lanjutan (Advanced)** → **Tambahkan CSS (Add CSS)**.
2. Tempel seluruh isi `ziyan_blogger_theme.css` ke kotak tersebut.
3. **Simpan**.
4. Untuk layer partikel ke-2 (`zyn-particles`), tetap perlu tambah `<div class='zyn-particles'></div>`
   setelah `<body>` lewat **Edit HTML** (langkah 7 Cara A). Jika dilewati, partikel tetap muncul
   (layer 1 via `body::after`), hanya kedalaman/parallax yang berkurang.

---

## Perbaikan SEO 1 — Meta Description (di `<head>`)

Buka **Edit HTML**, di dalam `<head>` (biasanya setelah
`<b:include data='blog' name='all-head-content'/>`), tempel:

```xml
<b:if cond='data:blog.metaDescription'>
  <meta expr:content='data:blog.metaDescription' name='description'/>
<b:else/>
  <meta content='ZYN AI Corp — perusahaan AI 100% agen. Blog resmi ZYN AI co: riset, produk, dan update agentik.' name='description'/>
</b:if>
```

`data:blog.metaDescription` otomatis diisi dari "Search description" tiap post/laman,
atau deskripsi blog di pengaturan. Fallback di `<b:else/>` menjamin selalu ada meta description.

---

## Perbaikan SEO 2 — H1 Otomatis untuk Post (pakai `<b:eval>`)

Buka **Edit HTML**, cari di widget **Blog** (`<b:widget type='Blog' ...>`) bagian
includable post yang memuat judul, biasanya berbentuk:

```xml
<h3 class='post-title entry-title'>
  <b:if cond='data:post.link'>
    <a expr:href='data:post.link'><data:post.title/></a>
  <b:else/>
    <b:if cond='data:post.url'>
      <a expr:href='data:post.url'><data:post.title/></a>
    <b:else/>
      <data:post.title/>
    </b:if>
  </b:if>
</h3>
```

Ganti **seluruh** blok `<h3 ...> ... </h3>` di atas dengan:

```xml
<b:if cond='data:post.title'>
  <b:if cond='data:blog.pageType == "item"'>
    <h1 class='post-title entry-title'>
      <b:if cond='data:post.link'>
        <a expr:href='data:post.link'><b:eval expr='data:post.title'/></a>
      <b:else/>
        <b:if cond='data:post.url'>
          <a expr:href='data:post.url'><b:eval expr='data:post.title'/></a>
        <b:else/>
          <b:eval expr='data:post.title'/>
        </b:if>
      </b:if>
    </h1>
  <b:else/>
    <h2 class='post-title entry-title'>
      <b:if cond='data:post.link'>
        <a expr:href='data:post.link'><b:eval expr='data:post.title'/></a>
      <b:else/>
        <b:if cond='data:post.url'>
          <a expr:href='data:post.url'><b:eval expr='data:post.title'/></a>
        <b:else/>
          <b:eval expr='data:post.title'/>
        </b:if>
      </b:if>
    </h2>
  </b:if>
</b:if>
```

Penjelasan:
- `<b:eval expr='data:post.title'/>` → render judul post secara aman (escape otomatis).
- H1 **hanya** di halaman artikel (`pageType == "item"`) → hindari banyak H1 di homepage (SEO lebih benar).
- Di homepage/arsip, judul jadi `<h2>` agar struktur heading rapi (H1 tetap milik judul blog).

> Catatan: Pastikan judul blog di Header widget memakai `<h1>` (default Blogger biasanya sudah).
> Jika belum, ubah `<p class='title'>`/`<h3>` di Header jadi `<h1>`.

---

## Set Meta Description per Post (wajib agar SEO aktif)

Setiap kali membuat/tombol post:
1. Di editor pos, klik ikon **⚙ Setelan (Post settings)** di kanan.
2. Isi **Search description** (≈ 150–160 karakter, mengandung kata kunci).
3. Publikasikan. Meta `<description>` di `<head>` akan otomatis terisi dari nilai ini.

---

## Tips & Troubleshooting

| Masalah | Solusi |
|---|---|
| Tema lama rusak setelah edit | Tempel kembali backup dari langkah 5, atau klik **Kembalikan (Revert)** di Edit HTML. |
| Font Outfit tidak muncul | Cek koneksi; `@import` butuh jaringan. Alternatif: tambah `<link>` di `<head>`: `<link href='https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap' rel='stylesheet'/>` |
| Partikel tidak terlihat | Pastikan `<div class='zyn-particles'></div>` ada setelah `<body>` (Cara A langkah 7). |
| Gerakan terlalu berat di HP | Sudah diatur `@media (max-width:600px)` turunkan opacity; plus `prefers-reduced-motion` mematikan animasi untuk pengguna yang mematikan gerakan. |
| Blogger tolak simpan | Pastikan tidak ada `]]>` tertinggal di dalam CSS selain penutup `<b:skin>`. |

---

## Catatan Keamanan

- Tema ini **hanya file**. Tidak ada perubahan otomatis ke akun Blogger Bos.
- Agent **tidak** memakai token OAuth / API untuk memasang tema. Semua dilakukan manual
  lewat UI Blogger oleh Bos.
- Token di `C:\Users\arija\ziyan_credentials\` **tidak digunakan** dan tidak dicetak di sini.
