---
name: hermes-voice-hud
description: Deploy a free local JARVIS voice HUD over Hermes.
---

# Hermes Voice HUD (JARVIS-style Dashboard)

## Trigger
- User asks for "JARVIS", "voice HUD", "mission control", or a browser UI over Hermes.

## What it is
`Itsme23476/jarvis-hermes-dashboard` — a thin local web HUD (Python `http.server` + vanilla JS) that drives the EXISTING Hermes CLI as its brain. Inherits Hermes tools, skills, memory, MCP. Binds `127.0.0.1:8730`. MIT.

## 100% FREE (no ElevenLabs)
Browser Web Speech API (Chrome/Edge) gives voice in/out with NO API key. ElevenLabs is optional + paid — skip it.

### Steps (Windows)
1. `git clone https://github.com/Itsme23476/jarvis-hermes-dashboard.git jarvis-dashboard`
2. `.env` in clone root:
   ```
   HERMES_CMD=C:\Users\arija\AppData\Local\hermes\hermes-agent\venv\Scripts\hermes.exe
   JARVIS_VOICE_MODE=browser
   JARVIS_PORT=8730
   ```
   No `ELEVENLABS_API_KEY` → browser fallback auto-engages.
3. Launch: `cd C:\Users\arija\jarvis-dashboard && python server.py` (background).
4. Verify: `curl -s http://127.0.0.1:8730/api/status` → `"runtime":"hermes"`.

## Pitfalls
- No requirements.txt — stdlib only, no `pip install`.
- Set `HERMES_CMD` explicitly or runtime falls back to `python3 -m hermes_cli.main` (may not resolve under MSYS).
- Grant mic permission to `127.0.0.1` in browser site settings for voice input.
- Local-only by design — never expose 8730.

## Files
`server.py` (HTTP+NDJSON), `runtime.py` (Hermes subprocess), `voice.py` (ElevenLabs/browser), `commands.py` (slash matrix), `persona.md` (JARVIS tone), `ui/` (HUD).
