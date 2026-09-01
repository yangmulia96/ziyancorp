# Session Manager Module Spec

## Purpose
Manages campaign sessions for the ZIYAN Affiliate Agent. Stores campaign metadata (link, description, platforms) when user sends initial text, retrieves when media files arrive.

## Location
`C:\Users\arija\ziyan_agent\session_manager.py`

## Storage
File-based JSON in `sessions/` directory: `sessions/camp_<uuid8>.json`

## Session Data Structure
```json
{
  "session_id": "camp_a1b2c3d4",
  "link": "https://s.shopee.co.id/xxx",
  "description": "Celana jeans korea...",
  "platforms": ["facebook", "instagram", "youtube"],
  "media_count": 4,
  "created_at": "2026-08-11T19:30:00Z"
}
```

## Methods

### create_session(link, desc, platforms)
Creates new session, returns session_id.

### get_session(session_id)
Returns session dict or None.

### update_session_media_count(session_id, count)
Updates media_count, returns bool.

### delete_session(session_id)
Deletes session file, returns bool.

### cleanup_expired_sessions(max_age_hours=24)
Removes sessions older than max_age_hours, returns deleted count.

## Usage in Telegram Bot Flow
1. User sends text with link + description (+ optional platforms)
2. Bot calls `create_session()` → gets session_id
3. Bot stores session_id in memory for this user
4. User sends media files (multi-file or sequential)
5. For each file, bot calls `get_session(session_id)` to retrieve link/desc/platforms
6. After all files processed, bot calls `delete_session(session_id)` to clean up

## Notes
- Session expires after 24 hours (configurable)
- File-based storage works for single-instance daemon
- For multi-instance, would need Redis/shared storage