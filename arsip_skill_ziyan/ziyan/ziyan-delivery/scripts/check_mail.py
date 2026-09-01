import imaplib, sys
from email import message_from_bytes
from email.header import decode_header

# Usage: python3 scripts/check_mail.py [list|read ID]
# Baca Gmail via imaplib pakai config himalaya (password sudah di disk, TIDAK print).
cfg = {}
for line in open('C:/Users/arija/.config/himalaya/config.toml', encoding='utf-8'):
    line = line.strip()
    if '=' in line and not line.startswith('#'):
        k, v = line.split('=', 1)
        cfg[k.strip()] = v.strip().strip('"')

user = cfg['imap.auth.username']
pw = cfg['imap.auth.password']

mail = imaplib.IMAP4_SSL('imap.gmail.com', 993)
mail.login(user, pw)
mail.select('INBOX')

mode = sys.argv[1] if len(sys.argv) > 1 else 'list'

if mode == 'list':
    typ, data = mail.search(None, 'ALL')
    recent = data[0].split()[-10:]
    for num in recent:
        typ, msg = mail.fetch(num, '(RFC822)')
        m = message_from_bytes(msg[0][1])
        frm = m.get('From', '')
        subj = m.get('Subject', '')
        try:
            subj = ''.join([t.decode(enc or 'utf-8') if isinstance(t, bytes) else t for t, enc in decode_header(subj)])
        except:
            pass
        print(f"ID {num.decode()}: {frm} | {subj}")
elif mode == 'read' and len(sys.argv) > 2:
    num = sys.argv[2].encode()
    typ, msg = mail.fetch(num, '(RFC822)')
    m = message_from_bytes(msg[0][1])
    if m.is_multipart():
        for part in m.walk():
            if part.get_content_type() == 'text/plain':
                print(part.get_payload(decode=True).decode('utf-8', errors='ignore')[:2000])
                break
    else:
        print(m.get_payload(decode=True).decode('utf-8', errors='ignore')[:2000])
mail.logout()
