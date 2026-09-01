import os, sys, json
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

ROOT = Path(r"C:\Users\arija\ziyancorp\scenic_wildlife_bot")
CLIENT_SECRET = ROOT / "client_secret.json"
TOKEN_SCENIC = ROOT / "token_scenic_wildlife.json"

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
            TOKEN_SCENIC.write_text(creds.to_json(), encoding="utf-8")
            
            try:
                yt = build("youtube", "v3", credentials=creds)
                ch = yt.channels().list(mine=True, part="snippet").execute()
                ch_title = ch["items"][0]["snippet"]["title"] if ch.get("items") else "4K Scenic Wildlife"
            except Exception:
                ch_title = "4K Scenic Wildlife"
            
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            html = f"""
            <html><body style="font-family:sans-serif; text-align:center; padding:50px;">
            <h1 style="color:green;">BERHASIL TERHUBUNG! 🎉</h1>
            <p>Channel YouTube <b>{ch_title} (@4kscenicwildlife)</b> berhasil dihubungkan ke sistem ZiyanCorp.</p>
            <p>Kamu bisa menutup tab ini sekarang.</p>
            </body></html>
            """
            self.wfile.write(html.encode("utf-8"))
            print(f"\n[SUKSES] Token YouTube 4K Scenic Wildlife berhasil disimpan! Channel: {ch_title}")
            sys.exit(0)
        else:
            self.send_response(400)
            self.end_headers()

def generate_link_and_listen():
    auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')
    print("="*70)
    print("LINK LOGIN OAUTH YOUTUBE: @4kscenicwildlife")
    print("="*70)
    print(auth_url)
    print("="*70)
    print("\nMenunggu login dan persetujuan di browser...")
    
    httpd = HTTPServer(('localhost', 8088), OAuthHandler)
    httpd.handle_request()

if __name__ == "__main__":
    generate_link_and_listen()
