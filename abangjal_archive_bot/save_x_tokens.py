import os, json
from pathlib import Path
from dotenv import set_key

ROOT = Path(r"C:\Users\arija\ziyancorp\abangjal_archive_bot")
ENV_FILE = ROOT / ".env"
TOKEN_FILE = ROOT / "x_token_arijal.json"

access_token = "WEdpVzNhZ29QemxKRUNWSlAwaEQ0MUFtMm51YmIycndleGJqTmZwbEF4enR4OjE3ODczOTgzNTI2Nzk6MTowOmF0OjE"
refresh_token = "MjJjV25Ja1FsNFRHUUhyYnphYnp5aEdZSGFLSDRVUklhS2xMWF8yWEt2Ml9wOjE3ODczOTgzNTI2Nzk6MTowOnJ0OjE"

# 1. Save to .env
set_key(str(ENV_FILE), "X_ACCESS_TOKEN_ARIJAL", access_token)
set_key(str(ENV_FILE), "X_REFRESH_TOKEN_ARIJAL", refresh_token)

# 2. Save to JSON
token_data = {
    "token_type": "bearer",
    "access_token": access_token,
    "refresh_token": refresh_token,
    "scope": "tweet.read tweet.write users.read offline.access"
}
TOKEN_FILE.write_text(json.dumps(token_data, indent=2), encoding="utf-8")
print(f"X (Twitter) tokens for Arijal Meutuwah saved to:\n1. {ENV_FILE}\n2. {TOKEN_FILE}")
