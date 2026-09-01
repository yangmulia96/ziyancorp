#!/usr/bin/env python3
# DPAPI cookie extractor for NotebookLM auth fallback (Windows/Hermes).
# Extracts Google/NotebookLM cookies from a CLOSED Brave/Chrome profile and
# writes Playwright storage_state.json format for notebooklm-py.
# NOTE: fails on Chrome 127+ App-Bound Encryption for SID/__Secure-1PSIDTS
#       (NotebookLM will still reject -> use interactive `login --fresh`).
import sqlite3, shutil, os, json, ctypes, ctypes.wintypes

BRAVE_COOKIES = r'C:\Users\arija\AppData\Local\BraveSoftware\Brave-Browser\User Data\Default\Network\Cookies'
OUT = os.path.expanduser(r'~\.notebooklm\profiles\default\storage_state.json')

def decrypt(blob):
    if not blob or blob[:3] not in (b'v10', b'v11'):
        return blob
    class BLOB(ctypes.Structure):
        _fields_ = [('cbData', ctypes.wintypes.DWORD),
                    ('pbData', ctypes.POINTER(ctypes.c_char))]
    cin = BLOB(len(blob), ctypes.cast(ctypes.create_string_buffer(blob, len(blob)),
                                      ctypes.POINTER(ctypes.c_char)))
    cout = BLOB()
    if ctypes.windll.crypt32.CryptUnprotectData(ctypes.byref(cin), None, None,
                                                 None, None, 0, ctypes.byref(cout)):
        buf = ctypes.create_string_buffer(cout.cbData)
        ctypes.memmove(buf, cout.pbData, cout.cbData)
        return buf.raw
    return b''

def main():
    tmp = r'C:\Users\arija\brave_cookies_tmp.db'
    shutil.copy2(BRAVE_COOKIES, tmp)
    con = sqlite3.connect(tmp)
    cur = con.cursor()
    cur.execute("SELECT name,value,host_key,path,expires_utc,is_secure,"
                "is_httponly,samesite FROM cookies "
                "WHERE host_key LIKE '%google%' OR host_key LIKE '%notebook%'")
    rows = cur.fetchall()
    con.close(); os.remove(tmp)
    out = {'cookies': []}
    for name, val, host, path, exp, sec, http, ss in rows:
        try:
            dec = decrypt(bytes(val))
            dec = dec.decode('utf-8', 'replace') if isinstance(dec, bytes) else dec
        except Exception:
            dec = ''
        out['cookies'].append({
            'name': name, 'value': dec, 'domain': host, 'path': path,
            'expires': (exp/10000000 - 11644473600) if exp else -1,
            'httpOnly': bool(http), 'secure': bool(sec),
            'sameSite': ['None', 'Lax', 'Strict'][ss] if ss in (0, 1, 2) else 'None'})
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w') as f:
        json.dump(out, f, indent=2)
    print(f'SAVED {len(out["cookies"])} cookies to {OUT}')

if __name__ == '__main__':
    main()
