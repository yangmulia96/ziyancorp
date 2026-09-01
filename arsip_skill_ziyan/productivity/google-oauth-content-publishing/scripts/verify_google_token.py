"""Refresh the stored Google token and PROVE what the agent can reach.

Reads token from C:/Users/arija/ziyan_credentials/youtube_token.json,
refreshes via refresh_token (reusing the Desktop client secret), then lists:
  - Blogger blogs (proves Blogger scope + which account)
  - YouTube channels (proves YouTube scope + which account)

Print the output to the user as evidence — never claim an asset is connected
without this proof.
"""
import json, urllib.request, urllib.parse

TOK = r"C:/Users/arija/ziyan_credentials/youtube_token.json"
CLIENT = r"C:/Users/arija/ziyan_credentials/youtube_desktop_client.json"

tok = json.load(open(TOK))
dc = json.load(open(CLIENT))["installed"]

# refresh
data = urllib.parse.urlencode({
    "client_id": dc["client_id"], "client_secret": dc["client_secret"],
    "refresh_token": tok["refresh_token"], "grant_type": "refresh_token"
}).encode()
req = urllib.request.Request("https://oauth2.googleapis.com/token", data=data, method="POST")
new = json.loads(urllib.request.urlopen(req, timeout=20).read())
tok["access_token"] = new["access_token"]
tok["expires_in"] = new.get("expires_in")
json.dump(tok, open(TOK, "w"), indent=2)
access = tok["access_token"]

def api(url):
    r = urllib.request.Request(url, headers={"Authorization": f"Bearer {access}"})
    try:
        resp = urllib.request.urlopen(r, timeout=20)
        return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:300]

print("=== BLOGGER ===")
st, b = api("https://www.googleapis.com/blogger/v3/users/self/blogs")
print("HTTP", st)
if st == 200:
    for blog in b.get("items", []):
        print(f"  - {blog['name']} | id={blog['id']} | {blog.get('url')}")
    if not b.get("items"):
        print("  (no blogs on this account)")
else:
    print("  ", b)

print("\n=== YOUTUBE ===")
st, y = api("https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&mine=true")
print("HTTP", st)
if st == 200:
    for ch in y.get("items", []):
        sn, stt = ch["snippet"], ch.get("statistics", {})
        print(f"  - {sn['title']} | id={ch['id']} | subs={stt.get('subscriberCount')} views={stt.get('viewCount')}")
else:
    print("  ", y)
