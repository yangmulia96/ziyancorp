@echo off
title ZiyanCorp Auto E-Book Generator (Official 2026 Iconographic Blueprint)
color 0b
echo ========================================================
echo   ZIYANCORP MASTER E-BOOK GENERATOR (2026 EDITION)
echo   Format: Icon Vektor Tech, Diagram Arsitektur, & PDF HD
echo ========================================================
echo.
set /p TOPIC="Masukkan Judul / Topik E-Book yang Ingin Dibuat: "

if "%TOPIC%"=="" (
    echo [!] Judul tidak boleh kosong.
    pause
    exit /b
)

echo.
echo [*] Memulai proses pembuatan E-Book Otomatis...
python C:\Users\arija\ziyancorp\ebook_ai_creator\auto_ebook.py "%TOPIC%"

echo.
echo ========================================================
echo [OK] E-Book Selesai Dibuat & Diunggah ke Google Drive!
echo ========================================================
pause
