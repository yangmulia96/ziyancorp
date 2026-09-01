# Bridge Secret-Leak Incident & Remediation (15/8/2026)

## What happened
While setting up the 3-agent GitHub bridge (`ziyancorp/ZIYAN_BRIDGE`), I wrote Meta app
secrets (Threads app secret `bbdc0cb1895636`, FB app secret `18bd7af50624616`) into
`SHARED_MEMORY.md` and `git push` to a **PUBLIC** repo. The secrets were exposed for
~30 minutes before detection.

## Detection
```
grep -c "bbdc0cb1895636\|18bd7af50624616" ZIYAN_BRIDGE/SHARED_MEMORY.md  # -> 1 (FOUND)
gh repo view ziyancorp/ZIYAN_BRIDGE --json isPrivate  # -> {"isPrivate":false}
```

## Remediation steps (in order)
1. **Scrub from file**: replace secret strings with `[VAULT: name.gpg]` references.
   ```python
   s = s.replace('bbdc0cb1895636', '[VAULT: threads_app_secret.gpg]')
   ```
2. **Verify clean**: `grep -c "bbdc0cb1895636" SHARED_MEMORY.md` → must be `0`.
3. **Commit + push** the cleaned version.
4. **Make repo private**:
   ```
   gh repo edit ziyancorp/ZIYAN_BRIDGE --visibility private --accept-visibility-change-consequences
   ```
5. **RESET secrets in Meta dashboard** (exposed secrets are compromised, even after
   repo is private — git history may persist on forks/mirrors):
   - developers.facebook.com/apps/APP_ID/settings/basic/ → Reset App secret
   - Same page → Threads section → Reset Threads app secret
6. **Store new secrets ONLY in vault**:
   ```
   bash bin/token_... no — use: bash bin/token_vault.sh set threads_app_secret "NEW_SECRET"
   ```
7. **Never** put secrets in shared repos again. Bridge files carry status + vault
   references, never values.

## Durable rule
Secrets (tokens, app secrets, API keys) live ONLY in `.hermes/vault/*.gpg` (AES256).
Shared memory / GitHub / chat carry `[VAULT: key.gpg]` pointers, never the value.
