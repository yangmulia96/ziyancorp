#!/usr/bin/env python3
"""
Produksi 3 Video Short - gTTS + Pexels + FFmpeg (LOCAL)
"""
import subprocess, sys, json, time, os, threading
from pathlib import Path

ROOT = Path(r"C:\Users\arija\ziyancorp\scenic_wildlife_bot")
OUTPUT = ROOT / "output_videos"
OUTPUT.mkdir(parents=True, exist_ok=True)

def get_meta(i):
    meta_file = ROOT / f"pending_meta_{i}.json"
    if meta_file.exists():
        with open(meta_file) as f:
            return json.load(f)
    return None

def generate_tts(text, output_mp3):
    try:
        from gtts import gTTS
        tts = gTTS(text=text, lang="en", slow=False)
        tts.save(str(output_mp3))
        print(f"  TTS: {output_mp3}")
        return True
    except Exception as e:
        print(f"  TTS gagal: {e}")
        return False

def download_footage(keyword, output_mp4):
    try:
        import requests
        api_key = "F9f4KvZlReqd7klXaknvf6zPpbT00GrD62LUUojmvxUV5DwuWzCFj21h"
        query = keyword.replace(" ", "+")
        url = f"https://api.pexels.com/videos/search?query={query}&per_page=1&orientation=vertical&size=large"
        headers = {"Authorization": api_key}
        resp = requests.get(url, headers=headers, timeout=15)
        data = resp.json()
        
        if data.get("videos") and len(data["videos"]) > 0:
            video_url = data["videos"][0]["video_files"][0]["link"]
            subprocess.run(["curl", "-L", "-o", str(output_mp4), video_url], timeout=60, check=True)
            size = os.path.getsize(output_mp4)
            print(f"  Footage: {output_mp4} ({size} bytes)")
            return output_mp4
        print(f"  No footage for '{keyword}'")
        return None
    except Exception as e:
        print(f"  Download error: {e}")
        return None

def compose_video(footage_mp4, audio_mp3, output_mp4):
    try:
        result = subprocess.run([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(audio_mp3)
        ], capture_output=True, text=True)
        audio_dur = float(result.stdout.strip())
        
        out = OUTPUT / output_mp4
        subprocess.run([
            "ffmpeg", "-y", "-i", str(footage_mp4), "-i", str(audio_mp3),
            "-vf", "scale=1080:1920,crop=1080:1920",
            "-c:v", "libx264", "-c:a", "aac", "-shortest", "-pix_fmt", "yuv420p",
            "-t", str(audio_dur),
            str(out)
        ], check=True, timeout=180)
        size = os.path.getsize(out)
        print(f"  Video: {out} ({size} bytes)")
        return out
    except Exception as e:
        print(f"  FFmpeg error: {e}")
        return None

def main():
    print("=" * 70)
    print("PRODUKSI 3 VIDEO SHORT - LOCAL RENDER")
    print("=" * 70)
    
    metas = []
    for i in range(1, 4):
        m = get_meta(i)
        if m:
            metas.append((i, m))
            print(f"\n{i}. {m['topic_title']}")
            print(f"   YT: {m['youtube_title']}")
            print(f"   Hook: {m['hook_sentence'][:80]}...")
    
    print("\n" + "=" * 70)
    print("RENDERING...")
    print("=" * 70)
    
    for i, m in metas:
        print(f"\n▶ Video {i}: {m['topic_title']}")
        
        # TTS
        audio_mp3 = OUTPUT / f"audio_{i}.mp3"
        if not generate_tts(m["hook_sentence"], audio_mp3):
            print(f"  ❌ TTS gagal")
            continue
        
        # Footage
        footage_mp4 = OUTPUT / f"footage_{i}.mp4"
        footage = download_footage(m["search_keyword"], footage_mp4)
        if not footage:
            print(f"  ⚠️  Tidak ada footage")
            continue
        
        # Video
        out_mp4 = f"short_{i}.mp4"
        video = compose_video(footage_mp4, audio_mp3, out_mp4)
        if video:
            print(f"  ✅ VIDEO SIAP!")
            slot = "15:48 WIB" if i == 1 else ("20:23 WIB" if i == 2 else "10:34 WIB (besok)")
            print(f"   → YouTube: {m['youtube_title']}")
            print(f"   → Slot: {slot}")
    
    print("\n" + "=" * 70)
    print("SELESAI!")
    print("=" * 70)
    for f in OUTPUT.glob("short_*.mp4"):
        print(f"  {f.name}")

if __name__ == "__main__":
    main()