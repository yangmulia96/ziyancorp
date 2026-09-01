# Source endpoints & fetch recipes

All fetches run from a working dir under the Windows home (no /tmp on this host):
```
mkdir -p /c/Users/<user>/research && cd /c/Users/arija/research
```
Use a descriptive User-Agent for RSS; the Googlebot UA is the fallback for The Verge.

## Parallel fetch (issue as separate terminal calls in one turn)
```
# Google News RSS — swap query + locale; when:2d / when:7d for window
curl -s -m 30 -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) CompoundResearch/1.0" \
  "https://news.google.com/rss/search?q=AI+technology+when:2d&hl=en-US&gl=US&ceid=US:en" -o gn.xml

# Hacker News top story IDs
curl -s -m 30 -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) CompoundResearch/1.0" \
  "https://hacker-news.firebaseio.com/v0/topstories.json" -o hn_top.json

# Tech press RSS
curl -s -m 30 -A "..." "https://techcrunch.com/feed/" -o tc.xml
curl -s -m 30 -A "..." "https://theverge.com/rss/index.xml" -o vg.xml   # 0 bytes? retry with Googlebot UA
curl -s -m 30 -A "..." "https://arstechnica.com/feed/" -o at.xml

# Reddit (optional; often returns HTML error page)
curl -s -m 30 -A "..." "https://www.reddit.com/r/technology/hot.json?limit=25" -o reddit.json
```

## HN item loop (bash, after hn_top.json exists)
```
ids=$(python3 -c "import json;print(' '.join(str(x) for x in json.load(open('hn_top.json'))[:25]))")
for id in $ids; do curl -s -m 20 "https://hacker-news.firebaseio.com/v0/item/$id.json" -o "hn_$id.json"; done
```

## Parsing notes (Python, run from the working dir with WORK=".")
- Windows-native `python3` does NOT understand `/c/...` MSYS paths → use relative paths.
- RSS (ElementTree): iterate `item` (RSS 2.0) and `entry` (Atom); grab title, link, pubDate/updated.
- HN items: `json.load` each `hn_*.json`; **skip non-dict** (job/Ask items can differ); print
  title, score, descendants (comments), url — fallback to `https://news.ycombinator.com/item?id=<id>`.
- Google News item links are tracking URLs (`news.google.com/rss/articles/...`) — real and functional;
  keep them and cite the publisher name in text.
- Reddit: `json['data']['children']`; but guard — if the file starts with `<` it is an HTML error page;
  skip it and record under Catatan Sumber Gagal.
- Cross-outlet confirmation: count how many independent sources cover the same story = stronger viral signal.
