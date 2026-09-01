# Discord "AI Company" Design — orchestrator + per-worker rooms

User wanted a single Orchestrator (1 agent / SOUL.md GM persona) that gradually
recruits/teaches/spawns worker AIs, each confined to its own Discord channel.

## Topology (analogy confirmed with user)
- **Server (guild)** = the "building" / company. One guild: "Hermes agent".
- **Channel** = a "room". Orchestrator owns an HQ room; each worker gets its own.
- **Bot** = `Hermes_bot` (1 token, 1 gateway connection), speaks for all agents.
  Per-worker identity = separate Hermes *profile* (own SOUL.md/role), not a new bot.

## Required permissions (verified)
To let the orchestrator **auto-create AND lock** per-worker rooms, the bot needs BOTH:
- `MANAGE_CHANNELS` (bit 4, decimal 16) — create/delete channels.
- `MANAGE_ROLES` (bit 28, decimal 268435456) — set channel permission overwrites
  (lock room to only that worker + orchestrator).
- Plus base: VIEW_CHANNEL(1024) SEND_MESSAGES(2048) READ_MESSAGE_HISTORY(65536)
  EMBED_LINKS(32768) ATTACH_FILES(16384).

Example full perms that worked: `70371697098320`
  = base(117760) + MANAGE_CHANNELS(16) + MANAGE_ROLES(268435456)
Verify any pasted URL with `scripts/decode_discord_perms.py`.

## PITFALLS (cost real debugging time this session)
1. **Manage Channels alone is NOT enough to lock rooms.** Creating a channel
   succeeds, but `PUT /channels/{id}/permissions/{overwrite_id}` returns
   **403** because setting overwrites requires `MANAGE_ROLES` at guild level.
   Symptom: `@everyone deny` may return 204 (works) but owner/bot allow returns 403.
2. **Role hierarchy 403.** Even with MANAGE_ROLES, the bot cannot set an overwrite
   for a member/role positioned *above* the bot's own role in the server hierarchy
   → `403 Missing Access`. Discord forbids a lower role editing higher ones.
   Fix: either (a) raise the bot's role above the target in Server Settings → Roles,
   or (b) have the user set the lock manually in the Discord UI (right-click channel
   → Edit → Permissions → add user/role → Allow). For the HQ lock where only the
   owner + bot should enter, UI edit by the user was the pragmatic path.
3. **Never grant Administrator** to get around the above — token already exposed in
   chat once = full server takeover risk. Use scoped perms + Reset Token after setup.

## Recommended flow for "hire a worker"
1. `POST /guilds/{gid}/channels` with name (e.g. `riset`) → creates room.
2. `PUT /channels/{cid}/permissions/{everyone_id}` deny VIEW (lock from public).
3. `PUT /channels/{cid}/permissions/{worker_role_id}` allow VIEW+SEND.
4. Create matching Hermes profile + skill SOP; route that worker's tasks there.

See `references/discord.md` for the Developer Portal click-path to obtain the token.
