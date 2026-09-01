import imaplib, ssl
ACCOUNTS = [
    ("arizalkempo@gmail.com", "sjeyujomwujoncrk"),
    ("mziyan266@gmail.com", "bknq zcej dcze pxyj"),
]
ctx = ssl.create_default_context()
for user, pw in ACCOUNTS:
    c = imaplib.IMAP4_SSL("imap.gmail.com", 993, ssl_context=ctx)
    c.login(user, pw)
    # INBOX remaining
    c.select("INBOX")
    _, d = c.search(None, 'X-GM-Raw', 'unsubscribe')
    inbox = len(d[0].split()) if d and d[0] else 0
    # Trash via both possible names
    for trash_name in ("[Gmail]/Trash", "Trash"):
        ok, d2 = c.select(trash_name)
        if ok == "OK":
            _, d2 = c.search(None, 'X-GM-Raw', 'unsubscribe')
            trash = len(d2[0].split()) if d2 and d2[0] else 0
            print(f"{user}: INBOX sisa={inbox} | {trash_name}={trash}")
            break
    else:
        print(f"{user}: INBOX sisa={inbox} | Trash gagal select")
    c.logout()
