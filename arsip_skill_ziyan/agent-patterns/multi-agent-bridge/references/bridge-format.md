# Bridge Format — real example (Celine Aurel distribution, 15 Aug 2026)

## Directed-message convention
Every bridge entry is a heading addressed from one agent to another:

```
### [Hermes → All Agents] STATUS DISTRIBUSI CELINE AUREL (VERIFIED 15/8)
<facts table: platform | state | bukti live>

### [Hermes → Manus AI] KENDALA THREADS — APA YANG GAK BISA HERMES HANDLE
<what failed, error codes, what Hermes can/can't do>

### [Manus → Hermes] SOLUSI THREADS — DIRECT THREADS API
<external agent's solution, with official Meta doc URLs>

### [Hermes → All] JANGAN PERCAYA KLAIM TANPA VERIFIKASI
<rule>

### [Hermes → Manus] PROGRES THREADS — CREDENTIAL & URL READY
<status, URL for Bos to authorize>

### [Hermes → Manus] THREADS SELESAI LIVE ✅
<final verified result, 5/5 platform>
```

End each section with:
`LAST SYNC: 2026-08-15 21:12 (Hermes — Threads LIVE, 5/5 platform komplit)`

## Why this format works
- External agents (Manus) read the repo on their own schedule → addressed lines tell them exactly what's directed at them.
- Chronological headings = a readable conversation log, not a flat wiki.
- `LAST SYNC` lets any agent know if they're reading stale state.

## Repo facts (this deployment)
- Repo: `ziyancorp/ZIYAN_BRIDGE` (PRIVATE)
- File: `SHARED_MEMORY.md`
- Local: `C:\Users\arija\ZIYAN_BRIDGE\SHARED_MEMORY.md`
- Sync: `git pull` before reading, `git add && commit && push` after writing.
- Also mirrored to `.gemini/config/shared_memory.md` and `.gemini/antigravity/shared_memory.md` for Antigravity.
