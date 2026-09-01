---
name: image-verification-fallback
description: Vision fails on image? Recover via profiling and OCR.
---

# Image Verification Fallback

When the vision tool fails, the agent must NOT hallucinate the image contents. This skill is the deterministic recovery path.

## Hard rule
If you did not actually see the image (vision error / 404 / empty), say so explicitly and recover via the steps below. Never describe what "might" be in the image as fact.

## TRIGGER — the user tells you to find/use a skill
If the user says "cari skill", "pakai skill", "bukankah ada skill untuk itu", or similar: **SEARCH IMMEDIATELY** via `skills_list` + `skill_view`. Do NOT argue that no skill exists, do NOT say "tidak ada skill". This session the agent repeatedly argued against an existing skill (this one) while the user insisted — the skill existed; the failure was not searching. The cost was the user's repeated frustration ("dari tadi aku suruh kamu cari skill... kamu bantah terus"). Rule: user hinting at a skill = load it first, then assess.

## TRIGGER — images sent through the chat gateway (Discord/Telegram/WhatsApp)
When the user attaches an image in chat and you must read it: **LOAD THIS SKILL FIRST.** On this host `vision_analyze` returns 404 because the active model has no native vision. **NEVER suggest `computer_use`** to read gateway attachments — `computer_use` drives the LOCAL Windows desktop and cannot see files the user sent via chat. This was repeatedly suggested and explicitly corrected; do not repeat it. Go straight to OCR (`references/discord-image-ocr.md`).

## Step 1 — Confirm the file is a real image
```
file "<path>.png"
```
Expect: `PNG image data, <W>x<H>, 8-bit/color RGBA, non-interlaced`. If it decodes, the file is valid even though vision can't read it.

## Step 2 — Pixel profile (cheap, tells you the KIND of image)
Use the Hermes venv python (has PIL). Run a color histogram:
```python
from PIL import Image
from collections import Counter
img = Image.open(r"<path>").convert("RGB")
px = list(img.getdata())
cnt = Counter(px)
avg = tuple(sum(p[i] for p in px)//len(px) for i in range(3))
print("SIZE", img.size)
for c,n in cnt.most_common(5): print(c, f"{100*n/len(px):.1f}%")
print("AVG", avg, "=>", "DARK/UI" if avg[0]<120 else "LIGHT/DOC")
```
Interpretation:
- 90%+ white + thin gray → **document / text on white** (screenshot of a webpage, settings page, or text doc)
- Dominant dark navy/blurple (~`(54,57,63)`) → **Discord UI**
- Mixed saturated colors → **photo / app with brand colors**

This does NOT read text — it only classifies, which is enough to decide next step.

## Step 3 — OCR recovery (when you need the actual text)
vision_analyze failing means you likely need the text. Use tesseract.

### Install (one-time, Windows)
```
winget install -e --id UB-Mannheim.TesseractOCR -h --accept-package-agreements --accept-source-agreements
```
Binary lands at `C:\Program Files\Tesseract-OCR\tesseract.exe`.

### CRITICAL: do NOT use the Hermes venv for OCR
The Hermes agent venv (`hermes-agent/venv`) has **no pip and a partially-broken PIL** (`cannot import name '_imaging'`). Installing there fails. Instead build an isolated venv with `uv`:
```
cd /tmp
uv venv ocr_env
uv pip install --python ocr_env pytesseract pillow
uv run --python ocr_env python ocr_script.py
```
### OCR script
```python
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
from PIL import Image
img = Image.open(r"<path>")
img = img.resize((img.width*2, img.height*2))  # upscale helps accuracy
print(pytesseract.image_to_string(img).strip())
```
Expected output for a clean doc screenshot: the actual text (e.g. `Ollama version 0.32.4`).

## Step 4 — Decide on the recovered content
Once you have the text/profile, act on it (manipulate, delete, report). In the session that spawned this skill, a screenshot of Windows "Apps & Features" showing `Ollama version 0.32.4` was recovered via OCR, classified as a doc, and the (now-redundant) source PNG was deleted — the information was already known.

## Pitfalls
- `vision_analyze` 404 is an environment/transient failure, NOT proof the image is empty. Always attempt recovery before concluding.
- Never `rm` an image you haven't identified. Classify + OCR first.
- **9router proxy models are ALL text-only or image-GENERATION.** No model in models9r.json (71 models, channels gemini/groq/kimi/kr/openrouter/root) can READ images. `gemini/` channel is dead (400 invalid key) anyway. So do NOT try to route screenshots through 9router for vision — use OCR below. See `references/9router_vision_audit.md` for the exact model-list audit proving all 6 vision-capable models live in the dead `gemini/` channel.
- **Active Hermes model (tencent/hy3:free) has NO native vision** -> vision_analyze hits aux model which 404s. OCR is the only reliable recovery path for this user.
- **Do NOT suggest computer_use for reading images the user sends via Discord** — computer_use drives the local Windows desktop, it cannot read attachment files. That was a wrong recommendation given repeatedly; stop offering it for image-reading.
- **Tesseract is ALREADY installed** at `C:\Program Files\Tesseract-OCR\tesseract.exe` on this host. Skip the winget install step. Hermes venv PIL is broken (`_imaging` import error) -> always use `uv venv ocr_env` + `uv pip install pillow pytesseract` then `uv run --python ocr_env`.

## Working OCR recipe (verified on this host)
```bash
cd /c/Users/arija
uv venv ocr_env
uv pip install --python ocr_env pytesseract pillow
cat > ocr_script.py <<'PY'
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
from PIL import Image
img = Image.open(r"<path>").resize((img.width*2, img.height*2))
print(pytesseract.image_to_string(img).strip())
PY
uv run --python ocr_env python ocr_script.py
```
This successfully recovered a Google Cloud Console "You need additional access" error screenshot that vision_analyze could not read.
Or run the bundled helper: `python scripts/ocr_recover.py <image_path>` (creates ocr_env automatically).
- PowerShell one-liners with `@{...}` break under git-bash/MSYS escaping — use `tasklist | grep`, `du -sh`, or `df -h` (POSIX) instead of complex `Get-Process` pipelines.
- The Hermes venv has no pip module (`python -m pip` fails) — use `uv` for any ad-hoc Python dependency.
- **PDFs from the user are NOT images** — do NOT OCR them. Use `pdftotext` (at `/mingw64/bin/pdftotext`, already present) directly: `pdftotext -layout "<file>.pdf" -`. React/JSX exports from Gemini Canvas arrive this way; extract, strip the leading ```react and trailing ``` markers, fix latin-1 bytes (`open(p,encoding='latin-1')`), then save as `.jsx`. This recovered a full ZYN AI Corp landing-page component this session.
- **CRITICAL unwrap step for code-in-PDF:** `pdftotext -layout` HARD-WRAPS lines at ~80 cols, which **splits string literals mid-word and truncates the file** (App_gemini.jsx arrived cut off at line 469, breaking the build). After extraction, run an unwrap pass: join lines that are clearly continuations of a string/statement (e.g. a line ending without `;`, `}`, or `>` and the next starting lowercase/quote), OR simpler — copy the raw text into a proper editor/VSCode and let Prettier/ESLint re-wrap. If the build fails with "unexpected EOF / string literal truncated", the PDF wrap is the cause. The sub-agent fixed this by writing a temporary unwrap script + manually rewriting the missing tail (cards, footer, CTA).

## Verification
After OCR, read the printed text back to the user and confirm before any destructive action (delete/move) on the source file.

## Support files
- `references/discord-image-ocr.md` — gateway-image OCR recipe (verified this host): Tesseract already installed, broken venv PIL, 9router has no vision models, `pdftotext` for PDFs, GCP-error recovery example.
