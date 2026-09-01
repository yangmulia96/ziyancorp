import json, urllib.parse, urllib.request, sys, os
from pathlib import Path
from dotenv import load_dotenv, set_key

ROOT = Path(r"C:\Users\arija\ziyancorp\abangjal_archive_bot")
ENV_FILE = ROOT / ".env"

APP_ID = "1994676317847313"
APP_SECRET = "19f1b7a237e0d59243720435167c8f3f"
REDIRECT = "https://localhost:8123/"

def req(url, data=None):
    r = urllib.request.urlopen(urllib.request.Request(url, data=data, method="POST" if data else "GET"))
    return json.loads(r.read())

def get_user_token_from_code(code):
    url = f"https://graph.facebook.com/v21.0/oauth/access_token?client_id={APP_ID}&redirect_uri={urllib.parse.quote(REDIRECT)}&client_secret={APP_SECRET}&code={code}"
    d = req(url)
    short = d["access_token"]
    url2 = f"https://graph.facebook.com/v21.0/oauth/access_token?grant_type=fb_exchange_token&client_id={APP_ID}&client_secret={APP_SECRET}&fb_exchange_token={short}"
    d2 = req(url2)
    return d2.get("access_token", short)

def get_page_tokens(user_token):
    url = f"https://graph.facebook.com/v21.0/me/accounts?access_token={user_token}&fields=id,name,access_token,instagram_business_account{{id,username}}"
    d = req(url)
    return d.get("data", [])

def process_redirect_url(url_str):
    q = urllib.parse.urlparse(url_str).query
    code = urllib.parse.parse_qs(q).get("code", [None])[0]
    if not code:
        # maybe user pasted code directly
        code = url_str.strip()
    
    print(f"Exchanging code for Long-Lived Token...")
    ut = get_user_token_from_code(code)
    pages = get_page_tokens(ut)
    
    print("\n=== DAFTAR HALAMAN FACEBOOK & INSTAGRAM DITEMUKAN ===")
    selected_page = None
    for p in pages:
        pname = p.get("name", "")
        pid = p.get("id", "")
        ptoken = p.get("access_token", "")
        ig = p.get("instagram_business_account")
        ig_id = ig.get("id") if ig else "Belum Tertaut"
        ig_user = ig.get("username") if ig else "-"
        print(f"\n[Page] {pname} (ID: {pid})")
        print(f"  Token: {ptoken[:25]}...")
        print(f"  Instagram Biz ID: {ig_id} (@{ig_user})")
        
        # Priority match for Arijal
        if "Arijal" in pname or "Meutuwah" in pname or "Ziyan" in pname:
            selected_page = p
    
    if not selected_page and pages:
        selected_page = pages[0]
        
    if selected_page:
        print("\n=== MENYIMPAN KE .ENV ABANGJAL_ARCHIVE_BOT ===")
        # update .env
        set_key(str(ENV_FILE), "FB_PAGE_ID_ARIJAL", selected_page["id"])
        set_key(str(ENV_FILE), "FB_PAGE_TOKEN_ARIJAL", selected_page["access_token"])
        set_key(str(ENV_FILE), "META_USER_TOKEN_ARIJAL", ut)
        if selected_page.get("instagram_business_account"):
            ig = selected_page["instagram_business_account"]
            set_key(str(ENV_FILE), "IG_BUSINESS_ID_ARIJAL", ig["id"])
            set_key(str(ENV_FILE), "IG_USERNAME_ARIJAL", ig.get("username", ""))
            print(f"[SUKSES] Facebook Page & Instagram Arijal Meutuwah BERHASIL DISIMPAN!")
        else:
            print(f"[SUKSES] Facebook Page Arijal Meutuwah DISIMPAN (Instagram belum terdeteksi tertaut di API)")
    else:
        print("[PERINGATAN] Tidak ada Page yang ditemukan pada akun ini.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        process_redirect_url(sys.argv[1])
    else:
        perms = "pages_show_list,pages_read_engagement,pages_manage_posts,instagram_basic,instagram_content_publish,business_management"
        auth_url = f"https://www.facebook.com/v21.0/dialog/oauth?client_id={APP_ID}&redirect_uri={urllib.parse.quote(REDIRECT)}&scope={urllib.parse.quote(perms)}&response_type=code"
        print("=== LINK OTENTIKASI META (FB & IG ARIJAL MEUTUWAH) ===")
        print(auth_url)
