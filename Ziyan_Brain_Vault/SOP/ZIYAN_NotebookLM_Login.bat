@echo off
REM ZIYAN - NotebookLM Re-Login (NOVA auth fix) - PAKAI VENV HERMES
REM Double-click file ini, lalu login di browser yang muncul.
cd /d C:\Users\arija
SET VIRTUAL_ENV=C:\Users\arija\AppData\Local\hermes\hermes-agent\venv
CALL "%VIRTUAL_ENV%\Scripts\activate.bat"
echo Menyiapkan login NotebookLM (venv Hermes)...
python -m notebooklm login --fresh
echo.
echo Setelah login sukses di browser, tutup jendela.
echo Lalu cek: python -m notebooklm list
pause
