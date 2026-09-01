# Gmail Marketing Cleanup — Recipe & Real Numbers

## The search that works
Gmail over IMAP does NOT honor normal body/subject search for marketing detection. Tested live on 2026-08-14 against two real accounts:

| IMAP query | arizalkempo INBOX | mziyan266 INBOX | Note |
|---|---|---|---|
| `text unsubscribe` | 0 | 0 | ❌ IMAP body search broken/unreliable on Gmail |
| `X-GM-Raw "has:unsubscribe"` | 0 | 0 | ❌ only matches `List-Unsubscribe` header |
| `X-GM-Raw "unsubscribe"` | **9071** | **213** | ✅ catches link + body text |
| `X-GM-Raw "from:substack"` | 2 | — | useful for platform-specific |

**Rule:** use `X-GM-Raw "unsubscribe"` as the marketing detector. It over-counts slightly (some legit transactional mail contains the word) but since we move to Trash (reversible 30d), precision loss is acceptable.

## Move-to-Trash mechanics
Gmail IMAP has no real MOVE that strips INBOX cleanly without server quirks; the robust path is label manipulation:
```python
c.uid('STORE', ids, '+X-GM-LABELS', '(\\Trash)')
c.uid('STORE', ids, '-X-GM-LABELS', '(\\Inbox)')
```

## Performance
- Per-UID STORE loop on 9k + 213 messages **timed out at 600s foreground** and moved 0.
- Bulk STORE (join BATCH=500 UIDs with `,`, one STORE per batch) is the fix. Run in `terminal(background=true)`.

## Verification delta (do this after any run)
```python
import imaplib, ssl
for user,pw in ACCOUNTS.items():
    c=imaplib.IMAP4_SSL("imap.gmail.com",993,ssl_context=ssl.create_default_context())
    c.login(user,pw)
    c.select("INBOX"); print(user, "INBOX left:", len(c.search(None,'X-GM-Raw','unsubscribe')[1][0].split()))
    c.select("[Gmail]/Trash"); print(user, "Trash:", len(c.search(None,'X-GM-Raw','unsubscribe')[1][0].split()))
    c.logout()
```

## Safety
- NEVER `EXPUNGE` or `batch-delete` — Trash is user-recoverable for 30 days.
- Scope to INBOX; do not touch `Receipts`, `Client Email`, `FINANCE REPORT`, `Personal`, `Travel`, `URGENT`, `SUBSCRIBE` labels.
