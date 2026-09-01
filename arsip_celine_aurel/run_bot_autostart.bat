@echo off
cd /d C:\Users\arija\ziyancorp\arsip_celine_aurel

REM === Anti-orphan: kill semua instance bot lama dulu ===
for /f "tokens=2" %%p in ('tasklist /fi "imagename eq python.exe" /fo list ^| findstr /i "PID:"') do (
    for /f "tokens=*" %%c in ('tasklist /fi "pid eq %%p" /fo list ^| findstr /i "Command Line:"') do (
        echo %%c | findstr /i "ziyan_bot.bot" >nul && taskkill /pid %%p /f >nul 2>&1
    )
)

REM === Reset env biar gak bocor dari session lain ===
set PYTHONPATH=
set FB_PAGE_TOKEN=
set CHANNEL_CELINE=
set GOOGLE_CREDENTIALS_FILE=client_secret.json
set HERMES_CUSTOM_9ROUTER_API_KEY=

REM === Ambil FB_PAGE_TOKEN dari vault terenkripsi ===
for /f "delims=" %%t in ('bash C:\Users\arija\bin\token_vault.sh get fb_page_token 2^>nul ^| tr -d "\n"') do set "FB_PAGE_TOKEN=%%t"

REM === CHANNEL_CELINE (Celine Aurel) ===
set CHANNEL_CELINE=-1004373452633

REM === HERMES_CUSTOM_9ROUTER_API_KEY dari .env kalau ada ===
for /f "tokens=1,* delims==" %%a in ('findstr /i "HERMES_CUSTOM_9ROUTER_API_KEY" .env 2^>nul') do set "HERMES_CUSTOM_9ROUTER_API_KEY=%%b"

REM === Jalankan bot (1 instance bersih) ===
C:\Users\arija\ziyancorp\arsip_celine_aurel\venv\Scripts\python.exe -m ziyan_bot.bot
