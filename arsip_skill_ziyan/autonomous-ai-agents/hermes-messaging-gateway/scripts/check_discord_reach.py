"""Diagnose Discord bot reachability: list guilds + text channels, test a target channel.

Usage: python check_discord_reach.py [TARGET_CHANNEL_ID]
Reads DISCORD_BOT_TOKEN from ~/.hermes/.env (never printed). Requires `requests`.
"""
import os, sys, requests

ENV = os.path.expanduser(r"C:\Users\arija\AppData\Local\hermes\.env")
if not os.path.exists(ENV):
    ENV = os.path.expanduser("~/.hermes/.env")
tok = None
for line in open(ENV, encoding="utf-8"):
    if line.startswith("DISCORD_BOT_TOKEN="):
        tok = line.strip().split("=", 1)[1].strip()
        break
assert tok, "DISCORD_BOT_TOKEN not found in .env"
H = {"Authorization": "Bot " + tok, "Content-Type": "application/json"}

me = requests.get("https://discord.com/api/v10/users/@me", headers=H).json()
print(f"BOT: {me.get('username')}#{me.get('discriminator')}")
guilds = requests.get("https://discord.com/api/v10/users/@me/guilds", headers=H).json()
print(f"GUILDS: {len(guilds)}")
for g in guilds:
    gid, name = g["id"], g["name"]
    chans = requests.get(f"https://discord.com/api/v10/guilds/{gid}/channels", headers=H).json()
    texts = [c for c in chans if c.get("type") in (0, 5)]
    print(f"  SERVER: {name} ({gid}) — {len(texts)} text channels")
    for c in texts:
        print(f"    #{c['name']}  [id={c['id']}]")

if len(sys.argv) > 1:
    tid = sys.argv[1]
    r = requests.get(f"https://discord.com/api/v10/channels/{tid}", headers=H)
    j = r.json()
    print(f"TARGET {tid}: HTTP {r.status_code} name={j.get('name')} guild={j.get('guild_id')}")
    if r.status_code == 403:
        print("  -> channel is in a guild the bot is NOT a member of, or lacks View Channel.")
