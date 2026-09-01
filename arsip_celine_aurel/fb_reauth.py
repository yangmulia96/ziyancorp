#!/usr/bin/env python3
"""FB Page re-auth: user login -> long-lived token -> page token.
Bos buka URL di HP, authorize, copy redirect URL (localhost) balik ke sini.
"""
import json, urllib.parse, urllib.request, sys, os

HOME = os.path.expanduser("~/OneDrive/ziyan_pending")
APP_ID = open(f"{HOME}/fb_app_id.txt").read().strip()
APP_SECRET = open(f"{HOME}/fb_app_secret.txt").read().strip()
REDIRECT = "https://localhost:8123/"

def req(url, data=None):
    r = urllib.request.urlopen(urllib.request.Request(url, data=data, method="POST" if data else "GET"))
    return json.loads(r.read())

def get_user_token_from_code(code):
    # exchange code -> short token
    url = f"https://graph.facebook.com/v19.0/oauth/access_token?client_id={APP_ID}&redirect_uri={urllib.parse.quote(REDIRECT)}&client_secret={APP_SECRET}&code={code}"
    d = req(url)
    short = d["access_token"]
    # extend to long-lived (60 days)
    url2 = f"https://graph.facebook.com/v19.0/oauth/access_token?grant_type=fb_exchange_token&client_id={APP_ID}&client_secret={APP_SECRET}&fb_exchange_token={short}"
    d2 = req(url2)
    return d2.get("access_token", short)

def get_page_token(user_token):
    url = f"https://graph.facebook.com/v19.0/me/accounts?access_token={user_token}&fields=id,name,access_token,instagram_business_account{{id,username}}"
    d = req(url)
    return d.get("data", [])

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1].startswith("http"):
        # Bos paste redirect URL
        q = urllib.parse.urlparse(sys.argv[1]).query
        code = urllib.parse.parse_qs(q).get("code", [None])[0]
        if not code:
            print("ERROR: gak ada 'code' di URL"); sys.exit(1)
        ut = get_user_token_from_code(code)
        pages = get_page_token(ut)
        print("=== PAGE TOKENS ===")
        for p in pages:
            print(f"Page: {p['name']} (id={p['id']})")
            print(f"  PAGE_TOKEN={p['access_token']}")
            if p.get("instagram_business_account"):
                ig = p["instagram_business_account"]
                print(f"  IG_BIZ_ID={ig['id']} IG_USERNAME={ig.get('username')}")
        # simpan user token (buat refresh IG/Threads)
        with open(f"{HOME}/fb_user_token_new.json", "w") as f:
            json.dump({"access_token": ut}, f)
        print("\nUser token disimpan ke fb_user_token_new.json")
    else:
        # print login URL
        perms = "pages_show_list,pages_read_engagement,pages_manage_posts,instagram_basic,instagram_content_publish,business_management"
        url = f"https://www.facebook.com/v19.0/dialog/oauth?client_id={APP_ID}&redirect_uri={urllib.parse.quote(REDIRECT)}&scope={urllib.parse.quote(perms)}&response_type=code"
        print("BUKA URL INI DI HP BOSS (Facebook app / browser):\n")
        print(url)
        print("\nSetelah authorize, copy URL di address bar (yang mulai https://localhost:8123/...) lalu jalankan:")
        print("python fb_reauth.py \"<URL redirect itu>\"")
