# Vault Decrypt Pattern (`.gpg` tokens)

## Location
Encrypted tokens: `~/.hermes/vault/*.gpg`
Helper script: `~/bin/token_vault.sh` (AES256 GPG symmetric)

## Decrypt (no manual passphrase prompt)
```bash
cd ~
TOK=$(bash bin/token_vault.sh get threads_token 2>/dev/null | tr -d '\n')
echo "$TOK"
```
Passphrase auto-read from `~/.hermes/.env` (`VAULT_PASS=...`).

## Raw GPG (if script unavailable)
```bash
gpg --batch --yes --passphrase "$VAULT_PASS" -d .hermes/vault/threads_token.gpg
```
NEVER run bare `gpg --decrypt file.gpg` without `--passphrase` in non-interactive shell — it hangs ~25s waiting for stdin.

## Validate after decrypt
A decrypted token may be EXPIRED. Always hit the API:
```bash
curl -s -m15 "https://graph.threads.net/v1.0/me?access_token=$TOK"
# error 190 "Session has expired" => token dead, re-auth needed
```

## Inventory (2026-08-15 state)
| Token | Decrypt | API Valid? |
|-------|---------|-----------|
| threads_token.gpg | OK | EXPIRED (10-Jul-26) |
| fb_page_token.gpg | OK | EXPIRED (10-Jul-26) |
| fb_user_token.gpg | OK | EXPIRED (10-Jul-26) |
| youtube_token_celineaurel.json | n/a (plain) | VALID |

## Don't search for "lost" tokens
Deep search (disk, GitHub, Antigravity logs, Hermes history) found: IG token never persisted
plain-text; Threads only in expired .gpg. Re-auth instead of hunting.
