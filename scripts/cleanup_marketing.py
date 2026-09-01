#!/usr/bin/env python3
"""Move sisa email marketing (X-GM-Raw unsubscribe) INBOX -> Trash.
Gmail: add \\Trash label + remove \\Inbox label. Re-select tiap batch agar state valid.
Trash reversible 30 hari.
"""
import imaplib, ssl, time
ACCOUNTS = [
    ("arizalkempo@gmail.com", "sjeyujomwujoncrk"),
    ("mziyan266@gmail.com", "bknq zcej dcze pxyj"),
]
BATCH = 300
BS = chr(92)
TRASH_LBL = f"({BS}Trash)"
INBOX_LBL = f"({BS}Inbox)"

def connect(u, p):
    ctx = ssl.create_default_context()
    c = imaplib.IMAP4_SSL("imap.gmail.com", 993, ssl_context=ctx)
    c.login(u, p)
    return c

def run(u, p):
    c = connect(u, p)
    ok, data = c.select("INBOX")
    if ok != "OK":
        print(f"  [{u}] select INBOX gagal: {data}", flush=True); c.logout(); return
    _, data = c.search(None, 'X-GM-Raw', 'unsubscribe')
    uids = data[0].split()
    total = len(uids)
    print(f"  [{u}] sisa INBOX unsub = {total}", flush=True)
    done = 0
    for i in range(0, total, BATCH):
        chunk = uids[i:i+BATCH]
        ids = b",".join(chunk)
        try:
            c.uid('STORE', ids, '+X-GM-LABELS', TRASH_LBL)
            c.uid('STORE', ids, '-X-GM-LABELS', INBOX_LBL)
            done += len(chunk)
            if done % 600 == 0 or done == total:
                print(f"    ...{done}/{total} -> Trash", flush=True)
        except Exception as e:
            print(f"    batch ERR ({len(chunk)}): {e}", flush=True)
            time.sleep(3)
            try:
                c.select("INBOX")
            except Exception:
                c = connect(u, p); c.select("INBOX")
    c.logout()
    print(f"  [{u}] SELESAI: {done}/{total}", flush=True)

if __name__ == "__main__":
    for u, p in ACCOUNTS:
        print(f"\n=== {u} ===", flush=True)
        run(u, p)
    print("\nDONE", flush=True)
