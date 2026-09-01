# Google Sheets — curl append + token refresh

Client secret: `AppData/Local/hermes/google_client_secret.json` → key `installed` (has client_id + client_secret). Google project = `ZiyanCorp`.
Token: `AppData/Local/hermes/ziyan_google_token.json` (access_token + refresh_token).

Refresh (if access_token empty/expired):
```python
import json, urllib.parse, urllib.request
d = json.load(open("AppData/Local/hermes/ziyan_google_token.json"))
sec = json.load(open("AppData/Local/hermes/google_client_secret.json"))["installed"]
data = urllib.parse.urlencode({"client_id":sec["client_id"],"client_secret":sec["client_secret"],
        "refresh_token":d["refresh_token"],"grant_type":"refresh_token"}).encode()
r = json.loads(urllib.request.urlopen(urllib.request.Request("https://oauth2.googleapis.com/token", data=data, method="POST"), timeout=15).read())
d["access_token"] = r["access_token"]; json.dump(d, open("AppData/Local/hermes/ziyan_google_token.json","w"))
```

Append row (bypass broken google-api lib):
```bash
AT=$(python3 -c "import json;print(json.load(open('AppData/Local/hermes/ziyan_google_token.json'))['access_token'])")
SID=1wLqdaYcjdaxXD1nEXPIv9PHObFhQPCi80cSiUHqEG8w
# write row.json: {"values":[["col1","col2",...]]}
curl -s -X POST "https://sheets.googleapis.com/v4/spreadsheets/$SID/values/Arsip!A:I:append?valueInputOption=USER_ENTERED&insertDataOption=INSERT_ROWS" \
  -H "Authorization: Bearer $AT" -H "Content-Type: application/json" --data-binary @row.json
```

Create tab "Arsip" if missing:
`POST /v4/spreadsheets/{SID}:batchUpdate` with `addSheet:{properties:{title:"Arsip"}}`.
