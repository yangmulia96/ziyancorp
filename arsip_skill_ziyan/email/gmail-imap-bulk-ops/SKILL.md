---
name: gmail-imap-bulk-ops
description: "Bulk move/clean Gmail emails via raw IMAP X-GM_Raw."
version: 1.0.0
author: ZIYAN Orchestrator
license: MIT
---

# Gmail Bulk Operations via IMAP (raw `imaplib`)

## When to use
- Mass-clean/purge an inbox (marketing, newsletters, promos) where web UI is impractical for 5k–40k messages.
- A tool reported "0 matches" from `text unsubscribe` / `body unsubscribe` — unreliable on Gmail IMAP.

## The reliable query: `X-GM_Raw`
Gmail IMAP exposes `X-GM_Raw`, same syntax as Gmail search box:
- `X-GM-Raw "unsubscribe"` → matches the word anywhere (body OR link). **Workhorse** — returns thousands.
- `X-GM-Raw "has:unsubscribe"` → only `List-Unsubscribe` header. Often **0** even when thousands qualify. Don't rely on it for cleanup.
- `X-GM-Raw "from:mailchimp"` → platform-specific, usually sparse.

```python
_, data = c.search(None, 'X-GM-Raw', 'unsubscribe')
uids = data[0].split()
```
`text unsubscribe` / `body unsubscribe` return **0** on Gmail — never use for counting/cleanup.

## Move (reversible) vs Delete (permanent)
ALWAYS move to Trash first (Gmail keeps 30 days, recoverable). Use labels, not flags:
```python
c.uid('STORE', ids, '+X-GM-LABELS', '(\\Trash)')
c.uid('STORE', ids, '-X-GM-LABELS', '(\\Inbox)')
```
Reversible. Only use `\\Deleted`+`EXPUNGE` if user explicitly wants permanent purge.

## Bulk pattern (critical for 10k+ inboxes)
Per-UID STORE round-trips too slowly (9k inbox exceeds 600s foreground). Batch:
- Join 300–500 UIDs with comma: `ids = b",".join(chunk)`.
- One STORE per batch (add Trash, remove Inbox).
- **Re-select INBOX every batch** — else connection drifts to AUTH state → `command SEARCH illegal in state AUTH`. Wrap re-select in try/except, reconnect if needed.
- Run script in **background** (`terminal(background=true, notify_on_complete=true)`). 9k cleanup takes minutes.

`UID MOVE` (RFC 6851) works but less robust than label STORE when Trash folder name differs per account.

## Verification (never trust self-reports)
Sub-agents often falsely report "completed / 0 results". After any run, verify with a real count:
```python
c.select("INBOX"); _, d = c.search(None, 'X-GM-Raw', 'unsubscribe'); inbox = len(d[0].split())
for name in ("[Gmail]/Trash", "Trash"):
    if c.select(name)[0] == "OK":
        _, d2 = c.search(None, 'X-GM-Raw', 'unsubscribe')
        trash = len(d2[0].split()) if d2 and d2[0] else 0
        print(f"INBOX sisa={inbox} | {name}={trash}")
        break
```
Gmail Trash may be named `Trash` (not `[Gmail]/Trash`) by locale — try both.

## Why not himalaya CLI?
himalaya v2.0.0 `gmail` backend requires OAuth2 bearer token; app password fails "Gmail config is missing." Raw `imaplib` + app password works immediately. Also: himalaya's bundled `config.toml` examples are v1.x and **do NOT parse on v2.0.0** (working v2 uses `[accounts.X.imap]` + `[accounts.X.imap.sasl.login]`). Flag the `himalaya` skill for adoption if you hit parse errors.

## App password
Gmail needs a 16-char App Password with 2FA on.

## Ready-to-run scripts (this session's artifacts)
- `C:\Users\arija\ziyancorp\scripts\cleanup_marketing.py` — bulk mover (set ACCOUNTS list, run in background).
- `C:\Users\arija\ziyancorp\scripts\verify_cleanup.py` — post-run INBOX-vs-Trash count.
If those paths are gone, reproduce from the patterns above (batch STORE + re-select + background run).
