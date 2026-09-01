#!/usr/bin/env python3
"""Bulk-move Gmail marketing emails to Trash via IMAP X-GM_Raw.

Scope : INBOX only (business/personal labels untouched).
Detect: X-GM-Raw "unsubscribe"  (accurate for Gmail bulk/newsletter mail).
Action : add \\Trash label + remove \\Inbox label  (reversible 30 days).
Bulk   : one STORE per BATCH of UIDs (per-UID STORE times out on big inboxes).

Default is DRY-RUN (count only). Set MOVE=True to actually move.
Run in background for inboxes > 1k messages.
"""
import imaplib, ssl, time

ACCOUNTS = {
    "arizalkempo@gmail.com": "REPLACE_APP_PASSWORD_1",
    "mziyan266@gmail.com":  "REPLACE_APP_PASSWORD_2",
}
IMAP_HOST = "imap.gmail.com"
BATCH = 500
MOVE = False  # set True to move to Trash


def connect(user, pw):
    ctx = ssl.create_default_context()
    c = imaplib.IMAP4_SSL(IMAP_HOST, 993, ssl_context=ctx)
    c.login(user, pw)
    return c


def process(user, pw):
    c = connect(user, pw)
    c.select("INBOX")
    typ, data = c.search(None, 'X-GM-Raw', 'unsubscribe')
    if typ != "OK":
        print(f"  [{user}] SEARCH gagal: {data}", flush=True)
        c.logout()
        return
    uids = data[0].split()
    total = len(uids)
    print(f"  [{user}] total match INBOX = {total}", flush=True)
    if not MOVE:
        c.logout()
        return
    done = 0
    for i in range(0, total, BATCH):
        chunk = uids[i:i + BATCH]
        ids = b",".join(chunk)
        try:
            c.uid('STORE', ids, '+X-GM-LABELS', '(\\Trash)')
            c.uid('STORE', ids, '-X-GM-LABELS', '(\\Inbox)')
            done += len(chunk)
            print(f"    ...{done}/{total} -> Trash", flush=True)
        except Exception as e:
            print(f"    BATCH ERR: {e}", flush=True)
            time.sleep(3)
    c.logout()
    print(f"  [{user}] SELESAI: {done} dipindah ke Trash.", flush=True)


if __name__ == "__main__":
    print("MODE:", "MOVE->Trash" if MOVE else "DRY-RUN (count only)", flush=True)
    for u, p in ACCOUNTS.items():
        print(f"\n=== {u} ===", flush=True)
        process(u, p)
    print("\nSELESAI.", flush=True)
