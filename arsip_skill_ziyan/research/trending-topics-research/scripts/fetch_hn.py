#!/usr/bin/env python3
"""Parallel Hacker News item fetcher for the Compound Daily trending pipeline.

Run from the research working dir (where hn_top.json lives), e.g.:
    cd /c/Users/<user>/research
    python3 scripts/fetch_hn.py

Cron-safe: uses ThreadPoolExecutor instead of shell `&` (blocked in foreground
terminal) or xargs -I{} -P (mutually-exclusive flag warning on this host).
Writes hn_<id>.json for the top 25 stories next to hn_top.json.
"""
import json, os, sys, urllib.request, concurrent.futures

HERE = os.path.dirname(os.path.abspath(__file__))
for c in (os.getcwd(), HERE):
    p = os.path.join(c, "hn_top.json")
    if os.path.exists(p):
        TOP = p
        break
else:
    print("hn_top.json not found in cwd or script dir. Fetch topstories first.", file=sys.stderr)
    sys.exit(1)

with open(TOP) as f:
    ids = json.load(f)[:25]

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
OUTDIR = os.path.dirname(TOP)


def fetch(i):
    url = f"https://hacker-news.firebaseio.com/v0/item/{i}.json"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=20) as r:
            data = r.read()
        with open(os.path.join(OUTDIR, f"hn_{i}.json"), "wb") as o:
            o.write(data)
        return (i, len(data))
    except Exception as e:
        return (i, f"ERR:{e}")


with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
    res = list(ex.map(fetch, ids))

ok = [r for r in res if isinstance(r[1], int) and r[1] > 0]
bad = [r for r in res if not (isinstance(r[1], int) and r[1] > 0)]
print(f"fetched ok={len(ok)} bad={len(bad)}")
if bad:
    print("bad:", bad[:5])
print("total hn_*.json files:", len([f for f in os.listdir(OUTDIR) if f.startswith('hn_') and f.endswith('.json')]))
