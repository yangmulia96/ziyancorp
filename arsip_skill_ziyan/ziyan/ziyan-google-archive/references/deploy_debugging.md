# Windows Process Debugging for Bot Deployment (ZIYAN)

Use PowerShell (`powershell -NoProfile -Command "..."`) from the agent terminal. git-bash `ps`/`grep` is unreliable for Windows process command lines.

## Count REAL bot instances (avoid false positives)
```powershell
Get-CimInstance Win32_Process -Filter "Name='python.exe' AND CommandLine LIKE '%ziyan_bot.bot%'" | Select-Object ProcessId | Format-Table
```
WRONG — also matches the agent's own shell commands containing the string:
```powershell
Get-CimInstance Win32_Process -Filter "CommandLine LIKE '%ziyan_bot.bot%'"
```

## Verify a PID's command line BEFORE killing
```powershell
Get-CimInstance Win32_Process -Filter "ProcessId=4180" | ForEach-Object { "PID=$($_.ProcessId) CMD=$($_.CommandLine)" }
```
A 250MB `python.exe` with "Unknown" window title can be 9router or the Hermes gateway — never kill on a guess.

## Kill all real bot instances
```powershell
Get-CimInstance Win32_Process -Filter "Name='python.exe' AND CommandLine LIKE '%ziyan_bot.bot%'" | ForEach-Object { taskkill /PID $_.ProcessId /F }
```

## Conflict diagnosis (Telegram "Conflict: terminated by other getUpdates request")
1. Kill all real bot instances (command above).
2. Wait ~3s, confirm count = 0.
3. Start exactly ONE instance:
   `cd ziyancorp/ziyan_archive_bot && env -u PYTHONPATH ./venv/Scripts/python.exe -m ziyan_bot.bot`
4. Verify log shows `Application started` + `getUpdates 200 OK` with NO `Conflict` and NO `REJECTED`.

## Critical rule
Verify every PID's `CommandLine` before `taskkill`. Guessing by RAM size or window title breaks infrastructure.
