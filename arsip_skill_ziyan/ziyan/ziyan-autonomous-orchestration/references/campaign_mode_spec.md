# Campaign Mode: Link+Desc+Multimedia → Variative Posts + Archive (TERBUKTI 2026-08-11)

## Overview
Bos can send one text message with product link, description, and optional platforms, then send multiple media files (video/photo) in one or multiple messages. The system processes each file into separate posts with variative captions, archives to Google Drive, and queues to Sheets per platform.

## Flow

### Phase 1: Campaign Setup (Text Input)
User sends text:
```
Link: https://s.shopee.co.id/xxx
Deskripsi: Celana jeans korea pinggang tinggi stretch nyaman
Platform: fb, ig, yt  (optional, default: fb,ig,yt)
```

Bot:
1. Parses link, description, platforms
2. Creates session: `session_id = camp_<uuid8>`
3. Saves to `sessions/camp_<uuid8>.json` with link, desc, platforms, media_count=0, created_at
4. Replies: "✅ Campaign siap. Kirim medianya (video/foto). Platform default: FB + IG + YT."

### Phase 2: Media Batch Processing
User sends media files (up to 10 in one message, or sequential):
For each file:
1. Download to `media/camp_<uuid8>_<index>.<ext>`
2. Upload to Google Drive: `/Ziyan/Campaigns/camp_<uuid8>/` → get `drive_file_id`
3. Generate variative caption via 9Router (angle based on index: 1=hemat, 2=kenyamanan, 3=gaya, 4=kualitas)
4. Determine platforms by file type: video→fb,ig,yt; photo→fb,ig
5. Queue to Sheets per platform per file with:
   - job_id: `camp_<uuid8>_<index>_<platform>`
   - media_path, drive_file_id, caption, affiliate_link, product_desc
   - platform, status=PENDING, schedule_time (stagger), created_at
   - caption_variation: `1_of_4`

### Phase 3: Confirmation
Bot replies summary:
```
✅ Campaign camp_a1b2c3d4 selesai!
📁 4 file → 11 job queued
Jobs:
• camp_a1b2c3d4_1 → FB, IG, YT
• camp_a1b2c3d4_2 → FB, IG, YT
• camp_a1b2c3d4_3 (foto) → FB, IG
• camp_a1b2c3d4_4 → FB, IG, YT
📊 Cek: /list camp_a1b2c3d4
🗂️ Drive: /Ziyan/Campaigns/camp_a1b2c3d4/
```

### Phase 4: Scheduler Auto-Publish (every 8 min)
- Query Sheets: status=PENDING AND schedule_time <= now
- Per job: download from Drive if needed → upload to platform → update Sheets POSTED + post_url + posted_at
- Stagger: schedule_time = now + 77min * queue_position

### Phase 5: Monitoring Commands
- `/list` — all PENDING jobs
- `/list <session_id>` — filter by campaign
- `/cancel <job_id>` — cancel one job
- `/cancel <session_id>` — cancel all jobs in campaign

## Technical Notes
- Google Drive API uses same service account as Sheets
- Folder created automatically if not exists
- Caption variation per file to avoid duplicate content
- Stagger based on queue position to prevent spam
- ig_user_id not set → IG skipped with warning (no crash)
- Session expires after 24h (configurable)
- File-based session storage (single-instance); multi-instance needs Redis