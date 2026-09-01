# Case: NotebookLM autopilot E2E run, 2026-08-02

Full pipeline `nb_autopilot.py` (CDP-driven NotebookLM Video Overview) →
`upload_pipeline.py` (YouTube upload). First end-to-end run.

## Stage results
| Stage | Status | Evidence |
|---|---|---|
| CDP reachable | OK | `curl -s http://127.0.0.1:9222/json/version` → Chrome/151 (Brave) |
| Cookie load | OK | 70 entries from `storage_state.json` (values never printed) |
| Session logged in | OK | `--dry-run` rendered real NotebookLM UI + account label |
| Create notebook | OK | click `partial:create new` |
| Insert source | OK | click `partial:website` → `exact:insert`, 60s settle |
| Trigger Video Overview | OK | click `partial:video overview` → `exact:generate` |
| Render | OK | ~2.5 min, three "still rendering" polls |
| Download | **FAILED** | printed `SELESAI (auto-download): ...\_ctest.mp4`; `ziyan_videos/` had no MP4, Downloads had nothing new |
| Upload | correctly skipped | `upload_pipeline.py --max 1` → "no new MP4" |

## Root cause
Completion was inferred from DOM text. `_ctest.mp4` was a guessed name, not a real
download filename. No `Browser.downloadProgress` subscription existed, so a never-
finishing (or never-starting) transfer looked identical to a successful one.

## What caught it
Running `ls -la` on the output directory immediately after the "success" line, plus a
`find -newermt` sweep over Downloads. Both empty → the log line was a lie.

## Prescribed fix
See the CDP download pattern in SKILL.md: `allowAndName` +
`downloadWillBegin` → `downloadProgress state == "completed"` → rename guid to
`suggestedFilename` → size assertion.

## Incidental setup gap
`websocket-client` was absent from the default interpreter; CDP scripts aborted with
`[FATAL] butuh websocket-client`. Fixed with `python -m pip install websocket-client`.

## Reporting lesson
The honest report ("generate OK, download failed, upload correctly refused, here is the
root cause and the fix") was more actionable than a binary pass/fail, and let the owning
agent ship a targeted patch.
