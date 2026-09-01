"""
YouTube Auto-Uploader for @4kscenicwildlife
Uploads completed video from Google Drive directly to YouTube with full metadata
"""
import os
import json
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


TOKEN_PATH = Path(__file__).parent / "token_scenic_wildlife.json"
DRIVE_FACTORY = "/content/drive/MyDrive/ZIYANCORP_AI_FACTORY"


def upload_to_youtube(video_path: str, data: dict, publish_at: str | None = None) -> dict:
    """Upload video to @4kscenicwildlife YouTube channel with scheduling support."""
    creds = Credentials.from_authorized_user_file(str(TOKEN_PATH))
    youtube = build("youtube", "v3", credentials=creds)

    # Check for schedule timestamp in data or parameter
    target_publish_at = publish_at or data.get("publish_at") or data.get("publishAt")

    status_body = {
        "selfDeclaredMadeForKids": False
    }

    if target_publish_at:
        # YouTube requires privacyStatus = 'private' when publishAt is set
        status_body["privacyStatus"] = "private"
        status_body["publishAt"] = target_publish_at
        print(f"[YOUTUBE_SCHEDULE] Video will be scheduled for: {target_publish_at}")
    else:
        status_body["privacyStatus"] = "public"
        print("[YOUTUBE_PUBLIC] No schedule provided, video will be published publicly immediately.")

    body = {
        "snippet": {
            "title": data["youtube_title"][:100],
            "description": data["youtube_description"],
            "tags": data.get("youtube_tags", []),
            "categoryId": "15"  # Pets & Animals
        },
        "status": status_body
    }

    media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype="video/mp4")
    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            pct = int(status.progress() * 100)
            print(f"Upload progress: {pct}%")

    video_id = response.get("id")
    url = f"https://youtube.com/shorts/{video_id}"
    print(f"[YOUTUBE_UPLOAD_SUCCESS] Video ID: {video_id} | URL: {url}")
    return {"video_id": video_id, "url": url}


if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 3:
        video_path = sys.argv[1]
        data_path = sys.argv[2]
        publish_at_arg = sys.argv[3] if len(sys.argv) >= 4 else None
        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        result = upload_to_youtube(video_path, data, publish_at=publish_at_arg)
        print(json.dumps(result))
