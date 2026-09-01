---
name: ziyan-shopee-affiliate-bot
description: Panduan bot Python (moviepy) untuk bikin video affiliate Shopee massal — gabungkan klip produk + voiceover audio jadi video siap upload. Use when Bos kirim video/tutorial tentang Shopee affiliate bot, Python automation, atau "autocuan 500K/hari".
version: 1.0.0
author: ZIYAN Orchestrator
license: MIT
---

# ZIYAN Shopee Affiliate Video Bot

## Konsep (dari @heyha.id TikTok)
- Script Python `app.py` pakai `moviepy`
- Input: folder `video/` (k lip produk) + `audio/` (voiceover wav)
- Output: `output/affiliate_N.mp4` (video + audio merged)
- Hasil: komisi Rp 500rb/hari (klaim di video)

## Struktur
```
ziyan_affiliate/
├── make_video.py   # main script
├── video/          # klip produk .mp4
├── audio/         # voiceover .wav
└── output/         # hasil .mp4
```

## Workflow n8n
- Manual Trigger → Code node (jalankan python) → Telegram notify
- File: `shopee_affiliate_bot.json`

## Monetisasi
- Template script: $29 (Gumroad)
- Jasa setup + voiceover AI: Rp 2-5jt
- Retainer: $100-300/bln (konten harian)

## Etika & Legal
- Shopee affiliate TIDAK larang video, tapi jangan spam/akun palsu
- Voiceover harus original (bukan claim orang lain)
- Sesuai prinsip ZIYAN: jangan tipu klien

## Referensi
- TikTok @heyha.id: "Cara cepat dapetin 500K perhari Shopee Affiliate Bot Python"
