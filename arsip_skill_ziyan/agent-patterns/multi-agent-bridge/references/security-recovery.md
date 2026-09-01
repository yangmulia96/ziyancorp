# Secret-Leak Recovery Runbook

Used when a Meta App Secret (or any credential) is accidentally committed to a
PUBLIC GitHub bridge repo.

## Incident: Meta App Secret pushed public (15 Aug 2026)
A bridge update included `fb_app_secret=18bd7af50624616` and
`threads_app_secret=bbdc0cb1895636` in `SHARED_MEMORY.md` on a PUBLIC repo
(`ziyancorp/ZIYAN_BRIDGE`). Detected via `grep` for the secret value.

## Recovery sequence (do in order)
1. **Scrub the file locally** — replace every secret value with `[VAULT: key.gpg]`.
   Verify zero matches: `grep -c "18bd7af50624616\|bbdc0cb1895636" SHARED_MEMORY.md` → must be 0.
2. **Commit + push the cleaned version** immediately (limits exposure window).
3. **Make the repo PRIVATE**:
   `gh repo edit <owner>/<repo> --visibility private --accept-visibility-change-consequences`
4. **ROTATE the credential at the source** (exposure = compromised, cannot un-leak):
   - Meta: developers.facebook.com/apps/<APP_ID>/settings/basic/ -> "Reset" next to App secret
     AND in the Threads section -> "Reset" next to Threads app secret.
   - The user generates fresh secrets in the dashboard; agent stores them ONLY in the vault.
5. **Update vault** with the new secret:
   `bash /c/Users/arija/bin/token_vault.sh set fb_app_secret "<new>"`

## Prevention
- Bridge repo created PRIVATE from day one.
- Agent NEVER writes secret values to the bridge — only `[VAULT: key.gpg]` references.
- App IDs (non-secret) are acceptable in the bridge; secrets are not.
- After any bridge edit touching credentials, grep the file for known secret patterns before push.
