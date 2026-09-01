import sys, json, urllib.parse
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

auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')

print("="*70)
print("LINK OAUTH RESMI:")
print("="*70)
print(auth_url)
print("="*70)
print("MENUNGGU_CALLBACK_SEKARANG")

class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = urlparse(self.path).query
        params = parse_qs(query)
        if "code" in params:
            code = params["code"][0]
            try:
                flow.fetch_token(code=code)
                creds = flow.credentials
                TOKEN_SCENIC.write_text(creds.to_json(), encoding="utf-8")
                
                yt = build("youtube", "v3", credentials=creds)
                ch = yt.channels().list(mine=True, part="snippet").execute()
                item = ch["items"][0]["snippet"] if ch.get("items") else {}
                ch_title = item.get("title", "Unknown")
                ch_handle = item.get("customUrl", "@unknown")
                
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                html = f"""
                <html><body style="font-family:sans-serif; text-align:center; padding:50px;">
                <h1 style="color:green;">BERHASIL TERHUBUNG!</h1>
                <p>Channel YouTube: <b>{ch_title} ({ch_handle})</b></p>
                <p>Token berhasil disimpan permanen. Tutup tab ini.</p>
                </body></html>
                """
                self.wfile.write(html.encode("utf-8"))
                print(f"\n[SUKSES_TERHUBUNG] Channel: {ch_title} | Handle: {ch_handle}")
                sys.exit(0)
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(f"Error: {e}".encode("utf-8"))
                print(f"\n[ERROR_TOKEN] {e}")
                sys.exit(1)
        else:
            self.send_response(400)
            self.end_headers()

httpd = HTTPServer(('0.0.0.0', 8088), OAuthHandler)
httpd.handle_request()
