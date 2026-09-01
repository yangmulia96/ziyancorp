# Discord Bot Setup Click-Path (for Hermes gateway)

1. Go to https://discord.com/developers/applications
2. **New Application** → name it (e.g. "Hermes Agent") → Create.
3. Left menu **Bot** tab:
   - Click **Add Bot** (if not already).
   - **Reset Token** → copy the new token → this is `DISCORD_BOT_TOKEN`.
   - Scroll to **Privileged Gateway Intents**:
     - ✅ MESSAGE CONTENT INTENT (required to read message text)
     - ✅ SERVER MEMBERS INTENT (required for allowed-users / member lookups)
4. Left menu **OAuth2 → URL Generator**:
   - Scopes: ✅ `bot`, ✅ `applications.commands`
   - Bot Permissions (scope minimal, NOT Administrator):
     - Send Messages
     - Read Messages / View Channels
     - Read Message History
     - Embed Links
     - Attach Files
     - Add Reactions
   - Copy generated URL → open in browser → pick your server → Authorize.
5. Get IDs for `.env`:
   - Channel ID (`DISCORD_HOME_CHANNEL`): enable Developer Mode (User Settings → Advanced → Developer Mode), right-click channel → Copy Channel ID.
   - Your User ID (`DISCORD_ALLOWED_USERS`): right-click your name → Copy User ID.
6. Paste three vars into `C:\Users\<user>\AppData\Local\hermes\.env` (via terminal, never print the raw token):
   ```
   DISCORD_BOT_TOKEN=<pasted-token>
   DISCORD_ALLOWED_USERS=<your-user-id>
   DISCORD_HOME_CHANNEL=<channel-id>
   ```
7. Restart gateway: `hermes gateway restart` (or stop then start).
8. Verify in `logs/gateway.log`: no more `LoginFailure`; look for ready/connected.

## Common failure: 403 Missing Access (bot logged in, can't post)
`401 Improper token` = bad token. `403 Missing Access` = token is fine, bot is connected, but it has NO permission on the specific channel you targeted with `hermes send` or where messages arrive.

Fix (two steps, both required):
- **Bot must be in the server**: confirm it appears in the member list. If missing, open the OAuth2 invite URL from step 4 and Authorize.
- **Channel-specific perms**: if the channel is private/locked, right-click the channel → Edit Channel → Permissions → Add Member/Role → the bot `Hermes_bot` → grant **View Channel** + **Send Messages**. Public channels usually inherit server-level perms from the invite, but locked channels need explicit grant.

## Invite URL sanity check (no need to open it)
URL form: `https://discord.com/oauth2/authorize?client_id=<id>&permissions=<bitfield>&scope=bot+applications.commands`
- `client_id` is the base64 of the bot's numeric ID (token starts with the same base64, e.g. `MTUzMjY1…` decodes to `153265…`).
- Decode `permissions` bitfield to confirm scope: e.g. `117760` = View Channels + Send Messages + Manage Messages + Embed Links + Attach Files (no Administrator — safe).
- Never paste raw tokens into the chat; if you did, Reset Token again after the gateway connects.
