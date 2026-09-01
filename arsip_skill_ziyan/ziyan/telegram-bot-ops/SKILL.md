---
name: telegram-bot-ops
description: "Telegram bot ops: Conflict, 404, whitelist, OAuth, 9Router."
---

# Telegram Bot Ops (deploy + troubleshoot)

Covers the recurring failure modes when a python-telegram-bot process talks to Google
Drive/Sheets or 9Router. Patterns below are cross-cutting; see `references/` for deep dives.

## 1. Single-instance guard (avoid getUpdates Conflict)
**Symptom:** `telegram.error.Conflict: terminated by other getUpdates request; make sure that only one bot instance is running`
**Cause:** more than one process polling the same bot token (stale background proc, manual double-start, or a prior terminal(background) not killed).
**Fix:** kill every matching python proc, then start exactly one:
```powershell
powershell -NoProfile -Command "Get-CimInstance Win32_Process -Filter \"Name='python.exe' AND CommandLine LIKE '%ziyan_bot.bot%'\" | ForEach-Object { taskkill /PID \$_.ProcessId /F }"
```
> PITFALL (shell false-positive): searching LIKE '%ziyan_bot.bot%' WITHOUT Name='python.exe' also matches the shell that runs the search (its own command line contains the string). Always filter by Name='python.exe' or you will see phantom '4 bots' that are just your grep/shell chain.
> Verify with: (Get-CimInstance ...).Count — expect 1 after a clean start.

## 2. Whitelist = OWNER USER ID, not BOT ID
`TELEGRAM_ALLOWED_USER_IDS` must hold the OWNER's Telegram user ID (e.g. 7349146540).
The bot token prefix (e.g. 8684088993:AA...) is the BOT ID — putting it in the whitelist makes the bot reject every real message ("Akses ditolak").
Find the real ID: have the owner send any message, log update.effective_user.id in reject_if_unauthorized, read the bot's stdout.

## 3. Channel admin membership gotcha (404) — [CORRECTED 2026-08-15]
**Symptom:** `getChat` / `sendMessage` / `getChatAdministrators` to a channel returns `{"ok":false,"error_code":404,"description":"Not Found"}` even with the correct `-100...` ID and the bot shown in the Admin list (screenshot proves it).

**ROOT CAUSE (verified):** A raw `curl` call to the Bot API returns 404, BUT the same bot posting via `python-telegram-bot`'s `context.bot.send_message(chat_id=..., text=...)` SUCCEEDS (tested live 2026-08-15: bot replied in channel, log `sendMessage HTTP/1.1 200 OK`). The library carries an auth/session context that a bare `curl` from the shell does NOT replicate. Do NOT trust `curl` 404 as proof the bot lacks access.

**FIX (definitive):**
- **Always post to the channel from inside the bot process** using `context.bot.send_message(chat_id=CHANNEL_ID, text=caption)` — never shell `curl`.
- For distribution, call the Telegram send from the handler (bot object), not from a `requests.post` helper.
- To read the real channel ID: log `update.effective_chat.id` when the bot receives any message (including channel posts) — `CHAT_DEBUG type=channel id=-1004373452633 title=Celine Aurel arsip` confirmed the ID this way.
- **Do NOT loop on `curl` 404** — it is a false negative. If the bot can receive updates from the channel (forward_origin logged, or channel post received), membership is fine; just use the bot object to send.

**Anti-loop note:** If you see the same 404 from `curl` 3+ times, STOP curling. The bug is the curl call, not the channel. Switch to the bot object immediately.

> In a channel, `update.effective_user` is None (poster read as channel itself), so an auth check based on user ID falsely rejects. Bypass `reject_if_unauthorized` for `chat.type == "channel"` and for distribution commands (only the owner knows product IDs).

## 3b. Forward vs copy (diagnostic)
When the owner says "I sent a message to the channel", distinguish:
- **Forward** (Diteruskan dari ...) → bot receives it in PM with `forward_origin` (MessageOriginChannel). Logged as `FORWARD_ORIGIN chat_id=-100...`.
- **Typing in channel** → bot receives it in-channel (`chat.type == "channel"`). Logged as `CHAT_DEBUG type=channel id=-100...`.
Asking the owner to "forward to PM" when they already typed in-channel wastes turns. Just log `effective_chat.id` and read it.

## 4. Google Drive writes: SA quota 0 -> use OAuth user
**Symptom:** upload fails 403 storageQuotaExceeded — "Service Accounts do not have storage quota."
**Cause:** a Service Account uploading to a personal Drive folder hits the SA's own (zero) quota, even if the folder is shared to the SA with edit rights.
**Fix:** OAuth user flow -> token.json. GoogleWorkspace auto-detects token.json and prefers it over the SA key if present.
Steps: create an OAuth Desktop client in Google Cloud -> download client_secret.json -> run the auth script with GOOGLE_CREDENTIALS_FILE=client_secret.json -> owner opens the printed URL, logs in, allows -> token.json written.
> PITFALL: if the OAuth consent screen is "restricted to test users", the token exchange fails with invalid_grant unless the owner's email is added as a Test User (Google Cloud -> APIs & Services -> OAuth consent screen -> Test users).
> PITFALL: the localhost redirect must be opened from the same machine running the bot, or the auth code is never caught (use a manual code-exchange script as fallback — see references/google_oauth_drive.md).

## 5. 9Router auth + streaming
- POST http://127.0.0.1:20128/v1/chat/completions requires header Authorization: Bearer $HERMES_CUSTOM_9ROUTER_API_KEY (key from env, ~35 chars). Without it: {"error":{"message":"Missing API key"}}.
- 9Router returns SSE (data: {...} lines, ending data: [DONE]) even when you send "stream": false. Parse the stream: accumulate choices[0].delta.content from each data: line; do not call r.json() directly.
See references/9router_auth.md.

## 6. python-telegram-bot 22.x code pitfalls (caused real outages)
These crash the dispatcher or uploads silently — re-verify with a live send after any edit:

- **`filters.Caption` (class) vs `filters.CAPTION` (const).** Registering
  `MessageHandler(filters.PHOTO | filters.Document.ALL | filters.Caption, ...)` crashes the
  dispatcher with `TypeError: MessageFilter.check_update() missing 1 required positional
  argument: 'update'`. The bot then polls `getUpdates` 200 OK forever but NEVER dispatches
  (no handler runs, no error in normal log). ALWAYS use `filters.CAPTION`.
- **`googleapiclient` `drive.files().create()` rejects `timeout=` kwarg.** Unlike PTB/httpx,
  googleapiclient does not accept `timeout` on the execute call:
  `TypeError: Got an unexpected keyword argument 'timeout'`. Remove it; use
  `MediaFileUpload(..., resumable=False)` for files <25MB (reliable on flaky links).
- **`upload_file` needs a `Path`, not `str`.** `GoogleWorkspace.upload_file(path, ...)` does
  `path.name` / `str(path)` — passing the string from `LocalFile.path` raises
  `'str' has no attribute 'name'`. Wrap: `upload_file(Path(local_file.path), parent, name)`.

## 7. finalize must not depend on the Telegram network
`finalize_batch` runs from a job_queue callback. If it calls
`await context.bot.send_chat_action(chat_id, ChatAction.UPLOAD_DOCUMENT)` FIRST and the
Telegram connection is flaky, you get `telegram.error.NetworkError: httpx.ReadError` and the
ENTIRE archive (Drive + Sheet write) aborts — files lost from the session.
FIX: do the archive (`archive_new_product` / `add_files`) FIRST, then send the reply as
best-effort wrapped in try/except so a Telegram failure never blocks the archive.
Also: apscheduler may log the job "missed by 5:33" if the event loop was starved — the job
still runs on the next tick, so don't assume silence = success; always check Drive/Sheet.

## 8. Verify handlers WITHOUT sending from Telegram
`bot{BT}/sendPhoto` via requests/curl sends FROM the bot TO the user (outgoing) — it does
NOT simulate the user sending to the bot, so the bot never receives it (getUpdates stays `[]`).
To prove handler logic end-to-end offline, drive `process_update` directly (see
`references/archive_bot_debugging.md` for the full recipe):
```python
app = build_application(cfg, arc, db)
await app.initialize(); await app.start()
with patch.object(telegram.ext.ExtBot, 'get_file', fake_get_file), \
     patch.object(File, 'download_to_drive', fake_download_to_drive):
    await app.process_update(Update.de_json(fake_incoming_update, app.bot))
await asyncio.sleep(BATCH_WINDOW_SECONDS + 5)   # let the finalize job run
await app.stop()
# then read PRODUCT_MASTER to confirm the row landed
```

## 9. Pushing bot code to GitHub — secret hygiene
Before `git add .` on a bot repo, confirm `.gitignore` excludes `client_secret.json`,
`token.json`, `token_celine.json`, `.env`, `credentials.json`. `client_secret.json` is NOT
excluded by default here and WILL leak the Google OAuth client secret to a public remote.
Also exclude `yt_user_data/` (Chrome profile leftovers from the YouTube uploader) and
`bot_debug.log`. Verify with `git add -n . | grep -iE "client_secret|token|credentials|\.env"`
→ expect only `.env.example` (template), nothing real.

See `references/archive_bot_debugging.md` for the offline `process_update` verification recipe and the live-bot checks (orphan-instance, Sheet confirmation).

## Environment notes (not skills, just state)
- On Windows the bot venv must run with env -u PYTHONPATH so the global Hermes venv does not leak requests/cryptography into the bot's isolated venv.
- Start the bot headless: cd <botdir> && env -u PYTHONPATH GOOGLE_CREDENTIALS_FILE=client_secret.json HERMES_CUSTOM_9ROUTER_API_KEY="$HERMES_CUSTOM_9ROUTER_API_KEY" ./venv/Scripts/python.exe -m ziyan_bot.bot
