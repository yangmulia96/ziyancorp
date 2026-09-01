"""Exchange a Google OAuth authorization code for tokens (YouTube+Blogger scopes).

Usage:
  python exchange_token.py <auth_code> [client_secret_json] [token_out_json]

Default client_secret: C:/Users/arija/ziyan_credentials/youtube_desktop_client.json
Default out:           C:/Users/arija/ziyan_credentials/youtube_token.json

The Desktop client redirect_uri must be http://localhost.
"""
import json, sys, urllib.parse, urllib.request

CODE = sys.argv[1] if len(sys.argv) > 1 else None
CLIENT = sys.argv[2] if len(sys.argv) > 2 else r"C:/Users/arija/ziyan_credentials/youtube_desktop_client.json"
OUT = sys.argv[3] if len(sys.argv) > 3 else r"C:/Users/arija/ziyan_credentials/youtube_token.json"

if not CODE:
    print("ERROR: pass the auth code as first arg"); sys.exit(1)

dc = json.load(open(CLIENT))["installed"]
data = urllib.parse.urlencode({
    "client_id": dc["client_id"], "client_secret": dc["client_secret"],
    "code": CODE, "redirect_uri": "http://localhost", "grant_type": "authorization_code"
}).encode()
req = urllib.request.Request("https://oauth2.googleapis.com/token", data=data, method="POST",
                             headers={"Content-Type": "application/x-www-form-urlencoded"})
r = urllib.request.urlopen(req, timeout=20)
tok = json.loads(r.read())
tok_out = {
    "access_token": tok["access_token"],
    "expires_in": tok.get("expires_in"),
    "refresh_token": tok.get("refresh_token"),
    "scope": tok.get("scope"),
    "token_type": tok.get("token_type", "Bearer"),
}
json.dump(tok_out, open(OUT, "w"), indent=2)
print("SAVED", OUT)
print("scope:", tok_out["scope"])
print("has_refresh:", bool(tok_out["refresh_token"]))
