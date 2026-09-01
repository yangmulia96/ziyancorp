#!/usr/bin/env python3
# parse_trending_v2.py — CORRECTED parser for trending-topics-research.
# Drop-in replacement for the bundled parse_trending.py (which used
# hn_boost = min(score//4,18) SCALING — violating the skill's mandated
# flat +8 — and LACKED the niche-fit override). This v2 fixes both.
#
# Algorithm (verified 2026-08-16/17), MUST match skill mandate:
#  (1) read hn_top.json + hn_*.json, gn_*.xml (Google News), tc.xml, at.xml
#  (2) normalize title (lowercase, strip " - Publisher", strip punctuation), tokenize
#  (3) greedy-merge clusters via token Jaccard >= 0.6 OR subset
#  (4) score = outlets*7 + (queries-1)*6 + hn_boost
#  (5) hn_boost = FLAT +8 if any HN score present (NOT min(score//4,18))
#  (6) noise filter (ticker aggregators: "stock price, news, quote",
#      "dividend analysis", "quote & history")
#  (7) niche-fit override: pick highest-scored cluster matching channel
#      audience (Tech/AI/Business/Finance + money angle) -> NOT raw rank-1
# Writes trends.json + trending_topics.md into the dir it is run from.
import json, os, re, glob
from xml.etree import ElementTree as ET

OUT = os.path.dirname(os.path.abspath(__file__))

NOISE = ['stock price, news, quote', 'dividend analysis', 'quote & history', 'stock quote', 'price, news, quote']
FIT = {'ai','artificial','intelligence','machine','learning','llm','chatgpt','openai','google',
       'meta','apple','microsoft','amazon','nvidia','chip','semiconductor','tech','technology',
       'software','cloud','startup','silicon','data','cyber','security','science','crypto','bitcoin',
       'finance','financial','stock','stocks','market','markets','economy','fed','inflation',
       'earnings','invest','revenue','business','bank','trade','tariff','fund','venture','ipo'}

def is_noise(t):
    low = t.lower()
    return any(s in low for s in NOISE)

def norm(t):
    t = t.lower()
    t = re.sub(r'\s-\s[a-z0-9 .,&\'\"-]+$', '', t)
    t = re.sub(r'[^a-z0-9 ]', ' ', t)
    return re.sub(r'\s+', ' ', t).strip()

def toks(t):
    return set(norm(t).split())

def jac(a, b):
    if not a or not b:
        return 0
    u = len(a | b)
    return len(a & b) / u if u else 0

stories = []
hn_by_title = {}

try:
    hn_ids = json.load(open(os.path.join(OUT, 'hn_top.json')))
except Exception as e:
    print("HN top missing:", e); hn_ids = []
for fn in glob.glob(os.path.join(OUT, 'hn_*.json')):
    if fn.endswith('hn_top.json'):
        continue
    try:
        d = json.load(open(fn))
    except Exception:
        continue
    if not isinstance(d, dict):
        continue
    title = d.get('title')
    if not title:
        continue
    url = d.get('url') or f"https://news.ycombinator.com/item?id={d.get('id')}"
    stories.append({'title': title, 'url': url, 'source': 'Hacker News', 'query': 'hn'})
    hn_by_title[title] = max(hn_by_title.get(title, 0), d.get('score') or 0)

gn_files = [('gn_ai.xml','ai'),('gn_fin.xml','fin'),('gn_tech.xml','tech'),
            ('gn_stock.xml','stock'),('gn_semi.xml','semi'),('gn_semiconductor.xml','semi')]
for fn, q in gn_files:
    p = os.path.join(OUT, fn)
    if not os.path.exists(p):
        continue
    try:
        tree = ET.parse(p)
    except Exception as e:
        print("PARSE FAIL", fn, e); continue
    for item in tree.getroot().iter('item'):
        title = (item.findtext('title') or '').strip()
        link = (item.findtext('link') or '').strip()
        src = (item.findtext('source') or 'GoogleNews').strip()
        if not title or not link or is_noise(title):
            continue
        stories.append({'title': title, 'url': link, 'source': src, 'query': q})

for fn, q in [('tc.xml', 'tech'), ('at.xml', 'tech')]:
    p = os.path.join(OUT, fn)
    if not os.path.exists(p):
        continue
    try:
        tree = ET.parse(p)
    except Exception:
        continue
    for item in tree.getroot().iter('item'):
        title = (item.findtext('title') or '').strip()
        link = (item.findtext('link') or '').strip()
        if not title or not link or is_noise(title):
            continue
        stories.append({'title': title, 'url': link, 'source': q.upper(), 'query': q})

print(f"Raw stories collected: {len(stories)}")

clusters = []
for s in stories:
    tk = toks(s['title'])
    placed = False
    for c in clusters:
        if jac(tk, c['tok']) >= 0.6 or tk.issubset(c['tok']) or c['tok'].issubset(tk):
            c['titles'].append(s['title']); c['urls'].add(s['url'])
            c['sources'].add(s['source']); c['queries'].add(s['query'])
            if s['query'] == 'hn':
                c['hn'] = True
            placed = True
            break
    if not placed:
        clusters.append({'titles': [s['title']], 'urls': {s['url']},
                         'sources': {s['source']}, 'queries': {s['query']},
                         'hn': (s['query'] == 'hn'), 'tok': tk})

for c in clusters:
    outlets = len(c['sources'])
    queries = len(c['queries'])
    hn_boost = 8 if c['hn'] else 0
    c['score'] = outlets * 7 + (queries - 1) * 6 + hn_boost
    c['rep'] = max(c['titles'], key=len)
    c['fit'] = bool(c['tok'] & FIT)
    c['hn_score'] = max([hn_by_title.get(t, 0) for t in c['titles']], default=0)

clusters.sort(key=lambda c: c['score'], reverse=True)

primary = None
for c in clusters:
    if c['fit']:
        primary = c
        break
if primary is None:
    primary = clusters[0] if clusters else None

top = clusters[:15]
out = []
for i, c in enumerate(top, 1):
    out.append({'rank': i, 'title': c['rep'], 'score': c['score'],
                'outlets': sorted(c['sources']), 'queries': sorted(c['queries']),
                'hn_score': c['hn_score'], 'fit': c['fit'],
                'urls': sorted(c['urls'])[:4]})
primary_out = None
if primary:
    primary_out = {'title': primary['rep'], 'score': primary['score'],
                   'outlets': sorted(primary['sources']), 'queries': sorted(primary['queries']),
                   'hn_score': primary['hn_score'], 'urls': sorted(primary['urls'])[:4]}

result = {'primary_topic': primary_out, 'topics': out}
json.dump(result, open(os.path.join(OUT, 'trends.json'), 'w'), indent=2)

md = ["# Compound Daily - Trending Topics Brief\n"]
md.append("## Primary topic (niche-fit override)\n")
if primary_out:
    md.append(f"- **{primary_out['title']}**")
    md.append(f"  - Score: {primary_out['score']} | Outlets: {', '.join(primary_out['outlets'])} | HN score: {primary_out['hn_score']}")
    for u in primary_out['urls']:
        md.append(f"  - {u}")
md.append("\n## Top 15 ranked\n")
for t in out:
    tag = "FIT" if t['fit'] else "off-niche"
    md.append(f"{t['rank']}. [{tag}] {t['title']} - score {t['score']}, outlets {len(t['outlets'])} ({', '.join(t['outlets'][:4])}), HN {t['hn_score']}")
    for u in t['urls'][:2]:
        md.append(f"   - {u}")
open(os.path.join(OUT, 'trending_topics.md'), 'w').write("\n".join(md))
print("Primary:", primary_out['title'] if primary_out else None)
print("Clusters:", len(clusters))
