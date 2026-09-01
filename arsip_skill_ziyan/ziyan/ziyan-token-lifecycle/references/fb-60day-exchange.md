# FB 60-Day PAGE Token Exchange — exact sequence

Prereqs:
- APP_ID  = OneDrive/ziyan_pending/fb_app_id.txt
- APP_SEC = OneDrive/ziyan_pending/fb_app_secret.txt
- SHORT_PAGE_TOKEN = from `/me/accounts` (or Bos pastes in chat → save to file)

Step 1 — get short page token:
```
TOK=$(cat OneDrive/ziyan_pending/fb_page_token.txt)   # short user/page token
curl -s "https://graph.facebook.com/v19.0/me/accounts?fields=id,name,access_token&access_token=$TOK"
# take the access_token for Celine Aurel (id 975723622288353)
```

Step 2 — exchange to 60-day:
```
APPID=$(cat OneDrive/ziyan_pending/fb_app_id.txt)
APPSEC=$(cat OneDrive/ziyan_pending/fb_app_secret.txt)
SHORT=<page token from step 1>
curl -s "https://graph.facebook.com/v19.0/oauth/access_token?grant_type=fb_exchange_token&client_id=$APPID&client_secret=$APPSEC&fb_exchange_token=$SHORT"
# => {"access_token":"EAA...","token_type":"bearer"}
```
Save result `access_token` to `OneDrive/ziyan_pending/fb_page_token.txt` (overwrites short one).

Step 3 — verify by post+delete:
```
PT=$(cat OneDrive/ziyan_pending/fb_page_token.txt)
FBID=975723622288353
PID=$(curl -s -X POST "https://graph.facebook.com/v19.0/$FBID/feed" -F "message=test" -F "access_token=$PT" | python3 -c "import sys,json;print(json.load(sys.stdin)['id'])")
curl -s -X DELETE "https://graph.facebook.com/v19.0/$PID?access_token=$PT"
```

Debug token:
```
curl -s "https://graph.facebook.com/debug_token?input_token=$PT&access_token=$PT"
# type:PAGE, is_valid:true. expires_at may be absent for long-lived → OK.
```

Pitfall: never trust `/me/accounts` token as long-lived without Step 2.
