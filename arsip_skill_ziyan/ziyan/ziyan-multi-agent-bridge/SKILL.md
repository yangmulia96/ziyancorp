---
name: ziyan-multi-agent-bridge
description: Cross-agent GitHub shared memory for ZIYAN agents.
---

# ZIYAN Multi-Agent Bridge (GitHub Shared Memory)

## When to use
- User: "buat shared memory di GitHub", "biar agent bisa kerjasama", "komunikasi dengan agent lain", "suruh Manus cek"
- 3 agents: **Hermes** (Orkestrator), **Antigravity/Google**, **Manus AI**
- Need persistent cross-session, cross-agent state

## Architecture (verified 15/8)
- Repo: `github.com/ziyancorp/ZIYAN_BRIDGE` — **MUST be PRIVATE**
- `SHARED_MEMORY.md` = conversation log (the bridge)
- `README.md` = structure + security rules
- `projects/completed/<name>/HISTORY.md`, `projects/active/`, `projects/blocked/`, `projects/archive/`
- Loop: agent `git pull` → read → append section → `git push`; others `git pull`

## Format conventions
```
### [Hermes → All] STATUS ...
facts verified via API
### [Manus → Hermes] SOLUSI ...
endpoint URLs
```
- VERIFY claims with API before writing "done" (Bos rule #2). Re-test others' claims yourself.
- Request specific agent: `[Hermes → Manus] tolong cek ...`

## CRITICAL SECURITY RULE (secret leaked to PUBLIC repo this session)
1. **NEVER** write secrets/tokens to `SHARED_MEMORY.md` or any GitHub file.
2. Use local vault:
   - `bash bin/token_vault.sh set <key> "<value>"` / `get <key>`
   - Vault: `C:\Users\arija\.hermes\vault\*.gpg` (AES256, pass in `~/.hermes/.env` VAULT_PASS)
   - Reference in bridge as `[VAULT: key.gpg]`
3. Repo MUST be private: `gh repo edit ziyancorp/ZIYAN_BRIDGE --visibility private --accept-visibility-change-consequences`
4. If a secret EVER leaks to public GitHub — **REMEDIATION RECIPE (verified 15/8)**:
   - **Detect**: `grep -c "actual_secret_value" ZIYAN_BRIDGE/SHARED_MEMORY.md` → if >0, leaked.
   - **Clean**: replace secret string in file with `[VAULT: key.gpg]` (python or patch tool). Re-grep until 0 matches.
   - **Push clean**: `git -C ZIYAN_BRIDGE commit -am "SECURITY: remove secret" && git push`
   - **Private NOW**: `gh repo edit ziyancorp/ZIYAN_BRIDGE --visibility private --accept-visibility-change-consequences`
   - **RESET in dashboard** (exposed token is burned — reading it back does NOT make it safe): Meta App → Settings → Basic → Reset App Secret (and Threads app secret). Get new secret, store in vault ONLY.
   - **NEVER** write the new secret to GitHub, only `[VAULT: key.gpg]` reference.
5. **GitHub identity quirk**: `gh auth status` may show login `yangmulia96` while `gh api users/ziyancorp` works (ziyancorp is a separate account/repo owner). When Bos gives a GitHub username from a screenshot, **trust the screenshot** (e.g. `ziyancorp`), don't hunt for the old `yangmulia96`. `gh` can push to `ziyancorp/*` even if `gh auth status` shows a different login, as long as that account owns the repo.

## Setup (first time)
```bash
cd C:\Users\arija\ZIYAN_BRIDGE
git init -q && git add SHARED_MEMORY.md README.md
git -c user.email=arizalkempo@gmail.com -c user.name="Yang Mulia" commit -m "bridge init"
gh repo create ziyancorp/ZIYAN_BRIDGE --public --description "Shared memory bridge"
git branch -M main && git push -u origin main
gh repo edit ziyancorp/ZIYAN_BRIDGE --visibility private --accept-visibility-change-consequences
```
- `gh` CLI may be logged in as a DIFFERENT username than GitHub web (e.g. `yangmulia96` vs `ziyancorp`). Confirm: `gh api users/ziyancorp`.

## Pitfalls
- Agent claiming "100% selesai" without API verification → re-test (Threads claimed done, token invalid 190).
- Public repo + secret = breach; reset tokens + private immediately.
- Don't mix FB Graph token with Threads user token (see ziyan-celine-distribution).
