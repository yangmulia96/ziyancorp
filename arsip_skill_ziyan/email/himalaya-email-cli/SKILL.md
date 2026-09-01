---
name: himalaya-email-cli
description: "Manage IMAP/SMTP email from terminal with himalaya v2."
version: 1.0.0
author: curator
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Email, IMAP, SMTP, CLI, Terminal]
---

# Himalaya Email CLI (v2.x)

Terminal email client over IMAP/SMTP. Use when Bos wants to read, list,
search, reply, forward, or send email without leaving the terminal.

> **VERSION-SKEW WARNING (first-class pitfall).** The *bundled* `himalaya`
> skill documents the **v1.2.0** config schema
> (`backend.type/host/port`, `backend.auth.raw`, `message.send.backend.*`).
> The binary on this box is **`himalaya v2.0.0`**, whose config keys differ.
> If `himalaya account list` fails with `TOML parse error … unknown field`,
> the config is using the wrong schema — **do not trust the bundled doc**.
> Fix: fetch the sample for the installed version and mirror its keys:
>
> ```bash
> curl -sL https://github.com/pimalaya/himalaya/archive/refs/heads/master.zip -o h.zip
> unzip -o h.zip
> sed -n '1,400p' himalaya-master/config.sample.toml   # authoritative schema
> ```

## Install (Windows x86_64)

```bash
# Release binary — no cargo/rust needed.
curl -sL -o himalaya.zip \
  "https://github.com/pimalaya/himalaya/releases/latest/download/himalaya.x86_64-windows.zip"
unzip -o himalaya.zip
# puts himalaya.exe in ./ (and ./result/bin/)
mv himalaya.exe "$HOME/AppData/Local/hermes/bin/"
export PATH="$HOME/AppData/Local/hermes/bin:$PATH"
himalaya --version      # verify; note the version for schema matching
```

## Config (v2.0.0 — WORKING, verified live)

Full worked example lives in `references/config-v2-worked.md`; copy-ready
template in `templates/config.toml.v2`. Key shape:

```toml
[accounts.default]
default = true
email = "user@gmail.com"
display-name = "Your Name"

[accounts.default.imap]
server = "imap.gmail.com:993"

[accounts.default.imap.sasl.login]
username = "user@gmail.com"
password.raw = "APP-PASSWORD"      # Gmail needs an App Password (2FA on)

[accounts.default.smtp]
server = "smtp.gmail.com:587"
starttls = true                    # DIRECT field under [smtp], NOT smtp.starttls

[accounts.default.smtp.sasl.login]
username = "user@gmail.com"
password.raw = "APP-PASSWORD"

[folder.aliases]                   # unchanged from v1.2.0 — still folder.aliases.X
inbox = "INBOX"
sent = "[Gmail]/Sent Mail"
drafts = "[Gmail]/Drafts"
trash = "[Gmail]/Trash"
```

Schema deltas vs the bundled v1.2.0 doc:
- `backend.type/host/port` + `backend.encryption.type` → **single `server = "host:port"`**
  under `[accounts.NAME.imap]` / `[accounts.NAME.smtp]`.
- `backend.auth.raw` → **`[accounts.NAME.imap.sasl.login]`** with `username`+`password.raw`.
- `message.send.backend.*` → merged into `[accounts.NAME.smtp]` + `[smtp.sasl.login]`.
- `starttls` is a **direct field** of `[smtp]` (or `[imap]`), never `smtp.starttls`.

## Common Operations (v2 subcommands)

```bash
himalaya account list                                   # list configured accounts
himalaya --account default mailbox list                 # folders (v2: 'mailbox', NOT 'folder')
himalaya --account default envelope list --mailbox INBOX
himalaya --account default envelope list from boss@x.com subject invoice
himalaya --account default message read 42
himalaya --account default attachment download 42
# Compose non-interactively (pipe via stdin):
cat <<'EOF' | himalaya template send
From: user@gmail.com
To: recipient@x.com
Subject: Test

Body here.
EOF
himalaya --account mziyan266 envelope list --mailbox INBOX   # switch account
```

## Pitfalls

- **`folder` is gone in v2** → use `mailbox`. `himalaya folder list` →
  `error: unrecognized subcommand 'folder'`.
- **Backup before rewriting config**: `cp config.toml config.toml.v1.bak`.
- **Gmail 2FA** requires an App Password, not the account password.
- **Multiple accounts**: pass `--account <name>`; the `default = true`
  account is used when omitted.
- Config resolves from `$HOME/.config/himalaya/config.toml`.

## Verification (run after any config change)

```bash
himalaya account list                       # must print the account table
himalaya --account default mailbox list     # must list INBOX + [Gmail]/* folders
```
Both must succeed before claiming email access works.
