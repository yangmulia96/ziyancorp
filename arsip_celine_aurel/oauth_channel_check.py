from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Read access is needed for the channel preflight; upload is needed by the uploader.
SCOPES = [
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/youtube.upload",
]


def get_credentials(client_secret_file: Path, token_file: Path) -> Credentials:
    credentials = None

    if token_file.exists():
        try:
            credentials = Credentials.from_authorized_user_file(
                str(token_file), SCOPES
            )
        except (ValueError, json.JSONDecodeError) as exc:
            raise RuntimeError(
                f"Token {token_file} tidak cocok dengan scope saat ini. "
                "Hapus token Celine dan lakukan consent ulang."
            ) from exc

    if credentials and credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())

    if not credentials or not credentials.valid:
        if not client_secret_file.exists():
            raise FileNotFoundError(
                f"Client secret tidak ditemukan: {client_secret_file}"
            )
        flow = InstalledAppFlow.from_client_secrets_file(
            str(client_secret_file), SCOPES
        )
        # The browser flow is performed by the owner. The script never handles a password.
        credentials = flow.run_local_server(
            port=0,
            access_type="offline",
            prompt="consent",
        )
        token_file.parent.mkdir(parents=True, exist_ok=True)
        token_file.write_text(credentials.to_json(), encoding="utf-8")

    return credentials


def get_my_channel(credentials: Credentials) -> dict:
    youtube = build("youtube", "v3", credentials=credentials)
    response = (
        youtube.channels()
        .list(part="id,snippet,contentDetails", mine=True)
        .execute()
    )
    items = response.get("items", [])
    if not items:
        raise RuntimeError(
            "Google Account yang memberi consent tidak mengembalikan channel "
            "melalui channels.list(mine=true). Periksa role Brand Account, "
            "default channel, atau masalah layanan Google."
        )
    if len(items) > 1:
        print(
            "Peringatan: API mengembalikan lebih dari satu channel; "
            "validasi target tetap wajib dilakukan.",
            file=sys.stderr,
        )
    item = items[0]
    return {
        "id": item.get("id"),
        "title": item.get("snippet", {}).get("title"),
        "customUrl": item.get("snippet", {}).get("customUrl"),
        "uploadsPlaylistId": item.get("contentDetails", {})
        .get("relatedPlaylists", {})
        .get("uploads"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validasi channel YouTube yang terikat pada token OAuth Celine."
    )
    parser.add_argument(
        "--client",
        type=Path,
        default=Path("client_secret.json"),
        help="Path ke client_secret.json",
    )
    parser.add_argument(
        "--token",
        type=Path,
        default=Path("token_celine.json"),
        help="Path ke token Celine; jangan gunakan token channel personal.",
    )
    parser.add_argument(
        "--expected-channel",
        action="append",
        required=True,
        help="Channel ID target. Bisa diberikan dua kali jika dua ID masih perlu diverifikasi.",
    )
    args = parser.parse_args()

    try:
        credentials = get_credentials(args.client, args.token)
        channel = get_my_channel(credentials)
    except (FileNotFoundError, RuntimeError, HttpError) as exc:
        print(f"PREFLIGHT_FAILED: {exc}", file=sys.stderr)
        return 2

    print(json.dumps(channel, ensure_ascii=False, indent=2))
    if channel["id"] not in set(args.expected_channel):
        print(
            "PREFLIGHT_FAILED: channel dari token bukan salah satu target. "
            "Uploader harus berhenti dan tidak boleh upload.",
            file=sys.stderr,
        )
        return 3

    print("PREFLIGHT_OK: channel cocok dengan target yang dikonfigurasi.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
