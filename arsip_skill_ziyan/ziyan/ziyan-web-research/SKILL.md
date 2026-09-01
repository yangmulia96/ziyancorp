---
name: ziyan-web-research
description: Riset web ZIYAN bila search diblokir atau sub-agent gagal.
version: 1.0.0
author: ZIYAN Orchestrator
license: MIT
---

# ZIYAN Web Research (Fallback & Techniques)

## Kapan pakai skill ini
- `html.duckduckgo.com/html` return kosong (diblokir)
- Google/Reddit/Medium/YouTube scrape 403/404/CAPTCHA
- Sub-agent `delegate_task` (leaf) return "akan cari" tanpa URL valid
- Butuh ambil teks artikel berbayar/JS-heavy

## Pola Utama (PENTING)
1. **JANGAN andalkan sub-agent untuk pencarian mentah.** Leaf agent (`delegate_task`, model openrouter) TIDAK bisa jalankan web search mandiri — dia cuma bikin todo lalu return narasi kosong (`call:web_search{}` kosong, tanpa URL). Penyebab: `delegate_task` children tidak dikasih akses search tool yang berfungsi. SELALU verifikasi: kalau output tidak ada `http(s)://` valid → ambil alih sendiri dengan `terminal` + curl.
2. **Cara dispatch sub-agent yang BENAR untuk riset:** jangan suruh dia "cari di web". Alih-alih, **Orion yang jalankan pencarian** (DuckDuckGo lite / URL langsung + jina.ai), lalu **pass hasilnya sebagai context** ke sub-agent biar dia proses/synthesis. Sub-agent dipakai untuk analisis & penulisan, BUKAN pengumpulan sumber.
3. **Validasi output sub-agent:** cek ada `http(s)://` valid? Kalau tidak → buang, ambil alih. Jangan percaya "ringkasan" tanpa URL. (Bukti: RISA 2x gagal cari 10 URL — cuma todo; Orion ambil alih via DuckDuckGo+jina.)
4. **Sub-agent bisa halusinasi** kalau disuruh analisis tanpa konteks cukup (contoh: RISA bedah @ngoprek.ai keluar "NFT collectibles", "avatar AI coach" yang tidak ada di screenshot). Selalu kasih data mentah (screenshot/teks) di context, jangan suruh "riset mandiri".
2. **URL langsung + r.jina.ai** lebih andal dari search engine:
   ```bash
   curl -s -m 8 -A "Mozilla/5.0" "URL" -o /dev/null -w "%{http_code}"   # cek 200
   curl -s -m 15 "https://r.jina.ai/URL" | head -40                      # ambil teks
   ```
3. **Sumber otoritatif yang terbukti 200** (carousel/AI marketing):
   - https://buffer.com/resources/instagram-carousel/
   - https://sproutsocial.com/insights/instagram-carousel/
   - https://www.socialpilot.co/blog/linkedin-carousel
   - https://influencermarketinghub.com/instagram-carousel-posts/
   - https://later.com/blog/instagram-carousel-posts/
   - https://blog.hootsuite.com/instagram-carousel-posts/

## TikTok / YouTube metadata
```bash
curl -s -m 8 "https://www.tiktok.com/oembed?url=URL" | python3 -c "import sys,json;d=json.load(sys.stdin);print(d.get('title'),'|',d.get('author_name'))"
curl -s -m 8 "https://www.youtube.com/oembed?url=URL&format=json" | python3 -c "import sys,json;d=json.load(sys.stdin);print(d.get('title'))"
```
Transcript video: diblokir CAPTCHA → pakai oembed/description saja, jangan paksa.

## GitHub
```bash
curl -s -m 8 "https://raw.githubusercontent.com/USER/REPO/branch/path"
curl -s -m 10 "https://api.github.com/repos/USER/REPO/contents/folder"
```

## 9Router combo
- HANYA bisa dibuat via Dashboard UI (`localhost:20128` → tab Combo & Vision Adapter). Tidak lewat CLI/API (endpoint butuh auth).
- Simpan mapping model per agent di memory, jangan coba script create combo.

## 9Router Streaming Response (PENTING — terbukti 2026-08-08)
`curl .../v1/chat/completions` dengan model `kr/claude-sonnet-4.5` kadang balikin **SSE chunk**, BUKAN JSON utuh.
Stdout mulai `data: {"id":"chatcmpl-...","object":"chat.completion.chunk",...}`.
Parsing `json.load(stdin)` LANGSUNG GAGAL: `JSONDecodeError: Expecting value: line 1 column 1`.
**FIX:** SELALU decode sebagai SSE — lihat `references/9router_streaming.md`. Jangan pakai `json.load` langsung ke response 9Router.
Menambah `"stream": false` di body SERING diabaikan oleh proxy → tetap SSE. Decode manual lebih aman.

## 9Router Model Availability Test (cari yang jalan)
Model di list `/v1/models` (100+) mayoritas GAGAL/quota. Tes dulu sebelum pakai:
```bash
KEY="$HERMES_CUSTOM_9ROUTER_API_KEY"
for m in "kr/claude-sonnet-4.5" "gemini/gemini-3.5-flash-lite" "gc/gemini-3-pro-preview"; do
  echo "=== $m ==="
  curl -s -m 25 "http://localhost:20128/v1/chat/completions" -H "Content-Type: application/json" \
    -H "Authorization: Bearer $KEY" \
    -d "{\"model\":\"$m\",\"messages\":[{\"role\":\"user\",\"content\":\"halo\"}],\"stream\":false}" | head -c 120
done
```
Stabil gratis (terbukti 2026-08-08): `kr/claude-sonnet-4.5`, `kr/claude-haiku-4.5`, `gemini/gemini-3.5-flash-lite`.
Gagal/quota: `gc/gemini-3-pro-preview`, `vx/gemini-3.1-pro`, `gemini/gemini-3.1-pro`, `kr/claude-opus-*`, `ag/gemini-pro-agent` (flaky/terpotong).

## TikTok Full-Account Scrape (terbukti 2026-08-08)
`r.jina.ai/https://www.tiktok.com/@user` HANYA balikin profil (following/followers/likes + bio), TIDAK ada list video. oembed cuma 1 video. Untuk bedah KONTEN butuh list video lengkap → pakai **yt-dlp** (ada di venv Hermes):

```bash
YTDLP="/c/Users/arija/AppData/Local/hermes/hermes-agent/venv/Scripts/yt-dlp"
$YTDLP --flat-playlist --dump-json "https://www.tiktok.com/@celineaurel" 2>/dev/null | head -50 | python3 -c "
import sys,json,re
from collections import Counter
views=[];likes=[];tags=Counter();types=[]
for l in sys.stdin:
    try:
        d=json.loads(l)
        v=d.get('view_count',0) or 0; lk=d.get('like_count',0) or 0
        views.append(v);likes.append(lk)
        t=(d.get('title','') or '').lower()
        if any(x in t for x in ['dress','outfit','kaos','celana','crop','outer','top']): types.append('Fashion OOTD')
        elif 'makan' in t or 'promo' in t: types.append('Food Promo')
        elif '#fyp' in t: types.append('FYP Random')
        else: types.append('Lainnya')
        for h in re.findall(r'#\w+', t): tags[h]+=1
    except: pass
print('Avg views:', sum(views)//len(views) if views else 0, '| Max:', max(views) if views else 0)
print('Engagement: %.1f%%' % (sum(likes)/max(sum(views),1)*100))
for ty,c in Counter(types).most_common(): print(ty, c)
for h,c in tags.most_common(10): print(h, c)
"
```
- `--flat-playlist --dump-json` → 1 JSON per baris (pakai `head -N` lalu parse line-by-line).
- Field: `view_count`, `like_count`, `title` (caption + hashtag).
- SocialBlade (`socialblade.com/tiktok/user/...`) lewat r.jina.ai JALAN untuk growth stats (tabel followers/likes per tanggal).

## Pitfall
- DuckDuckGo HTML sering kosong saat diblokir → skip, pakai URL langsung
- r.jina.ai bisa rate-limit → coba 2-3x atau ganti ke sumber lain
- Canva learn/help sering 404 → pakai `/templates/` path bukan `/learn/`
- Niagahoster → redirect ke Hostinger (404) → jangan percaya redirect otomatis
- TikTok video-list TIDAK bisa di-scrape via jina/oembed → wajib yt-dlp (lihat atas)
- yt-dlp `--flat-playlist` return JSON per baris, BUKAN array → jangan `json.load(stdin)` utuh

## Reference
- `references/web_research_fallback.md` — kumpulan command siap pakai
- `references/9router_streaming.md` — parser SSE 9Router
