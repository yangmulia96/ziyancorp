---
name: windows-script-paths
description: "Python path pitfalls on the Windows git-bash host."
version: 1.0.0
author: Hermes Orchestrator
license: MIT
platforms: [windows]
---

# Windows git-bash Terminal vs Windows-native Python — Path Semantics

On this host the Hermes `terminal` runs **git-bash/MSYS**, so `/c/Users/...` works in EVERY shell command (curl, ls, mkdir, cp). But `python3` launched from that shell is the **Windows-native** interpreter, which does NOT understand MSYS `/c/...` paths the way the shell does.

## ⚠️ PITFALL — absolute `/c/...` inside a `.py` silently misplaces files (terbukti 2026-08-14)
Writing `WORKDIR = "/c/Users/arija/workdir/videos/2026-08-14b"` inside a Python script, then `os.makedirs(WORKDIR)` / `open(os.path.join(WORKDIR, ...))` → Windows-native python treats `/c/Users/arija/...` as **relative to the current drive root**, so it actually writes to `C:\c\Users\arija\workdir\videos\2026-08-14b\` (note the EXTRA `c`).

**Symptom:** the script prints "OK / WROTE file", but `ls` in the correct terminal path shows NOTHING and `read_file` reports "File not found". The files exist — just one directory level too deep (`C:\c\...` instead of `C:\...`). This burned a full research+staging run before the misplacement was spotted.

### FIX (apply in every on-disk script)
- **Prefer relative paths**: since the terminal is already `cd`'d into the working dir, use `WORK = "."` inside the script and pass fetched files by plain name. Run the script FROM that dir.
- **OR use a real Windows path**: `WORKDIR = r"C:\Users\arija\workdir\videos\2026-08-14b"` (raw string, backslashes). Windows-native python understands this.
- **NEVER** put `/c/Users/...` literals inside `.py` source. `/c/...` is only valid in *terminal* commands, not inside Python's `open()`/`os` calls.
- **Verify after every script run**: `ls -la <correct_absolute_path>` via terminal. Do NOT trust a script's "OK" print — confirm the file is at the expected location. If missing, check `C:\c\Users\...` (the misplaced twin).

## Subprocess rules (cron-mode safety)
- `execute_code` is **blocked for subprocess calls** — use `terminal()` `curl` to fetch, then an **on-disk `.py`** (run via terminal) to parse. Do not shell out from execute_code.
- Parallel fetches: issue several `terminal()` calls in ONE turn (runtime runs them concurrently). Do NOT use `&` backgrounding inside a single foreground `terminal()` call (error: "Foreground command uses '&' backgrounding"). Chain sequentially with `&&` instead.

## Diagnosis recipe (file "missing" after script said OK)
1. `find /c/c -name "<filename>" 2>/dev/null` — the misplaced twin lives under `C:\c\...`.
2. `cp` it to the correct `C:\Users\...` location, then fix the script to use `.` or `C:\...` before the next run.

## References
- `references/path-misplacement-repro.md` — exact 2026-08-14 transcript (write `/c/` path → lands in `C:\c\`, symptom, fix).
