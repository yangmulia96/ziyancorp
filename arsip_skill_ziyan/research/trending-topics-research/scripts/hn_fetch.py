#!/usr/bin/env python3
# Fetch Hacker News topstories + each item via Python urllib.
# WHY: avoids the bash `while read` + `\r` line-ending trap that silently
# produces item/$id.json (0-byte, curl exit 3). Pure-Python = no \r issue.
import urllib.request, json, time, os

OUT = os.path.dirname(os.path.abspath(__file__))

def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode('utf-8')

base = "https://hacker-news.firebaseio.com/v0"
ids = json.loads(get(f"{base}/topstories.json"))[:25]
with open(os.path.join(OUT, "hn_top.json"), "w") as f:
    json.dump(ids, f)
ok = 0
for i in ids:
    try:
        d = get(f"{base}/item/{i}.json")
        with open(os.path.join(OUT, f"hn_{i}.json"), "w") as f:
            f.write(d)
        ok += 1
    except Exception as e:
        print("FAIL", i, e)
    time.sleep(0.15)
print(f"HN items fetched: {ok}/{len(ids)}")
