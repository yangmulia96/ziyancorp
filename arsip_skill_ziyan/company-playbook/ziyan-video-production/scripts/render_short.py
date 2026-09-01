#!/usr/bin/env python3
"""
render_short.py - Offline (no API key) vertical Shorts render pipeline.
JALUR B ZIYAN. Terverifikasi produksi (short 1080x1920, <=60s, edge-tts id-ID).

Usage (Windows/git-bash — WAJIB path absolut, jangan pakai ~):
    python "C:/Users/arija/AppData/Local/hermes/skills/company-playbook/ziyan-video-production/scripts/render_short.py" \
        "C:/path/naskah.json" --out "C:/path/short_02.mp4"
Atau via uv jika paket belum ada:
    uv run --with edge-tts --with pillow python render_short.py <script.json> [--out output.mp4]

Script JSON structure:
    {
        "title": "...",
        "scenes": [
            {"narration": "spoken text", "on_screen": "short on-screen text"},
            ...
        ],
        "voice": "id-ID-ArdiNeural"
    }

Outputs compact JSON to stdout:
    {"output_path": ..., "duration_sec": ..., "size_bytes": ..., "scenes": ..., "tts_engine": ...}
TTS fallback chain: edge-tts -> pyttsx3 -> silent. Duration guard MAX_TOTAL_SEC=60.
Verifikasi wajib setelah render: ffprobe -show_entries format=duration:stream=codec_name,width,height.
"""
import argparse
import asyncio
import json
import os
import shutil
import subprocess
import sys
import tempfile
import textwrap

W, H = 1080, 1920
MAX_TOTAL_SEC = 60.0
FONT_BOLD = r"C:\Windows\Fonts\arialbd.ttf"
FONT_REG = r"C:\Windows\Fonts\arial.ttf"


def log(*a):
    print(*a, file=sys.stderr, flush=True)


def ffprobe_duration(path):
    out = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", path
    ], text=True).strip()
    return float(out)


# ---------- TTS ----------
def tts_edge(text, voice, out_mp3):
    import edge_tts
    async def _run():
        comm = edge_tts.Communicate(text, voice)
        await comm.save(out_mp3)
    asyncio.run(_run())
    if not os.path.exists(out_mp3) or os.path.getsize(out_mp3) == 0:
        raise RuntimeError("edge-tts produced empty file")


def tts_pyttsx3(text, out_wav):
    import pyttsx3
    eng = pyttsx3.init()
    eng.save_to_file(text, out_wav)
    eng.runAndWait()
    if not os.path.exists(out_wav) or os.path.getsize(out_wav) == 0:
        raise RuntimeError("pyttsx3 produced empty file")


def make_silent(out_wav, seconds):
    subprocess.check_call([
        "ffmpeg", "-y", "-f", "lavfi", "-i",
        f"anullsrc=r=44100:cl=stereo", "-t", str(seconds),
        out_wav
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def make_scene_audio(narration, voice, workdir, idx):
    """Return (audio_path, engine_used). Tries edge-tts -> pyttsx3 -> silent."""
    mp3 = os.path.join(workdir, f"aud_{idx}.mp3")
    try:
        tts_edge(narration, voice, mp3)
        return mp3, "edge-tts"
    except Exception as e:
        log(f"[scene {idx}] edge-tts failed: {e}")
    wav = os.path.join(workdir, f"aud_{idx}.wav")
    try:
        tts_pyttsx3(narration, wav)
        return wav, "pyttsx3"
    except Exception as e:
        log(f"[scene {idx}] pyttsx3 failed: {e}")
    # silent fallback: ~ estimate reading time
    words = max(1, len(narration.split()))
    secs = max(2.0, words / 2.5)
    make_silent(wav, secs)
    return wav, "silent"


# ---------- Frame ----------
def make_frame(on_screen, title, scene_no, total_scenes, out_png):
    from PIL import Image, ImageDraw, ImageFont
    img = Image.new("RGB", (W, H))
    px = img.load()
    # dark vertical gradient
    top = (14, 18, 32)
    bot = (40, 20, 55)
    for y in range(H):
        t = y / (H - 1)
        r = int(top[0] + (bot[0] - top[0]) * t)
        g = int(top[1] + (bot[1] - top[1]) * t)
        b = int(top[2] + (bot[2] - top[2]) * t)
        for x in range(W):
            px[x, y] = (r, g, b)
    draw = ImageDraw.Draw(img)

    font_main = ImageFont.truetype(FONT_BOLD, 78)
    try:
        font_title = ImageFont.truetype(FONT_REG, 42)
    except Exception:
        font_title = font_main

    # title top
    if title:
        tw = draw.textlength(title, font=font_title)
        draw.text(((W - tw) / 2, 120), title, font=font_title, fill=(150, 160, 190))

    # wrap on-screen text
    wrapped = textwrap.wrap(on_screen, width=18) or [""]
    line_h = 96
    total_h = line_h * len(wrapped)
    y0 = (H - total_h) // 2
    for i, line in enumerate(wrapped):
        lw = draw.textlength(line, font=font_main)
        draw.text(((W - lw) / 2, y0 + i * line_h), line, font=font_main, fill=(245, 245, 250))

    # thin progress bar near bottom
    bar_y = H - 160
    bar_h = 8
    margin = 80
    draw.rectangle([margin, bar_y, W - margin, bar_y + bar_h], fill=(70, 70, 90))
    frac = scene_no / total_scenes
    draw.rectangle([margin, bar_y, margin + int((W - 2 * margin) * frac), bar_y + bar_h],
                   fill=(120, 200, 255))

    img.save(out_png)


# ---------- Per-scene video ----------
def make_scene_video(png, audio, out_mp4):
    dur = ffprobe_duration(audio)
    subprocess.check_call([
        "ffmpeg", "-y",
        "-loop", "1", "-i", png,
        "-i", audio,
        "-c:v", "libx264", "-tune", "stillimage", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "128k",
        "-t", f"{dur}",
        "-r", "30",
        "-shortest",
        out_mp4
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return ffprobe_duration(out_mp4)


def concat(scene_mp4s, out_mp4, workdir):
    listfile = os.path.join(workdir, "concat.txt")
    with open(listfile, "w") as f:
        for m in scene_mp4s:
            f.write(f"file '{m.replace(chr(92), '/')}'\n")
    subprocess.check_call([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", listfile,
        "-c", "copy", out_mp4
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("script")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    with open(args.script, encoding="utf-8") as f:
        data = json.load(f)

    title = data.get("title", "")
    scenes = data["scenes"]
    voice = data.get("voice", "id-ID-ArdiNeural")
    n = len(scenes)
    if n == 0:
        log("No scenes."); sys.exit(1)

    out_path = args.out
    if not out_path:
        base = os.path.splitext(os.path.basename(args.script))[0]
        out_path = os.path.abspath(base + ".mp4")
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)

    workdir = tempfile.mkdtemp(prefix="rendershort_")
    engines = set()
    scene_mp4s = []
    try:
        for i, sc in enumerate(scenes, 1):
            log(f"Scene {i}/{n} ...")
            audio, eng = make_scene_audio(sc.get("narration", ""), voice, workdir, i)
            engines.add(eng)
            png = os.path.join(workdir, f"frame_{i}.png")
            make_frame(sc.get("on_screen", ""), title, i, n, png)
            smp4 = os.path.join(workdir, f"scene_{i}.mp4")
            make_scene_video(png, audio, smp4)
            scene_mp4s.append(smp4)

        # duration check before concat
        total = sum(ffprobe_duration(m) for m in scene_mp4s)
        if total > MAX_TOTAL_SEC:
            log(f"ERROR: total duration {total:.1f}s > {MAX_TOTAL_SEC}s limit.")
            sys.exit(2)

        concat(scene_mp4s, out_path, workdir)
        final_dur = ffprobe_duration(out_path)
        if final_dur > MAX_TOTAL_SEC:
            log(f"ERROR: final duration {final_dur:.1f}s > {MAX_TOTAL_SEC}s limit.")
            sys.exit(2)

        result = {
            "output_path": out_path,
            "duration_sec": round(final_dur, 2),
            "size_bytes": os.path.getsize(out_path),
            "scenes": n,
            "tts_engine": sorted(engines),
        }
        print(json.dumps(result, ensure_ascii=False))
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


if __name__ == "__main__":
    main()
