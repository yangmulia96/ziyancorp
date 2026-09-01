"""Petakan setiap token OAuth YouTube ZIYAN -> channel yang dikuasainya.

Jalankan SEBELUM upload apa pun, supaya video tidak mendarat di channel yang salah.

Cara pakai (cron-safe: write_file lalu terminal, JANGAN execute_code):
    cp <skill>/scripts/probe_youtube_tokens.py C:\\Users\\arija\\ziyan_pending\\_chk_channels.py
    python3 ziyan_pending/_chk_channels.py

Output per baris: <file token> -> <channelId> | <judul channel>
Ekspektasi Compound Daily = UCzWib2-2CPkWo315fzucaUw
"""
import json
import os
import urllib.parse
import urllib.request

CRED = r"C:\Users\arija\ziyan_credentials"
CLIENT = json.load(open(os.path.join(CRED, "youtube_desktop_client.json")))["installed"]

TOKENS = [
    "youtube_token_compound.json",
    "youtube_token_compounddaily_v1.json",
    "youtube_token_ziyanmalik.json",
    "youtube_token.json",
]


def access_token(tok_path):
    t = json.load(open(tok_path))
    data = urllib.parse.urlencode({
        "client_id": CLIENT["client_id"],
        "client_secret": CLIENT["client_secret"],
        "refresh_token": t["refresh_token"],
        "grant_type": "refresh_token",
    }).encode()
    new = json.loads(urllib.request.urlopen(urllib.request.Request(
        "https://oauth2.googleapis.com/token", data=data, method="POST")).read())
    return new["access_token"]


for fname in TOKENS:
    path = os.path.join(CRED, fname)
    if not os.path.exists(path):
        continue
    try:
        acc = access_token(path)
        req = urllib.request.Request(
            "https://www.googleapis.com/youtube/v3/channels?part=snippet&mine=true",
            headers={"Authorization": "Bearer " + acc})
        items = json.loads(urllib.request.urlopen(req).read()).get("items", [])
        for it in items:
            print(fname, "->", it["id"], "|", it["snippet"]["title"])
        if not items:
            print(fname, "-> NO CHANNEL")
    except Exception as e:  # token kedaluwarsa / dicabut / scope kurang
        print(fname, "-> ERR", str(e)[:200])
