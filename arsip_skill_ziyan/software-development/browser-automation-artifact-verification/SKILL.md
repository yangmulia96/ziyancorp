---
name: browser-automation-artifact-verification
description: Verify browser-automation output on disk, not from DOM text.
version: 1.0.0
---

# Browser Automation: Artifact Verification

Use when a script drives a browser (CDP, Playwright, Selenium) to **produce a file** —
download a video/PDF/export, save a render, scrape-to-file — and you must report whether
it worked. The failure mode this skill prevents: the script prints `DONE` / `SELESAI`
because a DOM node appeared, while nothing ever landed on disk.

## Core rule
**Success = a file on disk with size > 0.** UI text, a spinner disappearing, a button
becoming enabled, or a filename scraped from the DOM are all *hints*, never proof.
Never report success to the user from a log line alone — always `ls -la <outdir>` (or
`os.path.getsize`) first, and compare against a pre-run snapshot of the directory.

## Correct CDP download pattern
Scraping a filename out of the DOM produces bogus names (real case: a script reported
`_ctest.mp4`, which never existed). Use the download events instead:

1. `Browser.setDownloadBehavior` with `behavior: "allowAndName"`, an explicit
   `downloadPath`, and `eventsEnabled: true`.
2. Subscribe to `Browser.downloadWillBegin` → capture `guid` and `suggestedFilename`.
3. Poll/await `Browser.downloadProgress` until `state == "completed"` for that `guid`.
   Treat `state == "canceled"` as a hard failure.
4. With `allowAndName` the file lands as `<downloadPath>/<guid>` (no extension) →
   rename to `suggestedFilename`.
5. Assert `os.path.getsize(final_path) > 0`, then report.

Playwright equivalent: `with page.expect_download() as dl:` then
`dl.value.save_as(path)` — `save_as` blocks until the transfer finishes, so it is
already safe; the anti-pattern is clicking and then sleeping.

## Pipeline discipline
- Split the run into `generate` and `consume` stages with the disk check between them.
- The consuming stage should **fail loudly and refuse to proceed** when no new artifact
  exists (e.g. "no new MP4 found") rather than uploading a stale file. That behaviour is
  correct, not a bug — if you see it, debug the producer.
- Give the producer a `--dry-run` flag that only validates connectivity + session and
  creates nothing. Run it first; it isolates auth failures from generation failures in
  one cheap step.

## Pitfalls
- A long render can outlive the tool's foreground timeout. Run the producer as a
  background process with completion notification and poll it, instead of shortening
  the wait and declaring failure.
- CDP scripts need `websocket-client` in the *same* interpreter you invoke:
  `python -m pip install websocket-client`. A `[FATAL] butuh websocket-client` line is a
  setup gap, not a broken pipeline.
- Verify the port is really speaking CDP before blaming the script:
  `curl -s http://127.0.0.1:9222/json/version`.
- When the artifact is missing, also check the browser's default Downloads folder — the
  download may have succeeded but ignored your `downloadPath`.
- Report honestly per stage. "Generate OK, download failed, upload correctly skipped" is
  far more useful than a single pass/fail verdict.

## References
- `references/notebooklm-download-false-positive.md` — full stage-by-stage transcript of
  the 2026-08-02 NotebookLM run where the false-positive was first caught.
