---
name: notebooklm-auth
description: Fix notebooklm-py auth on Windows/Hermes.
---

# NotebookLM CLI Authentication (Windows / Hermes)

Use this skill whenever a NotebookLM automation task fails at the auth step
(`notebooklm list` returns "Authentication expired or invalid") or when
onboarding the NotebookLM Operator for a content pipeline.

## Environment facts (this host)
- `notebooklm-py` is installed in the **Hermes venv**, NOT system python.
- System `python3` (3.13) does NOT have Playwright/notebooklm-py → calls fail.
- Correct binary: `C:\Users\arija\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe -m notebooklm`
- A `.bat` launcher MUST `CALL` the venv activate script, not use bare `python`.

## AUTH REALITY (proven 2026-08-02, Windows 10, this host)
**Neither `login --fresh` NOR `login --browser-cookies` works here.** Both fail:
- `login --fresh` (Playwright Chromium): window opens, but the session is NOT saved to `~/.notebooklm/profiles/default/storage_state.json` → `list` says "Missing required cookies: SID, __Secure-1PSIDTS". Cause: window closed / DevTools opened / redirect not captured.
- `login --browser-cookies brave|chrome` → `Failed to decode plaintext: Can't decode encrypted value` / `Could not decrypt chrome cookies`. Cause: **Windows DPAPI / App-Bound Encryption** blocks rookiepy from reading browser cookie DB. DPAPI `crypt32.CryptUnprotectData` fallback ALSO fails (same encrypted blob).
- `auth refresh` does NOT recover a stale cookie — it exercises the auth path once and fails identically.

**THE ONLY RELIABLE PATH = Netscape cookie export from the browser (not DPAPI).**
See `references/netscape_export.md` for the working convert script + 1-click `.bat`.

## Standard auth flow (WORKING — Netscape export)
1. User opens `notebooklm.google.com` in their already-logged-in Brave/Chrome, confirms dashboard loads.
2. User exports cookies via "Get cookies.txt LOCALLY" extension → **Netscape format** → saves `C:\Users\arija\Downloads\cookies.txt`.
   - MUST export from the notebooklm.google.com page (not another tab) so `__Secure-1PSIDTS` for the google domain is captured.
3. User double-clicks `sync_notebooklm_auth.bat` (agent-provided) → filters google cookies, converts to storage_state.json, runs `auth check`.
4. Verify with `notebooklm list` (NOT just `auth check` — see trap below).

## CRITICAL TRAP: `auth check` is a FALSE POSITIVE
`auth check --test` only verifies "SID cookie present in file" — it does NOT confirm the session is still live at Google. It can print "Authentication is valid" while `add-research` / `generate` still fail with "Authentication expired or invalid. Redirected to accounts.google.com".

**Always verify with a live call:**
- `notebooklm list` → returns notebook list (proves session alive)
- or `notebooklm source add-research "<topic>" --no-wait` (RPC actually exercises auth)

## COOKIE STALE = THE REAL BLOCKER
Error "Authentication expired" on live RPC = Google **rejected the cookie (stale/rotated)**, NOT a format bug. No CLI recovery exists.
**Only fix: re-export `cookies.txt` from notebooklm.google.com (still logged in) → replace file → re-run `sync_notebooklm_auth.bat`.** Repeat whenever the cookie expires.

## Convert script gotchas (proven)
- Session cookies (expiry=0 in Netscape) MUST become `"expires": -1`, NOT `null`. Playwright DROPS `null`-expiry cookies → Google logs out.
- Keep `sameSite: "Lax"` for non-secure; `secure` flag from the Netscape column.
- Filter to google domains only (`.google.com`, `.youtube.com`, `notebook.google.com`, `accounts.google.com`, `.google.co.id`) — unrelated cookies cause no harm but bloat the file.

## Verification (end state)
1. `notebooklm doctor` → "All checks passed"
2. `notebooklm list` → notebook list returned (NOT auth error)
3. Only then run `add-research` / `generate`.

## When to hand back to the user
If `cookies.txt` re-export still fails after 1-2 tries, ask the user to re-export from notebooklm.google.com directly. Do NOT loop on DPAPI/browser-cookies (both confirmed broken on this host).
