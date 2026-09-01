# Blogger API Upload — Verified Working (2026-08-03)

## Tokens / Credentials
- Token file: `C:\Users\arija\ziyan_credentials\youtube_token_ziyanmalik.json`
  - SUDAH punya scope `blogger` (lihat field `scope` di JSON).
  - TIDAK menyimpan `client_id` di dalamnya.
- Client file: `C:\Users\arija\ziyan_credentials\youtube_desktop_client.json`
  - `installed.client_id` = `789747689443-qk9ns1v1vigeinr20u9hibder54958l5.apps.googleusercontent.com`
  - Ini client yang cocok untuk refresh token di atas.
- Blog ID ZYN AI corp: `598320500315317650` (ziyancorp.blogspot.com)

## Refresh + List Blogs (test koneksi)
```python
import json, urllib.parse, urllib.request, os
base=r"C:\Users\arija\ziyan_credentials"
tok=json.load(open(os.path.join(base,"youtube_token_ziyanmalik.json")))
cli=json.load(open(os.path.join(base,"youtube_desktop_client.json")))["installed"]
data=urllib.parse.urlencode({"client_id":cli["client_id"],"client_secret":cli["client_secret"],
    "refresh_token":tok["refresh_token"],"grant_type":"refresh_token"}).encode()
resp=json.loads(urllib.request.urlopen(urllib.request.Request(
    "https://oauth2.googleapis.com/token", data=data,
    headers={"Content-Type":"application/x-www-form-urlencoded"}),timeout=20).read())
access=resp["access_token"]
r=urllib.request.urlopen(urllib.request.Request(
    "https://www.googleapis.com/blogger/v3/users/self/blogs",
    headers={"Authorization":f"Bearer {access}"}), timeout=20)
for b in json.loads(r.read()).get("items",[]):
    print(b["name"], b["id"])
```

## Upload Post (working snippet)
```python
import json, urllib.parse, urllib.request, os
base=r"C:\Users\arija\ziyan_credentials"
BLOG_ID="598320500315317650"
tok=json.load(open(os.path.join(base,"youtube_token_ziyanmalik.json")))
cli=json.load(open(os.path.join(base,"youtube_desktop_client.json")))["installed"]
# ... refresh access (same as above) ...
md = open(r"C:\Users\arija\ziyan_artifacts\ionq_skywater\blog_post_final.md", encoding="utf-8").read()
# PITFALL: jangan embed base64 image >~1MB, Blogger 400. Ganti ke URL eksternal:
md = md.replace("https://storage.googleapis.com/.../infographic.png",
                "https://i.ytimg.com/vi/4YognM-N-gM/maxresdefault.jpg")
post={"kind":"blogger#post",
      "title":"IonQ Completes Acquisition of SkyWater Technology: The Quantum Manufacturing Play Explained",
      "content":f"<div style='white-space:pre-wrap;font-family:system-ui,Arial,sans-serif;line-height:1.7'>{md}</div>"}
url=f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts?isDraft=false"
req=urllib.request.Request(url, data=json.dumps(post).encode(),
    headers={"Authorization":f"Bearer {access}","Content-Type":"application/json"}, method="POST")
r=urllib.request.urlopen(req, timeout=30)
out=json.loads(r.read())
print("POST_ID:", out.get("id"), "URL:", out.get("url"))
```

## Pitfalls
- 401 saat refresh: client_id mismatch (token dibuat dari client berbeda). Pakai `youtube_desktop_client.json` untuk token `ziyanmalik`.
- 400 saat POST: content terlalu besar (base64 image 6MB+) -> pakai URL eksternal.
- `isDraft=false` di query string -> langsung publish. Pakai `isDraft=true` kalau mau draft dulu.
- Blog ID salah -> cek via list blogs di atas.
