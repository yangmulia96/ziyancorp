# Laporan Tema Blogger ZIYAN (XML)

**File tema:** `C:\Users\arija\ziyan_blogger_theme.xml`
**Sumber CSS:** `C:\Users\arija\ziyan_blogger_theme.css` (dibungkus di dalam `<b:skin><![CDATA[ ... ]]></b:skin>`)

## Cara import
1. Buka **Blogger** -> pilih blog ZYN AI co.
2. Masuk ke **Theme** (Tema) -> klik panah di sebelah tombol "Customize" -> pilih **Backup / Restore**.
3. Klik **Restore** (Pulihkan) -> pilih file `ziyan_blogger_theme.xml` -> **Upload**.
4. Tunggu hingga muncul konfirmasi "Your theme has been successfully imported".

## Validasi XML
- Parser: `python xml.dom.minidom.parse(file)`
- Hasil: **VALID** (tanpa SAXParseException)
- Tidak ada teks di luar tag; struktur diawali <?xml?> lalu <!DOCTYPE html> lalu <html>.

## Struktur yang dibuat
- `<?xml version="1.0" encoding="UTF-8" ?>` + `<!DOCTYPE html>` + `<html xmlns:b=...>`.
- `<head>`: meta viewport, `all-head-content`, **meta description otomatis** (`<b:if cond='data:blog.metaDescription'>`), `<title>`, dan `<b:skin>` berisi CSS penuh.
- `<body>`:
  - `<div class='zyn-particles'></div>` (layer partikel 2 - CSS pakai `.zyn-particles`; layer 1 pakai `body::after`).
  - Section **Header** -> widget `Header1` (type Header, h1 otomatis).
  - Section **Post** -> widget **`Blog1`** (type Blog) dengan includable `post` yang menampilkan **H1 otomatis** via `<b:eval expr='data:post.title'/>`, body artikel, dan pager.
  - Section **Sidebar** -> widget `HTML1` (type HTML).
  - Section **Footer** -> widget `HTML2` (type HTML).
- Namespace Blogger dideklarasikan (`xmlns:b`, `xmlns:data`, `xmlns:expr`) agar XML well-formed dan bisa diimpor.

## Catatan
- CSS tidak dimodifikasi; hanya dipastikan tidak ada urutan `]]>` di dalam CDATA (tidak ditemukan, jadi tidak diubah).
- File siap diimpor tanpa error "Content is not allowed in prolog" karena tidak ada teks di luar tag.
