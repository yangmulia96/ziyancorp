import os, sys, json
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

ROOT = Path(r"C:\Users\arija\ziyancorp\abangjal_archive_bot")
CLIENT_SECRET = ROOT / "client_secret.json"
TOKEN_ARIJAL = ROOT / "token_arijal.json"

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/youtube.force-ssl"
]

flow = InstalledAppFlow.from_client_secrets_file(
    str(CLIENT_SECRET),
    SCOPES,
    redirect_uri="http://localhost:8088/"
)

class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = urlparse(self.path).query
        params = parse_qs(query)
        if "code" in params:
            code = params["code"][0]
            flow.fetch_token(code=code)
            creds = flow.credentials
            TOKEN_ARIJAL.write_text(creds.to_json(), encoding="utf-8")
            
            yt = build("youtube", "v3", credentials=creds)
            ch = yt.channels().list(mine=True, part="snippet").execute()
            ch_title = ch["items"][0]["snippet"]["title"] if ch.get("items") else "Unknown"
            
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            html = f"""
            <html><body style="font-family:sans-serif; text-align:center; padding:50px;">
            <h1 style="color:green;">BERHASIL TERHUBUNG! ✅</h1>
            <p>Channel YouTube <b>{ch_title}</b> berhasil dihubungkan ke bot Arijal Meutuwah.</p>
            <p>Kamu bisa menutup tab ini sekarang.</p>
            </body></html>
            """
            self.wfile.write(html.encode("utf-8"))
            print(f"\n[SUKSES] Token YouTube Arijal Meutuwah berhasil disimpan! Channel: {ch_title}")
            sys.exit(0)
        else:
            self.send_response(400)
            self.end_headers()

def run_server():
    auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')
    print("="*65)
    print("LANGKAH 1: HUBUNGKAN YOUTUBE CHANNEL ARIJAL MEUTUWAH")
    print("="*65)
    print("Buka link ini di browser kamu untuk login ke akun YouTube Arijal:")
    print(auth_url)
    print("="*65)
    
    httpd = HTTPServer(('localhost', 8088), OAuthHandler)
    httpd.handle_request()

if __name__ == "__main__":
    run_server()
