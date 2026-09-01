---
name: multi-agent-bridge
description: Coordinate AI agents via a GitHub shared-memory bridge.
---

# Multi-Agent Bridge (GitHub-backed shared memory)

When the user operates **more than one AI agent** (e.g. Hermes + Manus AI + Google Antigravity), a shared, git-backed Markdown file is the lowest-friction coordination layer. Each agent reads/writes the same repo; no chat relay needed.

## When to use
- User says "suruh agent X cek", "biar agent lain tau", "update shared memory", or names 2+ agents working the same problem.
- A blocker needs another agent's capability (e.g. Manus reads GitHub repos the user owns; Hermes owns local terminal/vault).
- Handoff required: one agent stalled, user wants another to continue with full context.

## Architecture
- **One private GitHub repo** = the bridge. Example from production: `ziyancorp/ZIYAN_BRIDGE` with `SHARED_MEMORY.md`.
- Local working copy on this machine: `C:\Users\arija\ZIYAN_BRIDGE\SHARED_MEMORY.md` (git pull / push to sync).
- External agents (Manus AI) read the public-or-private repo via their own GitHub access; Antigravity reads the local `.gemini/` mirror.
- Sync cadence: write → `git commit` → `git push`. Tell the other agent to `git pull`. Don't assume they see it otherwise.

## Directed-message format (CRITICAL)
Write updates as addressed log lines so each agent knows who said what:
```
### [Hermes → All Agents] STATUS DISTRIBUSI ...
### [Hermes → Manus AI] KENDALA THREADS ...
### [Manus → Hermes] SOLUSI THREADS ...
### [Hermes → All] JANGAN PERCAYA KLAIM TANPA VERIFIKASI
```
End each bridge section with `LAST SYNC: <timestamp> (<agent> — <what changed>)`.
This lets an external agent reply in the same file (`[Manus → Hermes] ...`) and Hermes pick it up on next `git pull`.

## SECURITY RULES (non-negotiable)
- **Never write secrets/keys/tokens into the bridge file.** App IDs (non-secret) are OK; App Secrets, access tokens, OAuth codes are NOT.
- Store all secrets in the local encrypted vault: `bash /c/Users/arija/bin/token_vault.sh set <key> "<value>"` (AES256, passphrase in `~/.hermes/.env` VAULT_PASS). Reference them in the bridge as `[VAULT: key.gpg]`, never the value.
- **Make the bridge repo PRIVATE** (`gh repo edit <owner>/<repo> --visibility private --accept-visibility-change-consequences`).
- If a secret is ever pushed to a public repo: (1) scrub it from the file → commit → push, (2) make repo private, (3) **rotate the credential at the source** (Meta App "Reset" button, etc.) because public exposure = compromised. A leaked token cannot be un-leaked.

## FACT-VALIDATION RULE (prevents cross-agent poison)
Other agents may report "100% done / all platforms live" based on another agent's claim, not on their own API test. **Never trust another agent's status claim.** Before reporting any platform/integration as working, verify yourself:
- Token valid? `curl .../me?access_token=TOKEN` → 200 with expected `username`/`id`.
- Post live? Re-READ the resource (`GET /me/threads`, `GET media/{id}`) → confirm ID exists.
- This caught a false "Threads 100% working" claim: token was expired (190) and Threads wasn't linked to the Page.

## SOP: raising a blocker to another agent
1. Write the blocker to the bridge in `[Hermes → <Agent>]` format with verified facts (what failed, error codes, what Hermes can/can't do).
2. `git push`.
3. Tell the user: "suruh <Agent> baca repo X, cek section Y."
4. When the other agent replies in-bridge, `git pull` and act on it.

## Pitfalls
- **Public repo + secret = incident.** Always create the bridge PRIVATE from the start.
- **Don't mix token types.** Threads needs a *Threads user token* (from Meta App → User Token Generator, or OAuth `threads.net`), NOT a Facebook Page/Graph token. FB Graph token ≠ Threads token.
- **Code-exchange tokens are single-use & short-lived.** If `tukar code` returns "Invalid verification code", the code was already used/expired — get a fresh one immediately; don't retry the same code.
- **`gh` CLI may be logged into a different account than the repo owner.** Verify with `gh api users/<owner>` / `gh repo view <owner>/<repo> --json isPrivate` before pushing.

## References
- `references/bridge-format.md` — full directed-message format + real example from the Celine Aurel distribution rollout.
- `references/security-recovery.md` — secret-leak scrub + rotate runbook.
