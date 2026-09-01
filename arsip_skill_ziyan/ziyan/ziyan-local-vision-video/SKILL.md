---
name: ziyan-local-vision-video
description: Local vision/video tools when Hermes vision fails.
---

# ZIYAN Local Vision & Video Understanding

## Trigger
- `vision_analyze` / `browser_vision` returns 404 or no response
- Bos sends image/video and asks "what is this" / "watch this"
- Need to read screenshot, photo, or video content locally (no API key)

## Why local
Hermes auxiliary vision (`gemini/gemini-2.5-flash` via 9router) was returning 404 in this environment. Instead of fighting the cloud route, use local open-source models that need no API key.

## Tools (all free, open-source)
| Tool | Role | Stars | Notes |
|---|---|---|---|
| **SmolVLM** (`HuggingFaceTB/SmolVLM-Instruct`) | VLM — reads images, answers questions, CPU-OK | HF | Use `AutoModelForImageTextToText` + `AutoProcessor`. Runs on CPU (float32). Video = extract frames with ffmpeg first. |
| **VideoCaptioner** (1.4.2) | ASR + subtitle + translate + synthesize | 15.6k | Free tier: Bijian ASR + Bing translate, NO API key needed. Needs Python <3.13. |

## Install (Windows, Python 3.14 host — PITFALLS)
Host `python` is 3.14. VideoCaptioner requires `>=3.10,<3.13` → **fails on 3.14**. SmolVLM needs `num2words` + `torchvision` beyond base transformers. Build both with `uv venv --python 3.12`.

### Working recipe (VERIFIED this session — moondream DOES NOT WORK here)
```bash
# 1. SmolVLM — CPU vision. uv venv py3.12 (host py3.14 breaks transformers)
uv venv --python 3.12 smolvlm_venv
uv pip install --python smolvlm_venv torch torchvision transformers accelerate pillow num2words

# 2. VideoCaptioner — needs py<3.13, use uv 3.12 venv
uv venv --python 3.12 video-captioner-venv
uv pip install --python video-captioner-venv videocaptioner
```
- Use `uv pip install --python <venv_dir>` (NOT `-m pip` — uv venvs ship without pip by default → "No module named pip").
- Environment gotcha: a global `PYTHONPATH` points at the Hermes venv (`C:\Users\arija\AppData\Local\hermes\hermes-agent\venv\Lib\site-packages`), so ANY venv resolves Hermes's broken PIL first → `ImportError: cannot import name '_imaging'`. **ALWAYS run with `env -u PYTHONPATH`**:
  `env -u PYTHONPATH smolvlm_venv/Scripts/python smolvlm_see.py <file>`
- SmolVLM also needs `num2words` (processor requirement) and `torchvision` (image backend). Install both.

## Usage
### SmolVLM — see an image (CORRECT, CPU-working)
```bash
env -u PYTHONPATH smolvlm_venv/Scripts/python smolvlm_see.py "C:\path\to\img.jpg" "Baca semua teks yang terlihat."
```
Helper script `C:\Users\arija\smolvlm_see.py` wraps SmolVLM for image OR video (auto frame-extract via ffmpeg). It uses `AutoModelForImageTextToText.from_pretrained("HuggingFaceTB/SmolVLM-Instruct")` + `AutoProcessor`. NOTE: the **Video** variant (`SmolVLM2-500M-Video-Instruct`) errors with MISSING weights on this setup — use the plain `SmolVLM-Instruct` and feed frames manually.
```python
# Key fix: drop pixel_attention_mask before generate(), else ValueError
inputs = {k: v for k, v in inputs.items() if k != "pixel_attention_mask"}
out = model.generate(**inputs, max_new_tokens=256)
```
### SmolVLM — see a video (frame extraction)
```bash
ffmpeg -i video.mp4 -vf fps=0.2 frame_%03d.jpg
# then run smolvlm_see.py on the mp4 (it auto-extracts, max ~10 frames)
```
### VideoCaptioner — transcribe + subtitle (FREE, no key)
```bash
video-captioner-venv/Scripts/python -m videocaptioner transcribe video.mp4 --asr bijian
video-captioner-venv/Scripts/python -m videocaptioner subtitle input.srt --translator bing --target-language en
video-captioner-venv/Scripts/python -m videocaptioner process video.mp4 --target-language ja
```
Note: `videocaptioner` CLI entrypoint may not be on PATH; call via `video-captioner-venv/Scripts/python -m videocaptioner <cmd>`.

## Helper script (created this session)
`C:\Users\arija\smolvlm_see.py` — wraps SmolVLM for image OR video (auto frame-extract via ffmpeg). Run with `env -u PYTHONPATH smolvlm_venv/Scripts/python smolvlm_see.py <file> [pertanyaan]`. (Older `moondream_see.py` in the same dir is dead — moondream does not run on this CPU laptop; ignore it.)

## Pitfalls
- **moondream is DEAD on this laptop.** moondream 2.x (`vl(local=True)` / `VisionModel.from_pretrained`) raises `RuntimeError: Photon local inference needs a supported accelerator, but neither CUDA nor Apple Silicon MPS is available`. This is a CPU-only Windows machine → moondream CANNOT run. Use **SmolVLM** instead. Do not waste time reinstalling moondream.
- **SmolVLM Video variant errors** (`SmolVLM2-500M-Video-Instruct` → MISSING weights at load). Use `SmolVLM-Instruct` + manual frame extraction.
- **PYTHONPATH pollution** — global PYTHONPATH points at Hermes venv broken PIL. Always prefix `env -u PYTHONPATH` before any venv python call, or you get `ImportError: cannot import name '_imaging' from 'PIL'`.
- **VideoCaptioner = audio understanding**, not visual. It transcribes speech → subtitles. Pair with SmolVLM frames for full video comprehension.
- **Python version caps**: VideoCaptioner <3.13, SmolVLM ok on 3.12 via uv. Host python is 3.14 → use `uv venv --python 3.12`.
- **Config.yaml Hermes is protected** — cannot switch vision provider via patch/write_file. If Bos wants Hermes native vision fixed, use `hermes config set` or dashboard `localhost:20128`.

## When to escalate
If Bos wants Hermes `vision_analyze` itself fixed (not a local workaround), that requires editing protected config or 9router Gemini vision setup — recommend Bos do it via dashboard or say so explicitly.
