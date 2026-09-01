# Why ZIYAN social publishing uses scheduler.py, NOT n8n (verified 2026-08-08, n8n v2.33.4)

## Symptom
- Workflow imported via **manual SQLite insert** (`INSERT INTO workflow_entity ...`) appears in DB with `active=1`, but its Webhook node returns:
  `404 "The requested webhook POST xxx is not registered"` / `Cannot POST /webhook/xxx`.
- Restarting n8n does NOT fix it. n8n startup log shows `0 published workflows` / `Finished building workflow dependency index. Processed 0 draft workflows`.

## Root cause
n8n v2.33 **does not register webhooks from workflows inserted directly into the SQLite DB**. Webhook registration happens at activation time via the **REST API / editor toggle**, not from the raw DB row. A manual INSERT bypasses that registration path, so the webhook listener never mounts.

Also confirmed:
- `n8n import:workflow --input=file.json` failed with `SQLITE_CONSTRAINT: NOT NULL constraint failed: workflow_entity.id` when the JSON carried custom node `id` fields.
- `.env` for n8n config/API key must live in the **current working directory** (where `n8n start` runs, e.g. `C:\Users\arija\.env`), NOT in `.n8n/`. Putting it in `.n8n/.env` made `X-N8N-API-KEY` header required but unread → API 401/403.
- The running n8n instance uses a **different encryptionKey** than when old credentials were created → `Credentials could not be decrypted` on the old FB Sheet workflow.

## Decision
For ZIYAN Telegram→FB/YT publishing, we replaced n8n with **`C:\Users\arija\ziyan_intake\scheduler.py`**:
- Orion (Hermes) receives the file/text in the Telegram DM, saves it, generates the caption via 9router, and calls `scheduler.enqueue()`.
- `scheduler.py loop` posts 1 queued item every 77 minutes to FB (video/feed) + YT Shorts (if video). X is skipped per Boss rule.
- No webhook, no n8n dependency. Simpler and already verified working end-to-end (crop-top test posted to Celine Aurel FB + YT public).

## If you MUST use n8n anyway
- Create/activate the workflow via the **REST API** (`POST /api/v1/workflows` with `X-N8N-API-KEY`, then `POST /api/v1/workflows/{id}/activate`), never by editing SQLite directly.
- Put `N8N_API_KEY=...` in the **cwd `.env`** before `n8n start`.
- Re-create credentials inside the SAME n8n instance (matching encryptionKey) or they won't decrypt.
