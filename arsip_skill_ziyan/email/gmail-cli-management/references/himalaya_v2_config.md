# himalaya v2.0.0 — Correct TOML Config (Windows / Gmail)

Verified working on himalaya v2.0.0 (build windows gnu x86_64). Replaces the v1.x syntax shown in the bundled himalaya skill, which errors on v2.0.0.

## Minimal working config (two Gmail accounts)

```toml
[accounts.default]
default = true
email = "arizalkempo@gmail.com"
display-name = "Ari Jal"

[accounts.default.imap]
server = "imap.gmail.com:993"

[accounts.default.imap.sasl.login]
username = "arizalkempo@gmail.com"
password.raw = "APP_PASSWORD_1"

[accounts.default.smtp]
server = "smtp.gmail.com:587"
starttls = true

[accounts.default.smtp.sasl.login]
username = "arizalkempo@gmail.com"
password.raw = "APP_PASSWORD_1"

[accounts.mziyan266]
email = "mziyan266@gmail.com"
display-name = "mziyan266"

[accounts.mziyan266.imap]
server = "imap.gmail.com:993"

[accounts.mziyan266.imap.sasl.login]
username = "mziyan266@gmail.com"
password.raw = "APP_PASSWORD_2"

[accounts.mziyan266.smtp]
server = "smtp.gmail.com:587"
starttls = true

[accounts.mziyan266.smtp.sasl.login]
username = "mziyan266@gmail.com"
password.raw = "APP_PASSWORD_2"

[folder.aliases]
inbox = "INBOX"
sent = "[Gmail]/Sent Mail"
drafts = "[Gmail]/Drafts"
trash = "[Gmail]/Trash"
archive = "[Gmail]/All Mail"
spam = "[Gmail]/Spam"
starred = "[Gmail]/Starred"
important = "[Gmail]/Important"
```

## What v1.x got wrong (do NOT use on v2.0.0)
| v1.x (fails) | v2.0.0 (correct) |
|---|---|
| `imap.port = 993` | `server = "imap.gmail.com:993"` |
| `imap.auth.mechanisms = ["login"]` | (omit — SASL block below) |
| `imap.auth.password = "..."` | `[accounts.X.imap.sasl.login]` → `password.raw` |
| `smtp.starttls = true` | `starttls = true` (under `[accounts.X.smtp]`) |
| `folder list` | `mailbox list` |
| `backend.type = "imap"` | removed (backend inferred) |

## Useful v2.0.0 commands
```bash
himalaya account list
himalaya --account default mailbox list
himalaya --account default envelope list --mailbox INBOX
himalaya --account default envelope list --mailbox INBOX -s 20
```

## Gmail REST backend (optional, needs OAuth2)
App passwords do NOT work for `himalaya gmail ...`. If you need it, the v2.0.0 key is:
```toml
[accounts.default.gmail]
auth.token.raw = "OAUTH2_ACCESS_TOKEN"   # short-lived; refresh is caller's responsibility
```
Until you have a real token, stick to the IMAP backend for all operations.
