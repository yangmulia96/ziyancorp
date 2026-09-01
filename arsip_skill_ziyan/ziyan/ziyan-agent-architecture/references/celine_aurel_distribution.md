# Celine Aurel Multi-Platform Distribution — Verified Operating Notes

Applies to: `C:\Users\arija\ziyancorp\ziyan_archive_bot\` (bot `@Zynarsipbot`, code `8684088993`).
Status verified 2026-08-15/16: **5/5 platforms LIVE** — Telegram Channel `-1004373452633`, FB Page `975723622288353`, Instagram `@celineaurel99` (`IG_BUSINESS_ID=17841444876830769`), YouTube Celine Aurel Official (`UC0h3xyafx6P6J_CjpzhpSeg`, `token_celine.json`), Threads `@celineaurel99`.

## THREADS PUBLISHING — CORRECT APPROACH (key fix)

Manus AI corrected a critical mistake: **Threads direct publishing needs a THREADS USER TOKEN, NOT a Facebook Page/Graph token.** Linking the Threads account to the FB Page is only required for Meta Business Suite cross-posting, NOT for the direct Threads API.

- Threads App ID/Secret live in the Meta App "n8n" dashboard -> **Threads** section (separate from FB App ID/Secret). `threads_app_id=1346767533487099`.
- Token source: Meta App -> Use cases -> Threads -> **User Token Generator** -> pick `@celineaurel99` -> "Generate Access..." -> copy long-lived token. (OAuth redirect flow also works but the dashboard generator is simpler and avoids the "redirect URI not whitelisted" error.)
- Exchange: `POST graph.threads.com/oauth/access_token` with `grant_type=th_exchange_token` + Threads App Secret (server-side only).
- Validate: `GET graph.threads.com/v1.0/me?fields=id,username` -> must return `celineaurel99`.
- Publish TEXT: `POST /{threads-user-id}/threads` (`media_type=TEXT`, `text`) -> `POST /{threads-user-id}/threads_publish` (`creation_id`).
- Token short ~1h, long ~60 days; long-lived refreshable via `/refresh_access_token`. Expired tokens cannot be re-exchanged — need re-auth.
- Store in vault `threads_user_token.gpg`; `distributor.py` reads `THREADS_USER_TOKEN` env (priority).

## ANTI-DETECTION PRIME-TIME SCHEDULER

Boss requirement: post automatically 4x/day at slightly-off-prime times, 1 product per slot, flexible volume (some days many, some none).

- Slots (WIB): **08:57, 13:03, 16:24, 20:29** (not round hours -> avoids bot pattern).
- Implemented with `application.job_queue.run_daily(scheduled_post, time(h,m,tzinfo=ZoneInfo("Asia/Jakarta")))` in `ziyan_bot/bot.py`.
- `post_one_pending()` in `distributor.py`: reads `PRODUCT_MASTER!A2:K`, filters `status=="PENDING"`, takes 1, generates caption, posts to all 5 platforms, then `mark_published()` updates cols I (timestamp) + J (status->PUBLISHED).
- If no PENDING -> skip silently.

## UPLOAD BATCH / LINK-FOLLOWS FIX

Boss uploads media then sends the affiliate link separately (or together). Original bug: `finalize_batch` discarded files if no caption/link present at the 120s window.

Fix: if `session.draft is None` at finalize, **reschedule 60s up to 3x** (don't drop files). Link sent within ~3 min still gets merged into the same product. `UploadSession` gained a `retry: int = 0` field.
Batch window `.env` `BATCH_WINDOW_SECONDS=120`.

## 3-AGENT GITHUB BRIDGE (cross-agent comms)

Boss runs 3 agents: **Hermes** (Orkestrator), **Manus AI** (technical solver), **Antigravity/Google** (reader/executor). Shared memory = GitHub repo **`ziyancorp/ZIYAN_BRIDGE`** (PRIVATE).

- `SHARED_MEMORY.md` = log of inter-agent conversation, format `[Hermes -> Manus]`, `[Manus -> Hermes]`, etc.
- `projects/completed|active|blocked|archive/<project>/HISTORY.md` = per-project archive (Boss explicitly wants structured folders, not one flat file).
- `README.md` = bridge usage + security rules.
- Flow: agent writes update -> `git push` -> other agent `git pull` -> replies in same file.
- **SECURITY RULE (enforced after 15/8 incident):** never write secrets/tokens into `SHARED_MEMORY.md`, chat, or any GitHub file. Use `[VAULT: name.gpg]` reference only. Vault = `C:\Users\arija\.hermes\vault\*.gpg`, decrypt `bash bin/token_vault.sh get <n>`. Repo must stay PRIVATE. (Incident: App Secret was pasted into the public bridge -> fixed by removing it + setting repo private + rotating the secret in Meta dashboard.)
- Boss's GitHub username is `ziyancorp` (changed from `yangmulia96` ~15/8; old name 404s). `gh` CLI logged in as `yangmulia96` can still access `ziyancorp/*`.

## VERIFY-DON'T-TRUST (cross-agent)

Boss hates agents claiming "100% done" without API verification. In this session an agent claimed Threads "100% working" but the token was invalid (190) and Threads wasn't linked to the Page. Always test the live API before reporting success. Hermes verifies; agents that skip verification get corrected in the bridge.
