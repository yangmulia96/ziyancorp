---
name: gmail-imap-bulk-cleanup
description: "Bulk Gmail cleanup via IMAP X-GM-Raw when text search fails."
version: 1.0.0
author: HERMES
license: MIT
---

# Gmail Bulk Cleanup via IMAP

Standard IMAP `TEXT` / `BODY` / `SUBJECT` searches against Gmail **return 0 or
near-0** for things like "unsubscribe" — Gmail does not index IMAP text search
reliably and throttles it. Use the **`X-GM-Raw`** extension with Gmail's native
search syntax instead. This finds what the user actually means.

## When to use
- User: "hapus semua email marketing", "bersihkan newsletter", "move promotions to trash"
- himalaya `envelope search unsubscribe` returns 0 (it does — the syntax is wrong for Gmail)
- Any bulk Gmail triage where keyword/folder scan is insufficient

## The search (X-GM-Raw)
```python
_, d = c.search(None, 'X-GM-Raw', 'unsubscribe')        # text/link unsubscribe — accurate, thousands
_, d = c.search(None, 'X-GM-Raw', 'has:unsubscribe')     # List-Unsubscribe header only — often 0
_, d = c.search(None, 'X-GM-Raw', 'from:mailchimp')      # platform-specific
_, d = c.search(None, 'X-GM-Raw', 'category:promotions') # Promotions tab
```
Scope to INBOX only unless the user wants labels too. Never touch business/
personal folders (Receipts, Client Email, FINANCE REPORT) unless explicitly told.

## Move to Trash (reversible 30 days)
Gmail IMAP "move" = toggle labels. Add `\Trash`, remove `\Inbox`:
```python
import imaplib, ssl
BS = chr(92)                       # ONE backslash
TRASH = f"({BS}Trash)"             # => (\Trash)
INBOX = f"({BS}Inbox)"            # => (\Inbox)
c = imaplib.IMAP4_SSL("imap.gmail.com", 993, ssl_context=ssl.create_default_context())
c.login(user, app_password)
c.select("INBOX")
_, d = c.search(None, 'X-GM-Raw', 'unsubscribe')
uids = d[0].split()
for i in range(0, len(uids), 300):                 # batch 300
    ids = b",".join(uids[i:i+300])
    c.uid('STORE', ids, '+X-GM-LABELS', TRASH)
    c.uid('STORE', ids, '-X-GM-LABELS', INBOX)
```
Do NOT expunge. Restore = move Trash → INBOX.

## THE ESCAPING TRAP (cost me 4 failed runs)
- Failure modes seen:
  - `'(\\Trash)'` → Gmail: `BAD [Could not parse command]` (wrong byte count)
  - `'(\\\\Trash)'` (8 backslashes) → Gmail: `BAD [Could not parse command]` (too many)
  - **Correct:** build with `BS = chr(92)` then `f"({BS}Trash)"` → literal `(\Trash)` (exactly one backslash). Verified working.
- Always test with a 3-UID batch and confirm `OK` before a full run.

## Verification (do NOT trust self-reported "done")
After a run, re-query both counts. Gmail label ops are async-ish and new mail
keeps arriving, so INBOX count may not hit 0 in one pass — loop until stable.
```python
c.select("INBOX"); _, d = c.search(None, 'X-GM-Raw', 'unsubscribe'); inbox = len(d[0].split()) or 0
for name in ("[Gmail]/Trash", "Trash"):
    ok, d = c.select(name)
    if ok == "OK":
        _, d = c.search(None, 'X-GM-Raw', 'unsubscribe'); print(name, len(d[0].split()) or 0); break
```
If `search` raises `command SEARCH illegal in state AUTH`, the connection lost
its selected mailbox — re-`select("INBOX")` before searching again.

## Running it
- Use `imaplib` directly (Python) — more reliable than driving the `himalaya`
  CLI for bulk label ops across thousands of UIDs.
- Long runs (8k+ messages) exceed 600s foreground timeout → run with
  `terminal(background=true, notify_on_complete=true)` and verify after.
- App passwords, not regular passwords, for Gmail IMAP.

## himalaya notes (v2.0.0 binary)
If using the himalaya CLI: `folder` was renamed to `mailbox` in v2
(`himalaya mailbox list`). The bundled skill's config examples are v1.x and
will NOT parse on v2.0.0. For bulk label moves prefer raw `imaplib` above.
