# X/Twitter — OAuth1a posting (free tier)

Credentials: `~/.x_credentials` (copy `.bak` → active if empty).
Fields: CONSUMER_KEY, CONSUMER_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET.

Bearer (App-only) → 403 on POST /2/tweets. Use OAuth1a:

```python
from requests_oauthlib import OAuth1Session
creds = {}
for line in open(os.path.expanduser("~/.x_credentials")):
    if '=' in line:
        k, v = line.strip().split('=', 1); creds[k] = v
oauth = OAuth1Session(creds['CONSUMER_KEY'], client_secret=creds['CONSUMER_KEY_SECRET'],
                      resource_owner_key=creds['ACCESS_TOKEN'], resource_owner_secret=creds['ACCESS_TOKEN_SECRET'])
# text post
r = oauth.post("https://api.twitter.com/2/tweets", json={"text": "hello"})
# r.status_code == 201 -> r.json()['data']['id']
# with media
with open(path,'rb') as f:
    m = oauth.post("https://upload.twitter.com/1.1/media/upload.json", files={'media': f})
mid = m.json()['media_id_string']
oauth.post("https://api.twitter.com/2/tweets", json={"text":"cap","media":{"media_ids":[mid]}})
# delete
oauth.delete(f"https://api.twitter.com/2/tweets/{id}")
```

Library `requests_oauthlib` + `tweepy` both present on this venv.
