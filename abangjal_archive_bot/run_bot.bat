@echo off
setlocal
cd /d "%~dp0"

if not exist .env (
  echo File .env belum ada.
  exit /b 1
)

:loop
python -m abangjal_bot.bot
echo Bot Arijal berhenti. Menyalakan ulang dalam 5 detik...
timeout /t 5 /nobreak >nul
goto loop
