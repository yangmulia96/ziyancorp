# Baca Dokumen Bos (PDF / DOC / JS)

## PDF
`pdftotext` ada di `C:\mingw64\bin\` (Git bash, bukan PowerShell).
```bash
pdftotext "C:\Users\arija\AppData\Local\hermes\cache\documents\doc_XXX.pdf" out.txt
head -100 out.txt
```

## DOC / JS / TXT
Langgsung `read_file` (text ASCII). `file` command cek tipe:
```bash
file "C:\path\to\file"
```

## JANGAN
- `execute_code` untuk baca file + urllib (diblokir policy "arbitrary local Python")
- Tulis script `.py` via `write_file` lalu `terminal python3 script.py`

## Contoh sesi (2026-08-08)
- `Ugc_ai` = JS source (React, 340 lines) → read_file langsung
- `Production_Roadmap.pdf` = 107KB → pdftotext → dapat 3 fase roadmap
- Gemini share link = r.jina.ai fetch (bukan login) → dapat warning/teks
