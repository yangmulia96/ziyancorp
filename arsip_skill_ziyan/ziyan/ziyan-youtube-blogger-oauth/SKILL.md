---
name: ziyan-youtube-blogger-oauth
description: ZIYAN YouTube + Blogger OAuth autopost pipeline.
---

# ZIYAN YouTube + Blogger OAuth Publish Pipeline

ZIYAN company accounts: YouTube channel **"Compound Daily"** (UCzWib2-2CPkWo315fzucaUw, 0 subs / 5 videos) is the ACTIVE PRODUCTION channel — canonical token `ziyan_credentials/youtube_token_compounddaily_v1.json` (also valid: `youtube_token.json`, `youtube_token_compound.json` — all three resolve to Compound Daily via API). Secondary OLDER channel **"Ziyan Malik"** (UCend05oI081uEVPTNa934Bg, 61 subs / 15 videos) → token `youtube_token_ziyanmalik.json`. Blogger blog **"ZYN AI corp"** (`ziyancorp.blogspot.com`, Blog ID `598320500315317650`). All assets in `C:/Users/arija/ziyan_credentials/`.

## Architecture facts (verified this session)
- One OAuth **Desktop client** (`youtube_desktop_client.json`) serves BOTH YouTube + Blogger. Scopes requested together: `youtube.upload youtube.readonly blogger`.
- **Web client type REJECTS `urn:ietf:wg:oauth:2.0:oob`** ("must contain a domain"). Desktop client accepts `redirect_uri=http://localhost` — no server needed, user copies `code=` from the redirected `http://localhost?code=XXXX` (the localhost page erroring is NORMAL).
- Consent screen must be **"In production" + External** (not Testing) → otherwise Error 403 `access_denied` and refresh_token expires in 7 days. User cap 100 is fine for personal use.
- **Blogger API v3 is NOT auto-enabled.** After consent, call `GET https://www.googleapis.com/blogger/v3/users/self/blogs` → if `403 "Blogger API has not been used..."`, Bos must click Enable at `https://console.developers.google.com/apis/api/blogger.googleapis.com/overview?project=<PROJECT_ID>`. Enabling requires the Google account that OWNS the GCP project (mziyan266 got "You need additional access" because it didn't own `lofty-layout-504106-n4`).
- **Blogger API has NO `blogs.insert`** — blogs cannot be created via API. Bos creates the blog in Blogger.com UI once; agent only posts/edits/deletes/moderates afterward.
- A token's `access_token` expires hourly → always **refresh** with `refresh_token` before any call (POST to `https://oauth2.googleapis.com/token` grant_type=refresh_token). A raw 401 means expired access token, not bad credentials.

## Publish flow (YouTube)
- Upload via `yt-dlp` or `nb_proof/youtube_uploader.py` (both present). Token in `ziyan_credentials/youtube_token.json`.
- Verify channel: `GET youtube/v3/channels?part=snippet,statistics&mine=true` with Bearer access_token.

## Publish flow (Blogger)
1. Get Blog ID once: `GET blogger/v3/users/self/blogs` → save `id` to `ziyan_credentials/blog_zyn_id.txt`.
2. **Draft, not live:** POST to `blogger/v3/blogs/{id}/posts` with body `{"title":..., "content":..., "status":"DRAFT"}`. If you OMIT `status`, Blogger publishes LIVE immediately (this bit us once — always set DRAFT then let Bos review).
3. To publish later: `POST blogger/v3/blogs/{id}/posts/{postId}/publish`.
4. Agent can also update/delete/moderate comments/search — full editor role, not just poster.
5. **SEO gaps found:** Blogger rendered our markdown `#` as not-`<h1>` and added NO meta description. Agent should wrap title in `<h1>` and set the `description` field per post.

## Anti-NOV writing rule (AdSense safety)
Blog content MUST use ZIYAN's OWN experiment data (ZIYAN_COMPANY_LOG.md, ziyan_riset_*.md, models9r.json) — never generic "top 10 AI tools" rehash. Include explicit AI disclosure. Post ≤1/day. Full analysis: `ziyan_blogspot_adsense_riski.md`.

## Deploy preview to phone (Bos is often mobile)
Bos cannot open local HTML files on laptop. To let him view a demo: push HTML to `yangmulia96/zyn-aicorp-site` repo and enable GitHub Pages (`POST /repos/{owner}/{repo}/pages` source branch=main). URL: `https://yangmulia96.github.io/zyn-aicorp-site/`. Pages needs 1-2 min to propagate.

## Pitfalls
- Do NOT assume a token/file that appeared in disk was produced by THIS agent — cross-check with Bos (we once reported a channel as "connected" that Bos had actually set up via Hermes Desktop; that was a hallucination). Always state proof + source.
- `gemini/` channel on 9router is dead (400 invalid key); `ag/gemini-3.1-flash-image` works for IMAGE GENERATION only — no model in our 9router reads images.
- GitHub PAT lives in `ziyan_keys.env` (GITHUB_PAT) — read from disk, never ask Bos to paste it in chat. Push URL: `https://$PAT@github.com/yangmulia96/<repo>.git`.

## VERIFIED channel facts (2026-08-03 — corrected from earlier wrong doc)
- **Compound Daily** (UCzWib2-2CPkWo315fzucaUw) is the ACTIVE production channel. Canonical token: `ziyan_credentials/youtube_token_compounddaily_v1.json`. `youtube_token.json` and `youtube_token_compound.json` ALSO resolve to Compound Daily (verified via API — earlier doc wrongly said they mapped to Ziyan Malik).
- **Ziyan Malik** (UCend05oI081uEVPTNa934Bg, 61 subs) is a SECONDARY older channel → token `youtube_token_ziyanmalik.json`.
- Token `.json` files store ONLY `access_token` + `refresh_token` (NO `client_id`/`client_secret` in body). To refresh: read client creds from `ziyan_credentials/youtube_desktop_client.json` (`installed` type) and POST `client_id`+`client_secret`+`refresh_token`+`grant_type=refresh_token` to `https://oauth2.googleapis.com/token`. Verified working this session.
- ALWAYS verify the channel via `GET youtube/v3/channels?part=snippet,statistics&mine=true` with a freshly-refreshed access_token BEFORE uploading. Do not trust the filename — multiple token files point at Compound Daily, not Ziyan Malik.

## SECURITY
- Secrets (Telegram bot `8825875995:AAF...`, OpenAI `sk-or-v1-...`) were observed LEAKING into the shell environment — bash tried to execute them as commands. Keep secrets ONLY in `ziyan_keys.env` / dedicated files, never in a raw Windows User Env Var that gets shell-expanded. Rotate any token that ever appeared in a process list or command history.
