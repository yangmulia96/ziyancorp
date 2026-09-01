"""
AutoTube Shorts Factory — Backend HTTP API Server
Dipanggil oleh n8n via HTTP Request Node.

ENDPOINTS:
  POST /generate-short
    Body JSON: {
      "niche": "Tech & AI",
      "script": "Teks narasi full...",
      "scenes": [
        {"text": "...", "image_prompt": "..."},
        ...
      ],
      "title": "Judul video untuk YouTube",
      "description": "Deskripsi YouTube"
    }
  GET /status
    Cek apakah server hidup.
  POST /publish
    Body JSON: {
      "video_path": "C:/path/to/video.mp4",
      "title": "...",
      "description": "...",
      "platforms": ["youtube", "telegram", "facebook", "instagram"]
    }
"""
import asyncio
import json
import os
import sys
import traceback
import uuid
from http.server import BaseHTTPRequestHandler, HTTPServer

import requests
from PIL import Image, ImageDraw
import numpy as np
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips

sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
OUTPUT_DIR = os.path.join(PROJECT_DIR, "tmp_assets")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load .env
env_path = os.path.join(PROJECT_DIR, ".env")
ENV = {}
if os.path.exists(env_path):
    for line in open(env_path):
        if "=" in line and not line.strip().startswith("#"):
            k, v = line.strip().split("=", 1)
            ENV[k.strip()] = v.strip()


# ─── TTS ────────────────────────────────────────────────────────────────────

async def _tts_async(text: str, output_mp3: str, voice: str = "id-ID-ArdiNeural"):
    from edge_tts import Communicate
    c = Communicate(text, voice)
    await c.save(output_mp3)


def generate_tts(text: str, output_mp3: str, voice: str = "id-ID-ArdiNeural"):
    asyncio.run(_tts_async(text, output_mp3, voice))


# ─── IMAGE ──────────────────────────────────────────────────────────────────

def fetch_image(prompt: str, idx: int, img_path: str):
    enc = requests.utils.quote(prompt)
    url = f"https://pollinations.ai/p/{enc}?width=1080&height=1920&seed={idx+100}&model=flux&nologo=true"
    try:
        r = requests.get(url, timeout=15)
        if r.status_code == 200 and len(r.content) > 5000:
            with open(img_path, "wb") as f:
                f.write(r.content)
            print(f"  ✅ Scene {idx+1} image downloaded.")
            return
    except Exception as e:
        print(f"  ⚠️ Image fetch failed ({e}), using synthetic canvas.")
    # Fallback: synthetic dark 9:16 gradient canvas
    canvas = Image.new("RGB", (1080, 1920), color=(10, 15, 30))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle([40, 40, 1040, 1880], outline=(56, 189, 248), width=6)
    draw.text((100, 900), prompt[:60], fill=(200, 220, 255))
    canvas.save(img_path)


# ─── RENDER ─────────────────────────────────────────────────────────────────

def render_short(scenes: list, output_mp4: str, voice: str = "id-ID-ArdiNeural") -> str:
    clips = []
    temp_files = []

    for idx, scene in enumerate(scenes):
        img_path = os.path.join(OUTPUT_DIR, f"_tmp_img_{idx}.jpg")
        audio_path = os.path.join(OUTPUT_DIR, f"_tmp_audio_{idx}.mp3")
        temp_files += [img_path, audio_path]

        fetch_image(scene.get("image_prompt", "cinematic 9:16 background"), idx, img_path)
        generate_tts(scene["text"], audio_path, voice)

        pil_img = Image.open(img_path).convert("RGB")
        img_np = np.array(pil_img)
        audio_clip = AudioFileClip(audio_path)
        img_clip = (
            ImageClip(img_np)
            .with_duration(audio_clip.duration)
            .with_audio(audio_clip)
        )
        clips.append(img_clip)

    final = concatenate_videoclips(clips, method="compose")
    final.write_videofile(output_mp4, fps=24, codec="libx264", audio_codec="aac", logger=None)

    for tf in temp_files:
        if os.path.exists(tf):
            os.remove(tf)

    return output_mp4


# ─── PUBLISH ────────────────────────────────────────────────────────────────

def publish_video(video_path: str, title: str, description: str, platforms: list) -> dict:
    results = {}
    sys.path.insert(0, PROJECT_DIR)

    # --- Telegram ---
    if "telegram" in platforms:
        try:
            token = ENV.get("BOT_TOKEN") or ENV.get("TELEGRAM_BOT_TOKEN")
            channel = ENV.get("CHANNEL_CELINE", "")
            with open(video_path, "rb") as vf:
                r = requests.post(
                    f"https://api.telegram.org/bot{token}/sendVideo",
                    data={"chat_id": channel, "caption": f"🎬 {title}\n\n{description[:800]}"},
                    files={"video": vf},
                    timeout=120,
                )
            results["telegram"] = "ok" if r.ok else r.text[:200]
        except Exception as e:
            results["telegram"] = f"error: {e}"

    # --- Facebook ---
    if "facebook" in platforms:
        try:
            page_id = ENV.get("FB_PAGE_ID")
            page_token = ENV.get("FB_PAGE_TOKEN")
            with open(video_path, "rb") as vf:
                r = requests.post(
                    f"https://graph-video.facebook.com/v21.0/{page_id}/videos",
                    data={"description": f"{title}\n{description}", "access_token": page_token},
                    files={"source": vf},
                    timeout=180,
                )
            results["facebook"] = "ok" if r.ok else r.json()
        except Exception as e:
            results["facebook"] = f"error: {e}"

    # --- YouTube (via existing uploader) ---
    if "youtube" in platforms:
        try:
            uploader_path = os.path.join(PROJECT_DIR, "youtube_upload_celine.py")
            import subprocess
            proc = subprocess.run(
                [sys.executable, uploader_path,
                 "--file", video_path,
                 "--title", title,
                 "--description", description,
                 "--category", "22",
                 "--privacyStatus", "public"],
                capture_output=True, text=True, timeout=300, cwd=PROJECT_DIR
            )
            results["youtube"] = "ok" if proc.returncode == 0 else proc.stderr[:300]
        except Exception as e:
            results["youtube"] = f"error: {e}"

    return results


# ─── HTTP SERVER ─────────────────────────────────────────────────────────────

class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        print(f"[API] {self.address_string()} - {format % args}")

    def send_json(self, data: dict, code: int = 200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/status":
            self.send_json({"status": "ok", "service": "autotube-shorts-factory"})
        else:
            self.send_json({"error": "not found"}, 404)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        try:
            payload = json.loads(body)
        except Exception:
            self.send_json({"error": "invalid json"}, 400)
            return

        if self.path == "/generate-short":
            try:
                scenes = payload.get("scenes", [])
                title = payload.get("title", "AutoTube Short")
                description = payload.get("description", "")
                voice = payload.get("voice", "id-ID-ArdiNeural")
                output_name = f"short_{uuid.uuid4().hex[:8]}.mp4"
                output_mp4 = os.path.join(OUTPUT_DIR, output_name)
                print(f"\n🎬 Generating Short: {title} ({len(scenes)} scenes)...")
                render_short(scenes, output_mp4, voice)
                self.send_json({
                    "status": "success",
                    "video_path": output_mp4,
                    "title": title,
                    "description": description,
                })
            except Exception as e:
                traceback.print_exc()
                self.send_json({"status": "error", "message": str(e)}, 500)

        elif self.path == "/publish":
            try:
                video_path = payload.get("video_path", "")
                title = payload.get("title", "AutoTube Short")
                description = payload.get("description", "")
                platforms = payload.get("platforms", ["telegram"])
                if not os.path.exists(video_path):
                    self.send_json({"status": "error", "message": f"video not found: {video_path}"}, 400)
                    return
                print(f"\n🚀 Publishing: {title} → {platforms}")
                results = publish_video(video_path, title, description, platforms)
                self.send_json({"status": "success", "results": results})
            except Exception as e:
                traceback.print_exc()
                self.send_json({"status": "error", "message": str(e)}, 500)
        else:
            self.send_json({"error": "unknown endpoint"}, 404)


if __name__ == "__main__":
    PORT = int(os.environ.get("AUTOTUBE_PORT", 7860))
    print(f"🚀 AutoTube Shorts Factory API running on http://localhost:{PORT}")
    print(f"   Endpoints:")
    print(f"   GET  /status")
    print(f"   POST /generate-short  — build 9:16 MP4 from scenes")
    print(f"   POST /publish         — push video to platforms")
    server = HTTPServer(("0.0.0.0", PORT), Handler)
    server.serve_forever()
