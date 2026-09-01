@echo off
echo =========================================
echo ZiyanCorp Omnichannel Distribution Runner
echo =========================================

echo [%date% %time%] Running Celine Aurel Distributor...
cd C:\Users\arija\ziyancorp\arsip_celine_aurel
C:\Python314\python.exe distribute_agent.py >> C:\Users\arija\ziyancorp\celine_cron.log 2>&1

echo [%date% %time%] Running Abangjal Distributor...
cd C:\Users\arija\ziyancorp\abangjal_archive_bot
C:\Python314\python.exe distribute_agent.py >> C:\Users\arija\ziyancorp\abangjal_cron.log 2>&1

echo [%date% %time%] Done!
