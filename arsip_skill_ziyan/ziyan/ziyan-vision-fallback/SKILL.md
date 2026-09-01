---
name: ziyan-vision-fallback
description: When Hermes vision_analyze 404s, use local moondream.
---

# ZIYAN Vision Fallback (Local, No API Key)

## Trigger
- `vision_analyze` returns 404 / "Couldn't find that, sorry"
- `browser_vision` fails on local file
- User says "lihat gambar/video ini" but vision tool errors

## Root cause (this environment)
- Hermes `vision_analyze` 404 = vision route on 9router not responding (model `gemini-2.5-flash` not on 9router; only `gemini-3.6-flash` etc.)
- Config `auxiliary.vision` is **protected** — agent CANNOT edit `~/.hermes/config.yaml` directly (refused with security error). Use `hermes config set` or user edits dashboard.
- Do NOT loop on `vision_analyze` — it will keep 404ing. Switch to local tool.

## Solution: Local open-source vision (moondream DOES NOT WORK here — see below)
**CRITICAL:** Do NOT use moondream. moondream 2.x requires CUDA/MPS and hard-fails on this CPU-only Windows laptop (`RuntimeError: Photon local inference needs a supported accelerator`). Use **SmolVLM** instead.

Full recipe, venv setup, and usage → see skill **`ziyan-local-vision-video`** (curator umbrella). Quick version:
```bash
uv venv --python 3.12 smolvlm_venv
uv pip install --python smolvlm_venv torch torchvision transformers accelerate pillow num2words
# run with env -u PYTHONPATH (global PYTHONPATH polutes venv with broken Hermes PIL)
env -u PYTHONPATH smolvlm_venv/Scripts/python C:\Users\arija\smolvlm_see.py <file> [pertanyaan]
```
Video (audio) → VideoCaptioner: `video-captioner-venv/Scripts/python -m videocaptioner transcribe video.mp4 --asr bijian`

## Pitfalls
- **moondream is DEAD on this laptop** (CUDA/MPS required). Do not install or call it. Use SmolVLM per `ziyan-local-vision-video`.
- Always run venv python with `env -u PYTHONPATH` — global PYTHONPATH leaks Hermes's broken PIL into the venv → `ImportError: cannot import name '_imaging'`.
- Do NOT try to edit `~/.hermes/config.yaml` vision section — protected. Bypass with local tools instead.
- `vision_analyze` on cached image path (e.g. `AppData/Local/hermes/cache/images/img_*.jpg`) 404s even though file exists on disk. Use `smolvlm_see.py` on that path directly.

## When to use which
- Image understanding → `smolvlm_see.py` (SmolVLM)
- Video "what is said / summarized" → VideoCaptioner transcribe
- Video "what is shown" → `smolvlm_see.py` with mp4 (frame extraction)

## Files
- `C:\Users\arija\smolvlm_see.py` — image/video frame VLM helper (SmolVLM)
- `C:\Users\arija\smolvlm_venv\` — uv venv (py3.12) for SmolVLM
- `C:\Users\arija\video-captioner-venv\` — uv venv (py3.12) for VideoCaptioner
- Full detail: skill **`ziyan-local-vision-video`**
