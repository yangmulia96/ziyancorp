@echo off
setlocal
cd /d "%~dp0"

if not exist .env (
  echo File .env belum ada. Salin .env.example menjadi .env lalu isi secret.
  exit /b 1
)
if not exist .venv (
  py -3 -m venv .venv
  .venv\Scripts\python.exe -m pip install --upgrade pip
  .venv\Scripts\pip.exe install -r requirements.txt
)

:loop
.venv\Scripts\python.exe -m ziyan_bot.bot
echo Bot berhenti. Restart dalam 5 detik...
timeout /t 5 /nobreak >nul
goto loop
