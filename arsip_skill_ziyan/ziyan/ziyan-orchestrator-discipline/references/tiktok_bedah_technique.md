# Bedah Akun TikTok — Teknik andal (terbukti 2026-08-08, @celineaurel)

## Masalah
- TikTok oembed (`/oembed?url=...`) → cuma return: nama, following, followers, likes, bio. TIDAK ada list video.
- `r.jina.ai/https://www.tiktok.com/@user` → cuma bio + suggested accounts. TIDAK ada video list.
- API publik (`api.tiktokv.com/aweme/v1/aweme/post`) → butuh `sec_user_id` + sering 403.

## Solusi: yt-dlp (flat-playlist)
`yt-dlp` ada di venv Hermes: `C:\Users\arija\AppData\Local\hermes\hermes-agent\venv\Scripts\yt-dlp`

```bash
# Ambil semua video (flat, tanpa download)
/c/Users/arija/AppData/Local/hermes/hermes-agent/venv/Scripts/yt-dlp \
  --flat-playlist --dump-json "https://www.tiktok.com/@celineaurel" > list.jsonl

# Per video (1 baris JSON): title, view_count, like_count, webpage_url
# Parse:
python3 -c "
import json
for line in open('list.jsonl'):
    d=json.loads(line)
    print(d.get('view_count',0), d.get('like_count',0), d.get('title','')[:60])
"
```

## Analisis pola konten (contoh @celineaurel, 498 video)
- Avg views 259, max 743, engagement 5.1%
- Tipe: 64% Fashion OOTD, 16% Lainnya, 14% FYP, 6% Food Promo
- Hashtag top: #fypシ, #creatorsearchinsights, #croptopwanita
- Klasifikasi: regex keyword di `title` (dress/kaos/celana = OOTD; #promomakan = Food; #fyp doang = Random)

## Catatan
- `view_count`/`like_count` di flat-playlist kadang 0 untuk video sangat baru (belum terindex) —ambil sample 20-50 teratas.
- yt-dlp tidak butuh login untuk public account.
- Ini cara SATU-SATUNYA dapat isi konten (bukan cuma profil) tanpa API key/TikTok login.
