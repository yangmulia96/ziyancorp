# X (Twitter) Developer Console — App & Token Lifecycle (Field Notes)

## FATAL: Deleting an app kills ALL its tokens
- Deleting an X app (via Settings tab → scroll bottom → Delete App, OR from Apps list) INVALIDATES every token issued by that app: Consumer Key/Secret, Access Token/Secret (OAuth1a), Bearer Token (App-only), and OAuth 2.0 Client ID / Access / Refresh tokens.
- Symptom after deletion: `GET /2/users/me` returns 401 (OAuth1a) or 403 (Bearer) no matter how many times you "regenerate" — because you're regenerating in a DIFFERENT (or nonexistent) app. The Consumer Key in `~/.x_credentials` no longer matches any live app.
- SESSION 2026-08-09: Bos deleted both `shopeeaffiliatee` and `2082093644111073280AgenticsID`. All saved tokens died. Auto-post X impossible until a NEW app was created.

## Recovery procedure (only path)
1. console.x.com → **+ Create App** (name e.g. `ziyan_x`).
2. App permissions: **Read + Write + Direct Message**.
3. Type of App: **Web App, Automated App or Bot** (confidential client).
4. Callback URI / Redirect: `http://127.0.0.1:3000`.
5. Website URL: `https://lynk.id/yang_mulia`.
6. After creation → card **Project Access** (yellow "Not connected") → click **Manage** → pick **Default project** → Connect. Status turns green "Connected".
7. Tab **Keys & Tokens** → **Regenerate Access Token & Secret** (OAuth 1.0a) — MUST be done AFTER step 6, or the token still won't call the API.
8. Copy these 4 values to agent (format `KEY=value` per line in `~/.x_credentials`):
   - CONSUMER_KEY
   - CONSUMER_KEY_SECRET
   - ACCESS_TOKEN
   - ACCESS_TOKEN_SECRET
9. Verify: `OAuth1Session(consumer_key, consumer_secret, access_token, access_token_secret).get("https://api.twitter.com/2/users/me")` → 200 + JSON.

## OAuth 2.0 tokens (alternative)
- Tab Keys & Tokens → "OAuth 2.0 Keys" → Client ID + (regenerate) Client Secret.
- "Generate" an Access Token + Refresh Token for your own account (enables DM access).
- These ALSO die if the app is deleted. Same recovery as above.

## Console navigation (verified, Bos previously angry at wrong directions)
- **Delete App button**: NOT in Keys & Tokens tab, NOT in "Authentication settings" sub-page. Go to app → **Settings** tab (gear icon, next to Keys & Tokens) → scroll to bottom → red **Delete App** → type app name exactly → confirm.
- **Project Access connect**: app overview page → yellow "Not connected" card → **Manage** button → select Default project → Save.
