# Agent Daemon Restart Protocol (VERIFIED 2026-08-11)

## Issue: Multi-instance ConflictError
```
telegram.error.Conflict: terminated by other getUpdates request; make sure that only one bot instance is running
```

## Root Cause
Multiple `python.exe agent.py` processes running simultaneously polling the same bot token.

## Fix Protocol (Windows)
```bash
# 1. Kill all python processes (clean slate)
tasklist /V /FI "IMAGENAME eq python.exe" | findstr /i agent
taskkill /F /PID <PID1> /PID <PID2> ...

# 2. Or kill ALL python processes if needed
taskkill /F /IM python.exe

# 3. Verify clean
tasklist /V /FI "IMAGENAME eq python.exe" | findstr /i agent
# Should return empty

# 4. Start fresh
cd /c/Users/arija/ziyan_agent
.venv/Scripts/python.exe agent.py > logs/agent.log 2>&1
```

## Verification Steps
1. Check log for startup sequence:
   - `ZIYAN Affiliate Agent Starting...`
   - `Instagram Business Account connected`
   - `YouTube connected`
   - `Scheduler started (check every 8 minutes)`
   - `Telegram bot started, polling...`
   - `getUpdates` returning 200 OK (no ConflictError)

2. Verify no ConflictError in logs:
   ```bash
   grep -i conflict logs/agent.log
   # Should return empty
   ```

## Prevention
- Use `BackgroundScheduler` (thread-based) not `AsyncIOScheduler`
- `telegram_bot.run()` manages own event loop with `run_polling(drop_pending_updates=True)`
- Always `taskkill` before deploy/restart in scripts/CI

## One-liner for Quick Restart
```bash
taskkill /F /IM python.exe 2>nul && cd /c/Users/arija/ziyan_agent && .venv/Scripts/python.exe agent.py > logs/agent.log 2>&1 &
```