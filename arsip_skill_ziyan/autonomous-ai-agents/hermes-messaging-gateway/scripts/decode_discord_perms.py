#!/usr/bin/env python3
"""Decode a Discord OAuth `permissions` integer into human-readable flag names.
Usage:
  python decode_discord_perms.py 70371428662864
  python decode_discord_perms.py --url "https://discord.com/oauth2/authorize?client_id=...&permissions=126032"
Prints which permissions are set + whether ADMINISTRATOR is included.
Use this to verify a pasted invite URL before the user clicks it.
"""
import sys, re

BITS = {
 0:"CREATE_INSTANT_INVITE",1:"KICK_MEMBERS",2:"BAN_MEMBERS",3:"ADMINISTRATOR",
 4:"MANAGE_CHANNELS",5:"MANAGE_GUILD",6:"ADD_REACTIONS",7:"VIEW_AUDIT_LOG",
 10:"VIEW_CHANNEL",11:"SEND_MESSAGES",12:"SEND_TTS_MESSAGES",13:"MANAGE_MESSAGES",
 14:"EMBED_LINKS",15:"ATTACH_FILES",16:"READ_MESSAGE_HISTORY",17:"MENTION_EVERYONE",
 18:"USE_EXTERNAL_EMOJIS",19:"VIEW_GUILD_INSCRIPTIONS",20:"CONNECT",21:"SPEAK",
 22:"MUTE_MEMBERS",23:"DEAFEN_MEMBERS",24:"MOVE_MEMBERS",25:"USE_VAD",
 26:"CHANGE_NICKNAME",27:"MANAGE_NICKNAMES",28:"MANAGE_ROLES",29:"MANAGE_WEBHOOKS",
 30:"MANAGE_EMOJIS",31:"USE_APPLICATION_COMMANDS",34:"MANAGE_THREADS",
 35:"USE_PUBLIC_THREADS",36:"USE_PRIVATE_THREADS",37:"USE_EXTERNAL_STICKERS",
 39:"VIEW_CREATOR_MONETIZATION_ANALYTICS",41:"USE_SOUNDBOARD",42:"USE_EXTERNAL_SOUNDS",
 44:"SEND_VOICE_MESSAGES",45:"USE_ACTIVITIES",46:"USE_CLYDE_AI",48:"CREATE_GUILD_EXPRESSIONS",
 49:"CREATE_EVENTS",50:"MODERATE_MEMBERS"
}

def decode(perms: int):
    print("ADMINISTRATOR included:", bool(perms & (1<<3)))
    print("--- Permission flags set ---")
    for b, name in sorted(BITS.items()):
        if perms & (1<<b):
            print(f"  [{b}] {name}")
    if perms & (1<<3):
        print("\nWARNING: includes ADMINISTRATOR. Avoid for bot tokens that may leak.")

def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else ""
    if arg.startswith("http"):
        m = re.search(r"permissions=(\d+)", arg)
        if not m:
            print("No permissions= param found in URL"); sys.exit(1)
        perms = int(m.group(1))
    else:
        perms = int(arg)
    decode(perms)

if __name__ == "__main__":
    main()
