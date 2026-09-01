# TikTok oEmbed Examples — Verified Success Cases

## Format
```bash
curl -s "https://www.tiktok.com/oembed?url=https://www.tiktok.com/@user/video/VIDEO_ID"
```

## Verified Examples

### 1. @github.signals/video/7668076568039771413 (2026-08-11)
**Response:**
```json
{
  "version": "1.0",
  "type": "video",
  "title": "This tool runs a 26-billion-parameter AI model on an 8GB Mac while using only around 2GB of system memory. You can now run a massive twenty-six-billion-parameter artificial intelligence model on an eight-gigabyte Apple Silicon Mac using only about two gigabytes of system memory. This is possible because turbo-fieldfare is a custom Swift and Metal engine built specifically to stream the model's massive neural experts directly from your solid-state drive only when they are needed for a token. By using a clever caching strategy and custom Apple graphics kernels, it keeps the core system memory footprint tiny while maintaining surprisingly fluid text generation speeds on standard consumer hardware. It is the perfect playground for anyone wanting to run heavy local AI without buying expensive hardware. Open source: drumih/turbo-fieldfare Follow for more open source project drops. #LocalAI #MacTok #AppleSilicon #AITools #LLM #MacTips #OpenSource #Mach",
  "author_name": "@github.signals",
  "author_url": "https://www.tiktok.com/@github.signals",
  "provider_name": "TikTok",
  "provider_url": "https://www.tiktok.com",
  "thumbnail_url": "https://p16-sign-va.tiktokcdn.com/...",
  "thumbnail_width": 720,
  "thumbnail_height": 1280
}
```

**Key data extracted:**
- **Topic:** turbo-fieldfare (26B param AI on Mac 8GB RAM, 2GB memory)
- **Tech:** Swift + Metal engine, stream neural experts from SSD, custom caching
- **Open source:** drumih/turbo-fieldfare
- **Hashtags:** #LocalAI #MacTok #AppleSilicon #AITools #LLM #MacTips #OpenSource

### 2. @marcinteodoru/video/7671031316732742943 (2026-08-09)
**Response:** Caption about Fable 5 Ultra Code (multi-agent QC tool for app/website)
**Key data:** Tech promo for dev tool, "Ship with confidence, not hope"

### 3. @adityagnwann/video/7664855091643485458 (2026-08-09)
**Response:** Caption about jcode (terminal coding agent)
**Key data:** Dev tool promo, "A terminal coding agent", install via curl

## Pattern Notes
- oEmbed selalu return **title = caption penuh** (bukan judul pendek)
- author_name = @username
- thumbnail_url = frame video (bisa dipakai untuk visual reference)
- Tidak return: transcript, video URL, hashtags terpisah (harus parse dari title)
- Rate limit: belum ketemu (test berulang OK)

## Short Link Resolution
```bash
# vt.tiktok.com/xxx → dapat URL asli
curl -s -o /dev/null -w "%{url_effective}\n" "https://vt.tiktok.com/ZS4cHNRJT/"
# Output: https://www.tiktok.com/@github.signals/video/7668076568039771413
```