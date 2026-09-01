# Secrets in GitHub — Incident & Procedure (15/8/2026)

## What happened
While writing the cross-agent bridge, real credentials were pasted into `SHARED_MEMORY.md`
and pushed to `ziyancorp/ZIYAN_BRIDGE` which was created as a **PUBLIC** repo.

Leaked values: FB App secret, Threads App secret, App IDs (App IDs are not secret but were
exposed alongside secrets).

## Detection
`grep -c "secret_value" SHARED_MEMORY.md` returned 1 → flagged immediately, before any
external clone could be confirmed.

## Containment steps (do all three)
1. **Scrub the file**: replace secret values with `[VAULT: nama.gpg]` placeholders.
   Verify with `grep -c "secret_value" SHARED_MEMORY.md` → must be 0.
2. **Make repo private**:
   `gh repo edit ziyancorp/ZIYAN_BRIDGE --visibility private --accept-visibility-change-consequences`
3. **RESET the leaked secret in the Meta dashboard** (developers.facebook.com → App →
   Settings → Basic → Reset next to App secret / Threads app secret). A deleted secret in
   git history is STILL compromised — reset is mandatory.

## Prevention rules (embedded in SKILL.md)
- Bridge files reference secrets as `[VAULT: nama.gpg]` only.
- Real secrets live in `C:\Users\arija\.hermes\vault\*.gpg` (AES256). Decrypt:
  `bash bin/token_vault.sh get <n>` (passphrase in `~/.hermes/.env` VAULT_PASS).
- Create bridge repos as PRIVATE on first push.
- Never paste raw tokens into chat, memory, or GitHub.

## Note on git history
Making a repo private hides current state but the leaked commit may remain in reflog/forks.
Resetting the credential is the only real fix — git hygiene alone is insufficient.
