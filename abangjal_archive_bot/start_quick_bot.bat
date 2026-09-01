@echo off
cd /d C:\Users\arija\ziyancorp\abangjal_archive_bot
call venv\Scripts\activate.bat 2>nul || echo No venv, using system python
python quick_bot.py >> quick_bot.log 2>&1
