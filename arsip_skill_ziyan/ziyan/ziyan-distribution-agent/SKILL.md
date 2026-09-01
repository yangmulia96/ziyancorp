---
name: ziyan-distribution-agent
description: Debug or build ZIYAN's YT/FB/IG/Threads post agent.
---

# ZIYAN Distribution Agent

Orchestrates posting ONE product (from `ARSIP_MASTER` Sheet / `AFFILIATE.json` in Drive) to **YouTube + Facebook + Instagram + Threads** in one run, all PUBLIC, with Bos's caption format (Shopee link + natural desc WITHOUT price + 4 hashtags).

## Communication Rule (Bos explicit, 16/8)
- Jawab SINGKAT, PADAT, JELAS. No warm-up, no theory without action.
- Tables > paragraphs. Copyable code/commands.
- Validate via API/terminal before claiming success. NEVER trust a sub-agent's self-report — re-check the endpoint.
- If stuck looping on a token error >2 tries, STOP and report exact blocker + what Bos must do in console. Don't spin.

## Architecture (distribute_agent.py + distributor.py)
- `distribute_agent.py`: reads latest product from Sheet, reads `AFFILIATE.json` from Drive, builds caption via 9Router, downloads real assets, calls `post_*` in `distributor.py`, marks PUBLISHED in Sheet.
- Tokens: ALL from vault (`bash /c/Users/arija/bin/token_vault.sh get <key>`) or `.env`. Never hardcode.
- Run isolated: `env -u PYTHONPATH ./venv/Scripts/python.exe distribute_agent.py` after exporting FB_PAGE_TOKEN / THREADS_USER_TOKEN / INSTAGRAM_USER_TOKEN.

## CRITICAL TOKEN/ENDPOINT GOTCHAS (verified 16/8)
Each platform has a DIFFERENT token source + endpoint. Mixing them = "Cannot parse access token" / "Insufficient Permission". Full table in `references/token-endpoints.md`.

| Platform | Token source | Endpoint | Notes |
|---|---|---|---|
| FB Page | `fb_page_token` (vault) | `graph.facebook.com` | Works |
| Threads | `THREADS_USER_TOKEN` (vault) | `graph.threads.net` | SEPARATE app (threads_app_id), NOT FB app. Text-only |
| IG | `INSTAGRAM_USER_TOKEN` (vault) | `graph.instagram.com` | NOT `graph.facebook.com`! Image via FB Page CDN first |
| YouTube | `token_celine.json` | youtube/v3 | Scope MUST include `youtube.upload` |

## IG image workaround
IG `image_url` must be a real image, not `drive.google.com/...` (HTML). Fix: download asset → `POST {fb_page_id}/photos` (published:false) → read `.source` CDN URL → use for IG `media`.

## YouTube scope failure
"If upload fails 'Insufficient Permission'": token scope lacks `youtube.upload`. Fix: delete `token_celine.json`, re-run `oauth_channel_check.py --expected-channel UC0h3xyafx6P6J_CjpzhpSeg` (opens browser, Bos authorizes). Saves new token with correct scope.

## Verify after posting (don't trust stdout)
- FB: `GET graph.facebook.com/{page_id}/feed?fields=id`
- Threads: `GET graph.threads.net/v1.0/me`
- IG: `GET graph.instagram.com/{ig_id}/media`
- YT: `GET youtube/v3/videos?part=status&id={id}`

## YouTube title length pitfall (verified 16/8, cost ~10 debug cycles)
YouTube **rejects video titles > 100 characters** with a MISLEADING error: `"The request metadata specifies an invalid or empty video title."` (reason `invalidTitle`). It does NOT say "too long". This also fires for empty/whitespace-only titles.
- Fix in `distribute_agent.py`: `yt_title = (prod.get("title") or f"Produk {pid}").strip()` then `if len(yt_title) > 95: yt_title = yt_title[:95].rsplit(" ",1)[0] + "..."`
- Symptom check: if `post_youtube_public` fails with `invalidTitle` but the same title works via manual CLI — you are almost certainly hitting the 100-char limit (the manual test used a shorter string). Reproduce with `subprocess.run([sys.executable,"youtube_upload_celine.py","--title",<title>,...])` to confirm.
- Also: the product `title` from Sheet often contains the price ("dengan harga Rp26.700") — strip it for YT description too (Bos rule: no price in captions). Use a simplified YT description, not the IG/Threads caption.

## GoogleWorkspace API quirk
`GoogleWorkspace` from `ziyan_bot.google_workspace` exposes a thin wrapper, NOT the raw `googleapiclient` Resource.
- `gw.drive.list_files(...)` / `gw.sheets.get_values(...)` → **AttributeError** ("'Resource' object has no attribute 'list_files'").
- Use the agent's own helpers instead: `get_products_latest()`, `get_affiliate_json(gw, pid)`, `download_asset(gw, drive_url, name)`. These are the supported entry points.
- `download_asset` ALWAYS writes to `tmp_assets/asset_video.mp4` (or `asset_photo.jpg`) regardless of the `name` arg you pass — do not assume the filename you gave.

## "Cannot parse access token" debugging ladder
When a Meta call returns `code 190 / Cannot parse access token`:
1. Check you're hitting the RIGHT endpoint for that token (see table above). FB token on Threads endpoint, or IG token on `graph.facebook.com`, both produce this.
2. Check the token is actually loaded — agent reads from `.env`/`INSTAGRAM_USER_TOKEN` etc.; if you `export` only `FB_PAGE_TOKEN` at runtime, the others fall back to `.env` (which may be empty/expired). `export` ALL four: `FB_PAGE_TOKEN`, `THREADS_USER_TOKEN`, `INSTAGRAM_USER_TOKEN`, `GOOGLE_CREDENTIALS_FILE`.
3. Test the token directly before blaming the code: `requests.get(endpoint/me, params={"access_token":tok})` → 200 = token good, code 190 = token bad/expired OR wrong endpoint.

## Cloning the project for a NEW brand (verified 17/8: ZIYAN → AbangJal)
Bos frequently spins up a sibling brand ("buat proyek distribusi abangjal"). Use this blueprint-copy pattern:
1. `mkdir abangjal_archive_bot`; copy `distribute_agent.py`, `distributor.py`, `youtube_upload_celine.py`, `run_distribute.sh`, `threads_reauth.py`, `.env.example`, `.gitignore`, `README.md`, `HISTORY.md` from `ziyan_archive_bot/`.
2. Copy the **bot package**: `cp ziyan_bot/{__init__,bot,archive,config,db,google_workspace,parser}.py abangjal_bot/` then `sed -i 's/ziyan_bot/abangjal_bot/g; s/ZIYAN/AbangJal/g; s/ziyan/abangjal/g' *.py`.
3. NEVER copy `.env`, `token*.json`, `client_secret.json`, `credentials.json` — those are per-brand secrets.
4. Test import: `<parent>/venv/Scripts/python.exe -c "import abangjal_bot.bot; import abangjal_bot.archive; print('OK')"`.
5. Bot token: Bos gives `<id>:<hash>` from @BotFather. Save `bash token_vault.sh set <brand>_bot_token "<tok>"` AND append `TELEGRAM_BOT_TOKEN=<tok>` to `.env`. Verify with `GET api.telegram.org/bot<tok>/getMe` (timeout 30s — Telegram API is slow from this host).
6. Bot still needs `GOOGLE_ROOT_FOLDER_ID` + `GOOGLE_SPREADSHEET_ID` in `.env` before it can archive. Without them `config.from_env()` raises RuntimeError — that's expected for a fresh blueprint, not a bug.
7. **Sheet tabs**: the bot crashes at startup (`Unable to parse range: <TAB>!1:1`) until PRODUCT_MASTER / CONTENT_ASSETS / PROCESS_LOG / ARSIP_MASTER exist with headers. Use the init recipe in `references/bot_intake_sheet_setup.md` (create folder + sheet + 4 tabs in one pass). This cost 3 bot-exit cycles on 17/8 — do it BEFORE first `python -m abangjal_bot.bot`.

## Cron: post ONLY pending, never repost
`distribute_agent.py` main() must call `get_pending_product()` (NOT `get_products_latest(limit=1)`). `get_pending_product()` scans `PRODUCT_MASTER!A2:J` reversed, returns first row whose column J != "PUBLISHED". After a successful run, `mark_published(pid)` writes `I{row}:J{row}` = `[timestamp, "PUBLISHED"]`.
- If you use `get_products_latest`, a 4x/day cron will repost the SAME newest product every run. That was the bug fixed 16/8.
- Wrapper `run_distribute.sh` exports FB_PAGE_TOKEN/THREADS_USER_TOKEN/INSTAGRAM_USER_TOKEN/GOOGLE_CREDENTIALS_FILE from vault so the cron session (which has no .env context) can run the agent.
- Cron create: `schedule="57 8,12,16,20 * * *"` (Bos's fixed slots 08:57/12:34/16:08/20:13). Deliver `origin`.

## Overlap note
Overlaps `ziyan-meta-distribution`, `ziyan-social-publisher` (user-owned). This captures the 16/8 working agent; merge if adopted.
