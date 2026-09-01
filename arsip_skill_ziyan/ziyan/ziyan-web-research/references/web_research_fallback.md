# Web Research Fallback — Command Siap Pakai

## 1. DuckDuckGo HTML (sering gagal)
```bash
curl -s -m 8 -A "Mozilla/5.0" "https://html.duckduckgo.com/html/?q=QUERY"
# Sering return kosong saat diblokir → jangan andalkan
```

## 2. Langsung ke sumber otoritatif + r.jina.ai (PALING ANDAL)
```bash
curl -s -o /dev/null -w "%{http_code}" -m 8 -A "Mozilla/5.0" "URL"
curl -s -m 15 "https://r.jina.ai/URL" | head -40
```
Sumber carousel/AI marketing terbukti 200:
- https://buffer.com/resources/instagram-carousel/
- https://sproutsocial.com/insights/instagram-carousel/
- https://www.socialpilot.co/blog/linkedin-carousel
- https://influencermarketinghub.com/instagram-carousel-posts/
- https://later.com/blog/instagram-carousel-posts/
- https://blog.hootsuite.com/instagram-carousel-posts/

## 3. TikTok / YouTube metadata
```bash
curl -s -m 8 "https://www.tiktok.com/oembed?url=URL" | python3 -c "import sys,json;d=json.load(sys.stdin);print(d.get('title'),'|',d.get('author_name'))"
curl -s -m 8 "https://www.youtube.com/oembed?url=URL&format=json" | python3 -c "import sys,json;d=json.load(sys.stdin);print(d.get('title'))"
```

## 4. Sub-agent (delegate_task) GAGAL → ambil alih
Leaf agent sering return narasi tanpa URL. Cek: kalau tidak ada http valid → eksekusi curl di atas sendiri.

## 5. GitHub raw / API
```bash
curl -s -m 8 "https://raw.githubusercontent.com/USER/REPO/branch/path"
curl -s -m 10 "https://api.github.com/repos/USER/REPO/contents/folder"
```

## 6. 9Router combo (hanya Dashboard UI)
Dashboard localhost:20128 → tab Combo & Vision Adapter. CLI/API tidak support create.
