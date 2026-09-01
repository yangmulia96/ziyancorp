---
name: gmail-cli-management
description: Bulk-clean Gmail inboxes via himalaya v2 or IMAP.
version: 1.0.0
author: ZIYAN Orchestrator
license: MIT
platforms: [windows, linux, macos]
---

# Gmail CLI Management (himalaya v2.0.0 + raw IMAP)

## When to use
- User: "hapus email marketing", "bersihkan inbox", "pindah newsletter ke trash", "cari email dari X".
- `himalaya` installed but config throws `unknown field auth` / `unknown field port` / `unrecognized subcommand folder`.
- Need to verify email state (counts) programmatically, or move thousands of messages safely.

## Install himalaya v2.0.0 (Windows, no Rust toolchain)
The `himalaya` binary is often absent even when the skill exists. Download the prebuilt release:
```bash
curl -L -o himalaya.zip "https://github.com/pimalaya/himalaya/releases/download/v2.0.0/himalaya.x86_64-windows.zip"
unzip himalaya.zip   # binary at ./himalaya.exe (or ./result/bin/himalaya.exe)
```
Install to `C:\Users\arija\AppData\Local\hermes\bin\` and prepend to PATH each session:
```bash
export PATH="/c/Users/arija/AppData/Local/hermes/bin:$PATH"
himalaya --version   # expect: himalaya v2.0.0 ...
```

## CRITICAL: v2.0.0 config format (bundled himalaya skill is WRONG for v2.0.0)
The shipped skill + `references/configuration.md` show v1.x syntax (`imap.auth.mechanisms`, `imap.auth.password`, `backend.type="imap"`, `message.send.backend.*`). **All of that fails on v2.0.0** with `unknown field auth` / `unknown field port`. Use this instead (full file in `references/himalaya_v2_config.md`):

```toml
[accounts.default]
default = true
email = "you@gmail.com"
display-name = "Your Name"

[accounts.default.imap]
server = "imap.gmail.com:993"

[accounts.default.imap.sasl.login]
username = "you@gmail.com"
password.raw = "APP_PASSWORD"

[accounts.default.smtp]
server = "smtp.gmail.com:587"
starttls = true

[accounts.default.smtp.sasl.login]
username = "you@gmail.com"
password.raw = "APP_PASSWORD"
```

Key differences from v1.x:
- `starttls = true` is a **sibling key** under `[accounts.X.smtp]` — NOT `smtp.starttls = true`.
- SASL block is `[accounts.X.imap.sasl.login]` / `[accounts.X.smtp.sasl.login]` with `username` + `password.raw`.
- The `folder` subcommand was **RENAMED to `mailbox`** in v2.0.0 (`himalaya mailbox list`, NOT `folder list`).
- Gmail REST backend (`himalaya gmail ...`) requires an **OAuth2 bearer token** — an app password does NOT satisfy it and yields `Gmail config is missing for account`. Use the IMAP backend for password auth; only add `[accounts.X.gmail]` if you hold a real OAuth token.

## Accurate marketing detection (the most important finding)
Gmail IMAP search is counter-intuitive. On a real 2-account test:

| Query | Result | Verdict |
|-------|--------|---------|
| `text unsubscribe` (IMAP body) | 0 | ❌ misses everything |
| `X-GM-Raw "has:unsubscribe"` | 0 | ❌ too strict (needs `List-Unsubscribe` header) |
| `SUBJECT "unsubscribe"` | 0 | ❌ |
| `X-GM-Raw "unsubscribe"` | **9071 + 213** | ✅ accurate: catches body text + links |

**Always use `X-GM-Raw "unsubscribe"`** — it maps to Gmail's native search and catches the bulk of newsletters/marketing. Scope to `INBOX` only (select INBOX before search) so business/personal labels (Receipts, Client Email, FINANCE REPORT, etc.) are untouched.

## Bulk move to Trash (reversible 30 days — NEVER expunge)
Gmail IMAP "move" = add `\Trash` label + remove `\Inbox` label. **Bulk STORE one command per batch of UIDs** (join UIDs with comma) — per-UID STORE is ~hundreds of times slower and **times out** on large inboxes (a 41k-message inbox killed a 600s foreground run before moving anything).

```python
ids = b",".join(uids[i:i+BATCH])          # BATCH = 500
c.uid('STORE', ids, '+X-GM-LABELS', '(\\Trash)')
c.uid('STORE', ids, '-X-GM-LABELS', '(\\Inbox)')
```

Full working script: `scripts/cleanup_marketing.py` (dry-run by default; set `MOVE=True` to act). Run in **background** (`terminal(background=true, notify_on_complete=true)`) for inboxes >1k messages.

## Verify after action (don't trust self-reports)
Sub-agents return `status=completed` even on 502 errors without moving a single message. Always re-verify:
```bash
himalaya --account default mailbox list        # confirm Trash present
```
Or re-run the `X-GM-Raw "unsubscribe"` count on `INBOX` vs `[Gmail]/Trash` via Python to confirm the delta.

## Pitfalls
- Bundled `himalaya` skill (v1.x config) is **outdated for v2.0.0** → recommend `hermes curator adopt himalaya` to fix upstream; use this skill's config meanwhile.
- IMAP from the Windows sandbox env is slow; large batch ops MUST run in background.
- Never `expunge` / permanently delete — Trash is reversible for 30 days. Restore = move back from Trash to Inbox.
