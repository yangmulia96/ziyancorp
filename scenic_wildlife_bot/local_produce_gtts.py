#!/usr/bin/env python3
"""
Produksi 3 Video Short - TTS pakai gTTS + FFmpeg
"""
import subprocess, sys, json, time, os, asyncio
from pathlib import Path
from gtts import gTTS

ROOT = Path(r"C:\Users\arija\ziyancorp\scenic_wildlife_bot")
OUTPUT = ROOT / "output_videos"
OUTPUT.mkdir(parents=True, exist_ok=True)

def get_meta(i):
    meta_file = ROOT / f"pending_meta_{i}.json"
    if meta_file.exists():
        with open(meta_file) as f:
            return json.load(f)
    return None

def create_video(search_keyword, audio_mp3, output_mp4, i=None):
    try:
        import requests
        api_key = "F9f4KvZlReqd7klXaknvf6zPpbT00GrD62LUUojmvxUV5DwuWzCFj21h"
        query = search_keyword.replace(" ", "+")
        url = f"https://api.pexels.com/videos/search?query={query}&per_page=1&orientation=vertical&size=large"
        headers = {"Authorization": api_key}
        resp = requests.get(url, headers=headers, timeout=15)
        data = resp.json()
        
        if data.get("videos") and len(data["videos"]) > 0:
            video_url = data["videos"][0]["video_files"][0]["link"]
            footage = OUTPUT / f"footage_{i}.mp4"
            subprocess.run(["curl", "-L", "-o", str(footage), video_url], timeout=60, check=True)
            
            result = subprocess.run([
                "ffprobe", "-v", "error", "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1", str(audio_mp3)
            ], capture_output=True, text=True)
            dur = float(result.stdout.strip())
            
            out = OUTPUT / output_mp4
            subprocess.run([
                "ffmpeg", "-y", "-i", str(footage), "-i", str(audio_mp3),
                "-vf", "scale=1080:1920,crop=1080:1920",
                "-c:v", "libx264", "-c:a", "aac", "-shortest", "-pix_fmt", "yuv420p",
                str(out)
            ], check=True, timeout=120)
            print(f"  Video: {out}")
            return out
        print(f"  No footage for '{search_keyword}'")
        return None
    except Exception as e:
        print(f"  Video error: {e}")
        return None

def main():
    print("=" * 60)
    print("3 VIDEO SHORT - LOCAL RENDER (gTTS + FFmpeg)")
    print("=" * 60)
    
    metas = []
    for i in range(1, 4):
        m = get_meta(i)
        if m:
            metas.append((i, m))
            print(f"\n{i}. {m['topic_title']}")
            print(f"   YT: {m['youtube_title']}")
            print(f"   Hook: {m['hook_sentence'][:80]}...")
    
    print("\n" + "=" * 60)
    print("RENDERING...")
    print("=" * 60)
    
    for i, m in metas:
        print(f"\nVideo {i}: {m['topic_title']}")
        
        audio = OUTPUT / f"audio_{i}.mp3"
        try:
            tts = gTTS(text=m["hook_sentence"], lang="id", slow=False)
            tts.save(str(audio))
            print(f"  TTS: {audio}")
        except Exception as e:
            print(f"  TTS failed: {e}")
            continue
        
        mp4 = f"short_{i}.mp4"
        video = create_video(m["search_keyword"], audio, mp4, i)
        if video:
            print(f"  OK: {video}")
    
    print("\nSelesai!")

if __name__ == "__main__":
    main()