# Cron-mode terminal gotchas — parallel HN fetch

This note captures a host quirk that broke the Hacker News item-fetch step during a
Compound Daily pipeline cron run, and the working fix.

## What failed
The research fetch step needs the top ~25 HN story JSONs (`hn_<id>.json`). The
obvious parallel patterns both FAIL in this host's foreground `terminal` call:

1. **Shell `&` + `wait` backgrounding** — rejected outright:
   ```
   Foreground command uses '&' backgrounding. Use terminal(background=true) ...
   ```
2. **`xargs`<->`xargs` `-I{} -P` combo** — `xargs` warns the flags are mutually
   exclusive and ignores `--max-args`, so only **1** file is written instead of 25.
3. **Sequential `for id in $ids; do curl; done`** — works but is ~500s (25 × 20s
   timeout), exceeding the foreground command timeout. Too slow.

(`execute_code` is also blocked for subprocess in cron mode — documented in SKILL.md.)

## Working fix
Use an on-disk Python script with `ThreadPoolExecutor` (8 workers), invoked via
`terminal python3 ...`. It is bundled as **`scripts/fetch_hn.py`**:

```bash
cd /c/Users/<user>/research        # where hn_top.json lives
python3 scripts/fetch_hn.py        # writes hn_<id>.json for top 25 (parallel, fast)
```

`fetch_hn.py` resolves `hn_top.json` from cwd or its own dir, fetches the top 25
items with an 8-worker pool, and reports ok/bad counts. Run it AFTER fetching
`hn_top.json` (see the Google News / HN parallel-fetch block in this file's parent).

## Why this matters
The trending-topics pipeline runs unattended from cron. Any step that silently
writes 1/25 files (the `xargs` case) or errors (`&`) produces a half-populated
`hn_*.json` set, which the parser still runs on — yielding a research brief with
weak/absent HN viral signals. Always use `scripts/fetch_hn.py`, never shell `&`
or `xargs -I{} -P`, for HN item fetches in cron/foreground-terminal contexts.
