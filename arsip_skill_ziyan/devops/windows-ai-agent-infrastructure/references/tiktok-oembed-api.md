# TikTok oEmbed API Reference

## Problem
TikTok blocks scraping (yt-dlp fails with "Unable to extract universal data for rehydration"). Channel-researcher model cannot browse live.

## Solution: TikTok oEmbed API
```
GET https://www.tiktok.com/oembed?url=https://www.tiktok.com/@{username}/video/{video_id}
```

## Example
```bash
curl -s "https://www.tiktok.com/oembed?url=https://www.tiktok.com/@github.signals/video/7668076568039771413"
```

## Response Format (JSON)
```json
{
  "version": "1.0",
  "type": "video",
  "title": "Full caption text including hashtags...",
  "author_name": "@username",
  "author_url": "https://www.tiktok.com/@username",
  "provider_name": "TikTok",
  "provider_url": "https://www.tiktok.com",
  "cache_age": 86400,
  "thumbnail_url": "https://...",
  "thumbnail_width": 720,
  "thumbnail_height": 1280,
  "html": "<blockquote class=\"tiktok-embed\" ...>"
}
```

## Key Fields
- `title` = **full caption** (text + hashtags + links)
- `author_name` = username
- `thumbnail_url` = video cover image

## Limitations
- Only public videos (not private/deleted)
- No video URL download
- No comments/stats
- Rate limited (unknown exact limit)

## Usage in ZIYAN
- Extract caption for content analysis
- Identify affiliate products/links
- Research competitor content strategy
- Feed into Sistem 2 (AI Influencer) / Sistem 3 (Value-First Help)