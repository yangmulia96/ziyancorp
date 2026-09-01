# Himalaya v2.0.0 — Worked Config (live-verified)

Two Gmail accounts, App Passwords, full `[Gmail]` folder aliases.
This exact file was written to `C:\Users\arija\.config\himalaya\config.toml`
and passed `himalaya account list` + `himalaya mailbox list` for BOTH accounts.

```toml
[accounts.default]
default = true
email = "arizalkempo@gmail.com"
display-name = "Ari Jal"

[accounts.default.imap]
server = "imap.gmail.com:993"

[accounts.default.imap.sasl.login]
username = "arizalkempo@gmail.com"
password.raw = "APP_PASSWORD_A"

[accounts.default.smtp]
server = "smtp.gmail.com:587"
starttls = true

[accounts.default.smtp.sasl.login]
username = "arizalkempo@gmail.com"
password.raw = "APP_PASSWORD_A"

[accounts.mziyan266]
email = "mziyan266@gmail.com"
display-name = "mziyan266"

[accounts.mziyan266.imap]
server = "imap.gmail.com:993"

[accounts.mziyan266.imap.sasl.login]
username = "mziyan266@gmail.com"
password.raw = "APP_PASSWORD_B"

[accounts.mziyan266.smtp]
server = "smtp.gmail.com:587"
starttls = true

[accounts.mziyan266.smtp.sasl.login]
username = "mziyan266@gmail.com"
password.raw = "APP_PASSWORD_B"

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

## What went wrong before (the v1 schema that fails on v2)

Each of these produced `TOML parse error … unknown field`:

1. `[accounts.N].imap.auth.mechanisms = ["login"]` → v2 has no `imap.auth`,
   only `imap.sasl.login` / `imap.sasl.plain`.
2. `[accounts.N].imap.port = 993` → v2 puts port inside the `server`
   string: `server = "host:port"`. `port` is **not** a key of `[imap]`.
3. `smtp.starttls = true` placed as `[accounts.N].smtp.starttls`? No — the
   failing form was `imap.starttls = false` and `smtp.starttls`; on v2
   `starttls` must be a **direct field** of `[smtp]`, e.g. `[smtp] starttls = true`,
   and there is no `starttls` key under `[imap]` unless you set it explicitly.
   For IMAP over 993 (implicit TLS) omit `starttls` entirely.

## Install + verify recipe (Windows)

```bash
curl -sL -o himalaya.zip \
  "https://github.com/pimalaya/himalaya/releases/latest/download/himalaya.x86_64-windows.zip"
unzip -o himalaya.zip
mv himalaya.exe "$HOME/AppData/Local/hermes/bin/"
export PATH="$HOME/AppData/Local/hermes/bin:$PATH"
himalaya --version                       # confirm v2.0.0
himalaya account list                     # both accounts appear
himalaya --account default mailbox list   # INBOX + [Gmail]/* present
```
