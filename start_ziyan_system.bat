@echo off
REM ========================================================
REM ZIYAN AUTOMATION SYSTEMS - MASTER BOT STARTER
REM Auto-launches: Celine Bot, AbangJal Bot, Scenic Wildlife Bot, Hermes Gateway
REM ========================================================

echo [1/4] Memulai Bot Celine Aurel...
cd /d C:\Users\arija\ziyancorp\arsip_celine_aurel
set PYTHONPATH=C:\Users\arija\ziyancorp\arsip_celine_aurel
start "" "C:\Users\arija\ziyancorp\arsip_celine_aurel\venv\Scripts\pythonw.exe" -m ziyan_bot.bot

ping 127.0.0.1 -n 2 >nul

echo [2/4] Memulai Bot AbangJal Arsip...
cd /d C:\Users\arija\ziyancorp\abangjal_archive_bot
set PYTHONPATH=C:\Users\arija\ziyancorp\abangjal_archive_bot
start "" "C:\Users\arija\ziyancorp\arsip_celine_aurel\venv\Scripts\pythonw.exe" -m abangjal_bot.bot

ping 127.0.0.1 -n 2 >nul

echo [3/4] Memulai Scenic Wildlife Bot...
cd /d C:\Users\arija\ziyancorp\scenic_wildlife_bot
start "" "C:\Python314\pythonw.exe" C:\Users\arija\ziyancorp\scenic_wildlife_bot\run_agent.py

ping 127.0.0.1 -n 2 >nul

echo [4/4] Memulai Hermes Gateway...
start "" "C:\Python314\pythonw.exe" C:\Users\arija\hermes_gateway_supervisor.py

echo [OK] Seluruh sistem ZiyanCorp aktif:
echo   - Bot Celine Aurel
echo   - Bot AbangJal Arsip
echo   - Scenic Wildlife Bot
echo   - Hermes Gateway (auto-restart)
