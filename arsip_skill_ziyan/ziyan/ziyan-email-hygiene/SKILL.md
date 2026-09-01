---
name: ziyan-email-hygiene
description: Bulk Gmail cleanup via himalaya + IMAP on ZIYAN accounts.
version: 1.0.0
author: ZIYAN Orchestrator
license: MIT
---

# ZIYAN Email Hygiene (himalaya CLI)

## When to use
- Bulk-move/delete marketing/newsletter/unsubscribe emails from Bos's Gmail accounts.
- Any IMAP/SMTP operation on `arizalkempo@gmail.com` (alias `default`) or `mziyan266@gmail.com` (alias `mziyan266`).
- Setup/repair himalaya config on this Windows box.

## Accounts (verified live)
| Email | himalaya alias | INBOX |
|-------|---------------|-------|
| arizalkempo@gmail.com | `default` | massive (~41k, of which ~9k unsub) |
| mziyan266@gmail.com | `mziyan266` | ~460 |

## CRITICAL: himalaya v2.0.0 config format
Binary: `C:\Users\arija\AppData\Local\hermes\bin\himalaya.exe` (v2.0.0, prebuilt Windows x86_64).
Old v1 TOML (`imap.auth.mechanisms`, `backend.host`) is REJECTED. Correct v2 shape:
```toml
[accounts.default]
default = true
email = "arizalkempo@gmail.com"
display-name = "Ari Jal"

[accounts.default.imap]
server = "imap.gmail.com:993"

[accounts.default.imap.sasl.login]
username = "arizalkempo@gmail.com"
password.raw = "APP_PASSWORD"

[accounts.default.smtp]
server = "smtp.gmail.com:587"
starttls = true

[accounts.default.smtp.sasl.login]
username = "arizalkempo@gmail.com"
password.raw = "APP_PASSWORD"

[folder.aliases]
inbox = "INBOX"
sent = "[Gmail]/Sent Mail"
drafts = "[Gmail]/Drafts"
trash = "[Gmail]/Trash"
archive = "[Gmail]/All Mail"
spam = "[Gmail]/Spam"
```
Notes: v2 uses `imap.sasl.login` (not `imap.auth`), Gmail folder `[Gmail]/Trash` is the trash alias.
Backward `folder.aliases.X` (plural dotted) is required for Gmail save-to-sent.

## Commands (v2)
- List accounts: `himalaya account list`
- Mailboxes: `himalaya --account default mailbox list`  (NOT `folder list`)
- Envelopes: `himalaya --account default envelope list --mailbox INBOX`
- Move: `himalaya --account default message move <ID> <from> <to>` — but for Gmail bulk use **Python IMAP** (more reliable, see below).

## CRITICAL: detect marketing via X-GM-Raw, not text search
Plain `envelope search` / `text unsubscribe` returns **0** on Gmail (sub-agent burned 3 rounds on this).
Gmail supports raw query via IMAP `X-GM_Raw`:
```python
c.select("INBOX")
_, d = c.search(None, 'X-GM-Raw', 'unsubscribe')   # matches body+link, ~9000 hits
uids = d[0].split()
```
`has:unsubscribe` (header List-Unsubscribe) returns fewer; `X-GM-Raw "unsubscribe"` is the broad, accurate one.

## CRITICAL: move to Trash needs literal backslash escaping
`c.uid('STORE', ids, '+X-GM-LABELS', '(\\Trash)')` FAILS — Python string `'(\\Trash)'` is `(\Trash)` (single backslash → Gmail rejects "Label name not allowed").
The literal IMAP token Gmail wants is `(\Trash)` with ONE backslash. Use:
```python
BS = chr(92)                       # single backslash
trash_lbl = f"({BS}Trash)"
inbox_lbl = f"({BS}Inbox)"
c.uid('STORE', ids, '+X-GM-LABELS', trash_lbl)   # add Trash label
c.uid('STORE', ids, '-X-GM-LABELS', inbox_lbl)   # remove Inbox label
```
Do NOT use raw string `r'(\Trash)'` (that's two backslashes) nor `'(\\\\Trash)'` (four). Both fail.
Batch by 300-500 UIDs per command (bulk STORE one command per chunk, much faster than per-UID).
Re-`select("INBOX")` after each batch or state errors appear.

## Flow (proven 2026-08-15)
1. `python3 cleanup_marketing.py` (background, 600s+ timeout) — moves X-GM-Raw unsubscribe in INBOX → Trash.
2. Verify: re-select INBOX, count remaining; check `[Gmail]/Trash`.
3. Trash is reversible 30 days — safe. Never `expunge`/permanent delete.
4. Inflow: new subscription emails keep arriving (~30/min), so "remaining" never hits 0 — that's expected, not a failure.

## Gotchas
- Sub-agents on free models (laguna-s-2.1:free) hit 502 ECONNRESET mid-run — do the cleanup yourself in foreground/background, not via delegate.
- IMAP search over 41k mailbox is slow (20-60s per query) — be patient, don't assume failure.
- Gmail `X-GM-Raw` is IMAP-only; the `himalaya gmail messages list -q` subcommand needs OAuth2 (app password won't work there), so use raw IMAP Python, not the gmail subcommand.
