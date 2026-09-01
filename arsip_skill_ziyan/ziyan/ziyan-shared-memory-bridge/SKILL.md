---
name: ziyan-shared-memory-bridge
description: Collaborate with other agents via the shared GitHub bridge.
---

# ZIYAN Shared Memory Bridge

## When to use
- Bos: "update shared memory", "biar agent lain tau", "komunikasi dengan Manus/Antigravity", "simpan di GitHub biar agent lain baca".
- You need to tell another agent (Manus AI / Antigravity) about a blocker, a verified result, or a request for help.
- You are handed a task that another agent already touched and you must check what they claimed vs what is true.

## What it is
A GitHub repo used as **ingatan bersama** (shared memory) between the 3 agents Bos:
- **Hermes** (Orkestrator Utama — you)
- **Manus AI** (technical solver, can read GitHub repos)
- **Antigravity / Google** (reader + executor, reads `.gemini/` mirror + git pull)

The bridge is the single source of truth that survives across agent sessions.

## Active repo (verified 15/8/2026)
- **`https://github.com/ziyancorp/ZIYAN_BRIDGE`** — PRIVATE repo.
- Root file: `SHARED_MEMORY.md` (log percakapan antar agent).
- Structure:
  ```
  ZIYAN_BRIDGE/
  ├── SHARED_MEMORY.md          # baca ini dulu — format [Agent → All]
  ├── README.md                 # struktur + aturan keamanan
  └── projects/
      ├── completed/<nama>/HISTORY.md   # proyek selesai
      ├── active/                       # lagi jalan
      ├── blocked/                      # nemu kendala
      └── archive/                      # lama/tidak lanjut
  ```

## Workflow (WRITE side — Hermes)
1. Edit `SHARED_MEMORY.md` (lokal di `C:\Users\arija\ZIYAN_BRIDGE\`).
2. Append a block with explicit sender tag:
   ```
   ### [Hermes → Manus] JUDUL
   fakta / permintaan / bukti.
   LAST SYNC: 2026-08-15 21:30 (Hermes — konteks)
   ```
3. `git add SHARED_MEMORY.md && git commit -m "bridge: ..." && git push`
4. Tell Bos: "sudah di bridge, suruh Manus/AG baca repo".

## MAINTENANCE (cleanup junk before/after updating)
The bridge repo accumulates throwaway scripts from old workflows. They are NOT tracked
by default but `git status` shows them as `??` and they erode trust / mislead other agents.
**Session 2026-08-16 purge list (delete, do NOT commit):**
- `_apply_*.py`, `_delta_*.json`, `_sync_*.py`, `_dbdump_*.py` — delta-apply leftovers from the
  old shared-memory-delta workflow (obsolete since 10 Aug; edits are now direct).
- `_n8n_*` (logs, `*.sqlite`, `deadDB/`, `state_*.txt`) — n8n debug junk.
- `_update_md.py`, `bridge_sync.py`, `build_bridge.py`, `make_snapshot_xlsx.py`, `start_n8n.bat`,
  `update_shared_mem.py` — one-off utility scripts.
- `SHARED_MEMORY.md.bak`, `ZIYAN_MidnightSnapshot_*.xlsx` — backups / snapshots.
**Procedure when Bos says "update shared memory" / "simpan pencapaian":**
1. `cd C:\Users\arija\ZIYAN_BRIDGE`
2. `git status --short` → identify `??` junk; `rm -f` the patterns above (verify they match junk, not real files).
3. Edit/append `SHARED_MEMORY.md` with the achievement (architecture, bugs fixed, verified result, LAST SYNC stamp).
4. `git add SHARED_MEMORY.md && git commit -m "bridge: <topic>" && git push origin main`
5. Confirm to Bos: committed + pushed, repo clean.
**Gotcha:** there is NO `.gitignore` in ZIYAN_BRIDGE — rely on explicit `rm` of known junk patterns,
never a blanket `git add .`. The only tracked files should be `README.md`, `SHARED_MEMORY.md`,
`SHARED_MEMORY.bak.md`, and `projects/**/HISTORY.md`.

## GIT CONFLICT / REBASE PATTERNS (learned 16/8)
- **Rebase opens editor → hangs:** `git rebase --continue` launches an editor (even for a no-edit commit)
  and the foreground command **times out**. FIX: `GIT_EDITOR=true git rebase --continue` (true = no-op
  editor, keeps the commit message) — never run bare `git rebase --continue` in a foreground terminal call.
- **Fast-forward push rejected after local commit:** another agent/Bos pushed to `main` while you edited.
  FIX: `git pull --rebase origin main` (resolves clean if your edits are appended sections) → resolve any
  `<<<<<<<`/`=======`/`>>>>>>>` conflict by **merging BOTH sides** (e.g. Manus's answer + your new section),
  then `GIT_EDITOR=true git rebase --continue` → `git push`.
- **Conflict merge rule:** when merging, KEEP both authors' blocks (don't discard Manus's reply to satisfy
  your append). Strip only the conflict markers. Commit message stays descriptive.
- **Verify pushed:** after `git push` succeeds, check `git log --oneline -1` shows your commit on `main`.

## Workflow (READ side)
- Before trusting another agent's claim, `git pull` then read `SHARED_MEMORY.md`.
- **VERIFY, don't believe.** If agent X says "100% done", test the API yourself (rule #2 Bos). In this session an agent claimed Threads "terpasang & bisa post" but the token was invalid (error 190) and Threads wasn't linked — claim was false until verified.

## Message format rules
- Tags: `[Hermes → All]`, `[Hermes → Manus]`, `[Manus → Hermes]`, `[Hermes → Antigravity]`.
- Always stamp `LAST SYNC:` with timestamp + agent + context.
- Write facts as **verified** (with API proof / post ID) vs **claims** (mark clearly).

## HARD SECURITY RULE (learned the expensive way)
- **NEVER write tokens/secrets to SHARED_MEMORY.md or any GitHub file.** In this session a secret was accidentally pasted into the bridge and pushed to a PUBLIC repo. Fix required: (a) scrub secret from file, (b) `gh repo edit ... --visibility private --accept-visibility-change-consequences`, (c) **reset the leaked secret in the Meta dashboard** (exposed secrets cannot be trusted even after deletion).
- In bridge files, reference secrets as `[VAULT: nama.gpg]`. Real values live in `C:\Users\arija\.hermes\vault\*.gpg` (decrypt: `bash bin/token_vault.sh get <n>`).
- Make the bridge repo **PRIVATE** on first push.

## Related
- Technical case study (Threads API, token types): `references/threads-token-case-study.md`
- Security incident writeup: `references/secrets-in-github-incident.md`
- Token refresh for Meta platforms: see `ziyan-token-lifecycle` (user-owned — adopt via `hermes curator adopt` if you need to extend it).
