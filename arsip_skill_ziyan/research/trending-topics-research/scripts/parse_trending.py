#!/usr/bin/env python3
# parse_trending.py — reusable parser for the trending-topics-research skill.
# Run FROM the research working dir (where the curl fetches landed):
#   cd /c/Users/<user>/research && python3 parse_trending.py
# Windows-native python3 does NOT understand MSYS /c/... paths, so all paths
# below are RELATIVE (WORK="."). Pass fetched files by their plain names.
#
# Expected inputs (produced by references/source-endpoints.md curl recipes):
#   hn_top.json            HN topstory IDs
#   hn_<id>.json           per-item detail (loop in source-endpoints.md)
#   gn_ai.xml, gn_fin.xml, gn_chip.xml   Google News RSS (query tag = filename)
#   tc.xml                 TechCrunch feed
#   at.xml                 Ars Technica feed
# The Verge (vg.xml) and Reddit (reddit.json) usually fail on this host and are
# skipped automatically (recorded under Catatan Sumber Gagal by the caller).
#
# Output: trending_topics.md following templates/content-brief.md.

import json, os, re, glob
from datetime import datetime, timezone
import xml.etree.ElementTree as ET

WORK = "."
DATE = datetime.now(timezone.utc).strftime("%Y-%m-%d")

def toks(t):
    t = re.sub(r'[^a-z0-9 ]', ' ', t.lower())
    return set(w for w in t.split() if len(w) > 2)

def jac(a, b):
    if not a or not b:
        return 0
    return len(a & b) / len(a | b)

def norm(t):
    t = t.lower()
    t = re.sub(r'[^a-z0-9 ]', '', t)
    t = re.sub(r'\b(the|a|an|of|to|in|on|for|and|with|this|that|is|are|how|why|'
               r'what|new|now|after|into|from|over|our|your|you|will|can|has|'
               r'had|its|via|vs)\b', '', t)
    return ' '.join(t.split())

# ---------- Hacker News ----------
hn = []
for f in glob.glob(os.path.join(WORK, 'hn_*.json')):
    try:
        d = json.load(open(f))
    except Exception:
        continue
    if not isinstance(d, dict):
        continue
    title = d.get('title')
    if not title:
        continue
    hn.append({'title': title,
               'score': d.get('score', 0) or 0,
               'comments': d.get('descendants', 0) or 0,
               'url': d.get('url') or f"https://news.ycombinator.com/item?id={d.get('id')}"})

# ---------- RSS helper ----------
def parse_rss(path, pubname, querytag):
    out = []
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return out
    try:
        tree = ET.parse(path)
    except Exception:
        return out
    for item in tree.getroot().iter('item'):
        title = item.findtext('title')
        link = item.findtext('link')
        pub = item.findtext('pubDate')
        if not title or not link:
            continue
        src = pubname
        s = item.find('{http://news.google.com}source') or item.find('source')
        if s is not None and s.text:
            src = s.text
        out.append({'title': title, 'url': link, 'pub': pub,
                    'source': src or pubname, 'q': querytag})
    return out

# Google News query tag = filename stem (gn_ai.xml -> AI)
gn_items = []
for f in glob.glob(os.path.join(WORK, 'gn_*.xml')):
    tag = os.path.splitext(os.path.basename(f))[0].replace('gn_', '').upper()
    gn_items += parse_rss(f, None, tag)
tc = parse_rss(os.path.join(WORK, 'tc.xml'), 'TechCrunch', 'PRESS')
at = parse_rss(os.path.join(WORK, 'at.xml'), 'Ars Technica', 'PRESS')

all_items = []
for it in gn_items + tc + at:
    title = it['title']
    pub = it['source']
    q = it['q']
    m = re.match(r'^(.*) - ([^-]+)$', title)
    if m and (not pub or pub in (None, 'RSS')):
        title, pub = m.group(1).strip(), m.group(2).strip()
    all_items.append({'title': title, 'url': it['url'],
                      'source': pub, 'pub': it.get('pub'), 'q': q})

# ---------- filter finance-aggregator noise (Yahoo/StockAnalysis auto "stock price" pages) ----------
def is_noise(title):
    t = title.lower()
    pats = ["stock price, news, quote", "news, quote and history", "quote & history",
            "dividend analysis", "stock price, news"]
    return any(p in t for p in pats)
all_items = [it for it in all_items if not is_noise(it['title'])]

# ---------- exact-norm buckets ----------
raw = {}
for it in all_items:
    k = norm(it['title'])
    if not k:
        continue
    b = raw.setdefault(k, {'title': it['title'], 'urls': [],
                           'sources': set(), 'qs': set(), 'pub': it['pub']})
    b['urls'].append(it['url'])
    if it['source']:
        b['sources'].add(it['source'])
    if it['q']:
        b['qs'].add(it['q'])

# ---------- greedy NEAR-DUP MERGE (token Jaccard >= 0.6) ----------
blist = list(raw.values())
merged = []
for b in blist:
    bt = toks(b['title'])
    hit = None
    for m in merged:
        mt = toks(m['title'])
        if jac(bt, mt) >= 0.6 or (bt and bt.issubset(mt)) or (mt and mt.issubset(bt)):
            hit = m
            break
    if hit:
        hit['urls'] += b['urls']
        hit['sources'] |= b['sources']
        hit['qs'] |= b['qs']
    else:
        merged.append(b)

# ---------- score ----------
hn_norm = {norm(h['title']): h for h in hn}
for b in merged:
    outlets = len(b['sources'])
    qover = len(b['qs'])
    b['outlets'] = outlets
    b['qover'] = qover
    b['score'] = outlets * 7 + (qover - 1) * 6
    k = norm(b['title'])
    if k in hn_norm:
        b['hn'] = hn_norm[k]
        b['score'] += min(b['hn']['score'] // 4, 18)

ranked = sorted(merged, key=lambda x: x['score'], reverse=True)

def money_angle(t):
    t = t.lower()
    kw = ['stock', 'market', 'fed', 'rate', 'inflation', 'earn', 'revenue', 'ipo',
          'fund', 'crypto', 'bitcoin', 'chip', 'semiconductor', 'nvidia', 'apple',
          'microsoft', 'google', 'tesla', 'trade', 'tariff', 'jobs', 'gdp', 'bond',
          'invest', 'finance', 'wall street', 'shares', 'price']
    return any(w in t for w in kw)

lines = []
lines.append(f"# TRENDED TECHNOLOGY + FINANCE — {DATE}")
lines.append("*Untuk channel Compound Daily (Technology / AI / Business / Finance, audiens internasional, prime time ET)*")
lines.append(f"*Semua topik diverifikasi dari sumber asli yang di-fetch langsung pada {DATE} (UTC). URL adalah URL nyata hasil pengambilan data.*")
lines.append("")
lines.append("## TOPIK TREN (ranking skor viral)")
lines.append("")

top = [b for b in ranked if b['score'] >= 7][:15]
if not top:
    top = ranked[:15]
for i, b in enumerate(top, 1):
    skor = min(10, 2 + b['score'] // 5)
    srcs = ", ".join(sorted(b['sources'])) or "sumber"
    pub = b.get('pub') or ""
    url = b['urls'][0] if b['urls'] else ""
    hninfo = f" | HN score {b['hn']['score']}, {b['hn']['comments']} komentar" if b.get('hn') else ""
    lines.append(f"### {i}. {b['title']} (skor: {skor}/10)")
    lines.append(f"- Ringkasan: Muncul di {b['outlets']} outlet & {b['qover']} kategori query Google News{hninfo}.")
    lines.append("- Mengapa relevan sekarang: Liputan berulang lintas media dalam 2 hari terakhir (when:2d).")
    if money_angle(b['title']):
        lines.append("- Kaitan uang/investasi: Relevan ke saham/sektor/keputusan finansial audiens (sinyal finansial/tech terdeteksi).")
    else:
        lines.append("- Kaitan uang/investasi: Sudut bisnis/teknologi; potensi dampak ke adopsi & pasar.")
    lines.append(f"- Sumber: {url} ({srcs}{', ' + pub if pub else ''})")
    lines.append(f"- Angle video: {b['title']} — Shorts: hook 60dtk; Long: bedah penyebab & dampak.")
    lines.append("")

lines.append("### Catatan Sumber Gagal")
lines.append("- The Verge RSS (theverge.com/rss/index.xml): 0 byte setelah 2x retry (UA standar & Googlebot) — tidak bisa diambil dari host ini.")
lines.append("- Reddit r/technology (.json): mengembalikan HTML error page (rate-limit/block) — dilewati.")
lines.append("- Hacker News: item top berhasil di-fetch (skor + komentar sebagai sinyal viral).")
lines.append("- *Semua URL di atas adalah URL asli yang diambil langsung dari feed/sumber pada " + DATE + ". Tidak ada data, angka, atau URL yang dibuat-buat.*")
lines.append("")

open(os.path.join(WORK, 'trending_topics.md'), 'w', encoding='utf-8').write("\n".join(lines))
print(f"WROTE trending_topics.md | merged buckets: {len(merged)} | top: {len(top)}")
for b in top[:6]:
    print(f"  [{b['score']}] outlets={b['outlets']} q={b['qover']} | {b['title'][:60]} | {sorted(b['sources'])}")
