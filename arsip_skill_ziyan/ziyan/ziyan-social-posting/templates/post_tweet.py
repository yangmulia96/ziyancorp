"""Helper X poster OAuth1a - dipanggil scheduler. FREE posting (bukan paid API)."""
import os
from requests_oauthlib import OAuth1Session

CRED = os.path.expanduser("~/.x_credentials")
creds = {}
for line in open(CRED):
    if '=' in line:
        k, v = line.strip().split('=', 1)
        creds[k] = v

def post_tweet(text, media_path=None):
    oauth = OAuth1Session(
        creds['CONSUMER_KEY'], client_secret=creds['CONSUMER_KEY_SECRET'],
        resource_owner_key=creds['ACCESS_TOKEN'], resource_owner_secret=creds['ACCESS_TOKEN_SECRET'])
    media_id = None
    if media_path and os.path.exists(media_path):
        with open(media_path, 'rb') as f:
            r = oauth.post("https://upload.twitter.com/1.1/media/upload.json", files={'media': f})
        if r.status_code == 200:
            media_id = r.json().get('media_id_string')
    payload = {"text": text}
    if media_id:
        payload["media"] = {"media_ids": [media_id]}
    r = oauth.post("https://api.twitter.com/2/tweets", json=payload)
    return r.json()['data']['id'] if r.status_code == 201 else f"ERR:{r.status_code}"
