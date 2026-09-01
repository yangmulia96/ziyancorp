# Web Research Fallback — Working Recipe (verified 2 Aug 2026)

## Context
ZIYAN Fase 1 (RISA sub-agent) failed 2x:
- Run 1: `upstream server error (500)` on `gemma-4-26b` (transient, recovered).
- Run 2: `session storage could not be written` — Hermes session-DB write lock (NOT disk; 346GB free). Sub-agent crashed after `mkdir`, 0 files saved.

Parent (Nous) took over via `terminal` and harvested 10 sources in one shot.

## Blocked Search Engines (this host)
| Engine | Result |
|---|---|
| Google | captcha / empty (bot-blocked) |
| DuckDuckGo HTML | `000` timeout |
| Bing | HTTP 200 (~70-86KB) BUT result URLs JSON-encoded → regex `href` yields 0 |

## Working Method: Direct Source-Domain Fetch
Google/DuckDuckGo/Bing parsing all unreliable. Go straight to the source domain.

### Tested-good 200 domains (tech/finance/quantum)
- `ionq.com/news` ✅
- `thequantuminsider.com/?s=<query>` ✅
- `techcrunch.com`, `arstechnica.com` ✅
- `theverge.com` (needs Googlebot UA)
- `reuters.com`, `bloomberg.com` = 401 bot-blocked ❌

### Exact command pattern
```bash
cd /c/Users/arija/ziyan_notebooklm_sources/ionq_skywater
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
curl -s --max-time 30 -A "$UA" -L "https://www.ionq.com/news/ionq-completes-acquisition-of-skywater-technology" -o ionq_main.html -w "[%{http_code}] size=%{size_download}\n"
```

### Extract internal article links
```bash
python3 -c "
import re
html = open('ionq_news.html', encoding='utf-8', errors='replace').read()
links = re.findall(r'href=\"([^\"]+)\"', html)
abs_links = []
for l in links:
    if l.startswith('/'): l = 'https://www.ionq.com'+l
    if 'ionq.com' in l and any(k in l.lower() for k in ('skywater','acquisition','news')):
        abs_links.append(l)
seen=set(); uniq=[l for l in abs_links if l not in seen and not seen.add(l)]
print(len(uniq),'links')
"
```

## Result (IonQ x SkyWater 10 sources)
Folder: `C:\Users\arija\ziyan_notebooklm_sources\ionq_skywater\`
- ionq_acquisition_main.html (IonQ official)
- ionq_regulatory.html (IonQ official)
- qi_complete.html, qi_regulatory.html, qi_merger_agreement.html, qi_announce.html,
  qi_q1_rev.html, qi_ceo.html, qi_skywater_q4.html, qi_trapped_ion.html (Quantum Insider)

All HTTP 200, 90KB–260KB each. Ready for NOVA (NotebookLM ingest).

## Lesson
When Boss says "fase masih gagal ya?" → STOP re-dispatching, diagnose root cause from
live transcript, then Parent-takeover mechanical tasks in terminal. That IS the CEO move.
