---
name: ziyan-media-gen-cli
description: Install & run AI image/video CLIs for ZIYAN on Windows.
---

# ZIYAN — AI Media Generation CLI

Use when the user wants to generate images / videos / 3D / audio from the terminal via
external AI CLIs, or asks to "set up X CLI", or asks whether a media-gen tool is free or paid.
Covers Higgsfield (paid aggregator) and Nano Banana / Gemini API (free tier) as the first
concrete examples; extend with more tools as ZIYAN adopts them.

## Workflow
1. **Verify the exact package name first.** User-pasted install commands frequently contain
   typos, `@file:` artifacts, or unclosed quotes → npm 404. Strip `@file:` prefix, confirm the
   real scoped name via `npm view <name> version` before installing.
2. **Install global npm CLI.** If `postinstall` downloads a binary and fails on Windows, use
   `npm i -g <pkg> --ignore-scripts`, then download + extract the binary manually (recipe in
   references/higgsfield.md — the pattern generalizes to any CLI that ships a Go/Rust binary
   via GitHub Releases).
3. **Companion skills.** Install locally; NEVER `--global` for PromptScript-based skill repos
   (`--global` errors with "PromptScript does not support global skill installation"). Always
   pass `--yes` to avoid the interactive multi-select prompt.
4. **Auth.** CLIs that use browser OAuth should be launched in a background terminal so the
   loopback listener stays alive while the user signs in; hand the user the printed URL. Watch
   for server-side scope bugs that block login (vendor issue, not local setup).
5. **Pricing / monetization check.** Before committing ZIYAN budget, confirm free tier
   (Gemini API free quota covers Nano Banana image gen) vs paid credit models (Higgsfield).

## Pitfalls (verified this session)
- Don't trust `@file:` prefix in pasted commands — it is a copy artifact, not a valid npm spec.
- `npx skills add <repo> --global` fails for PromptScript skills; use
  `npx --yes skills add <repo> --yes` (local → symlinks into `~/.agents/skills/`, Hermes Agent reads it).
- Higgsfield v1.1.20 `auth login` FAILS server-side: Clerk rejects scope `user:org:read`
  ("The requested scope is invalid... not allowed to request scope 'user:'"). Wait for vendor
  fix or log in via web + supply token manually. Not a local setup defect.
- When `web_search` tool is unavailable and `browser_navigate` times out, verify pricing/
  availability by fetching with `curl -sSL --compressed <url>` and stripping tags via Python
  `urllib` + `re` (recipe in references/higgsfield.md).

## References
- `references/higgsfield.md` — exact install recipe (incl. Windows postinstall workaround),
  companion-skill command, auth scope bug detail, and verified pricing facts.
