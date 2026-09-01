# Bulk unsubscribe cleanup — proven script template

Place at `ziyancorp/scripts/cleanup_marketing.py`. Run in background (600s+).
Move (not delete) X-GM-Raw unsubscribe in INBOX → [Gmail]/Trash (reversible 30d).

```python
import imaplib, ssl, time
ACCOUNTS = [
    ("arizalkempo@gmail.com", "APP_PASSWORD_1"),
    ("mziyan266@gmail.com", "APP_PASSWORD_2"),
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
    c.select("INBOX")
    _, d = c.search(None, 'X-GM-Raw', 'unsubscribe')
    uids = d[0].split()
    total = len(uids)
    print(f"  [{u}] sisa INBOX unsub = {total}", flush=True)
    done = 0
    for i in range(0, total, BATCH):
        ids = b",".join(uids[i:i+BATCH])
        try:
            c.uid('STORE', ids, '+X-GM-LABELS', TRASH_LBL)
            c.uid('STORE', ids, '-X-GM-LABELS', INBOX_LBL)
            done += len(uids[i:i+BATCH])
            if done % 600 == 0 or done == total:
                print(f"    ...{done}/{total} -> Trash", flush=True)
        except Exception as e:
            print(f"    batch ERR: {e}", flush=True)
            time.sleep(3)
            try: c.select("INBOX")
            except Exception:
                c = connect(u, p); c.select("INBOX")
    c.logout()
    print(f"  [{u}] SELESAI: {done}/{total}", flush=True)

for u, p in ACCOUNTS:
    print(f"\n=== {u} ===", flush=True)
    run(u, p)
print("\nDONE", flush=True)
```

Verify (separate script) counts remaining in INBOX + Trash:
```python
import imaplib, ssl
for u,p in [("arizalkempo@gmail.com","P1"),("mziyan266@gmail.com","P2")]:
    c=imaplib.IMAP4_SSL("imap.gmail.com",993,ssl_context=ssl.create_default_context()); c.login(u,p)
    c.select("INBOX"); _,d=c.search(None,'X-GM-Raw','unsubscribe'); inbox=len(d[0].split()) if d[0] else 0
    for tn in ("[Gmail]/Trash","Trash"):
        ok,dd=c.select(tn)
        if ok=="OK":
            _,dd=c.search(None,'X-GM-Raw','unsubscribe'); trash=len(dd[0].split()) if dd[0] else 0
            print(f"{u}: INBOX sisa={inbox} | {tn}={trash}"); break
    c.logout()
```
