
import os, json, shutil, subprocess, textwrap, re
from pathlib import Path

# ---- CONFIG ----
PEXELS_API_KEY = "F9f4KvZlReqd7klXaknvf6zPpbT00GrD62LUUojmvxUV5DwuWzCFj21h"
PIXABAY_API_KEY = "57267312-9c26b138313d3dedf51fca0a7"
GEMINI_API_KEY = "AQ.Ab8RN6Jh-jeCGKc3YTcSuVsaHUrVonnc4mUeJGqvAtbmGSd9mQ"
DRIVE_OUTPUT = "/content/drive/MyDrive/ZIYANCORP_AI_FACTORY"

data = {"id": "WILDLIFE_001", "topic_title": "Peregrine Falcon: The 390 KM/H Biological Missile", "hook_sentence": "This bird falls faster than a Ferrari at top speed!", "script_lines": ["Meet the Peregrine Falcon, the undisputed fastest creature on Earth.", "When diving for prey, it folds its wings and reaches an astonishing 390 kilometers per hour.", "Special baffles inside its nostrils act as jet engine diffusers, allowing it to breathe at extreme velocity.", "Its target never hears it coming until the fatal mid-air strike.", "Nature engineered the ultimate supersonic predator millions of years before humans built airplanes."], "search_keyword": "falcon flying dramatic", "youtube_title": "The Fastest Animal on Earth Falls at 390 KM/H! 🦅 #Shorts", "youtube_description": "Discover the incredible speed and anatomy of the Peregrine Falcon diving at 390 km/h.\n\n#wildlife #peregrinefalcon #fastestanimal #nature4k #animalfacts", "youtube_tags": ["peregrine falcon", "fastest animal", "wildlife", "predator", "nature shorts", "animal facts 4k"], "slot_time": "10:34", "status": "READY"}
topic_title   = data["topic_title"]
hook_sentence = data["hook_sentence"]
script_lines  = data["script_lines"]
search_kw     = data["search_keyword"]
safe_name     = re.sub(r"[^a-zA-Z0-9_]", "_", topic_title)[:40]

print(f"STARTING PRODUCTION: {{topic_title}}")

# ---- INSTALL DEPS ----
subprocess.run(["pip", "install", "-q", "pydub", "edge-tts", "Pillow", "requests", "google-generativeai"], check=True)
import requests
from PIL import Image, ImageDraw, ImageFont
import asyncio, edge_tts
from pydub import AudioSegment

# ---- FETCH STOCK VIDEOS ----
os.makedirs("/content/clips", exist_ok=True)
os.makedirs(DRIVE_OUTPUT, exist_ok=True)

def fetch_pexels_videos(query, max_clips=6):
    headers = {"Authorization": PEXELS_API_KEY}
    url = f"https://api.pexels.com/videos/search?query={{query}}&per_page=15&size=large"
    r = requests.get(url, headers=headers, timeout=30)
    videos = r.json().get("videos", [])
    clips = []
    for v in videos:
        if len(clips) >= max_clips:
            break
        for f in v.get("video_files", []):
            if f.get("quality") in ("hd", "uhd") and f.get("width", 0) >= 1080:
                try:
                    vid_url = f["link"]
                    fname = f"/content/clips/clip_{{len(clips)}}.mp4"
                    r2 = requests.get(vid_url, timeout=60, stream=True)
                    with open(fname, "wb") as fp:
                        for chunk in r2.iter_content(chunk_size=1024*1024):
                            fp.write(chunk)
                    clips.append(fname)
                    break
                except Exception as ex:
                    print(f"Clip download failed: {{ex}}")
                    continue
    return clips

print("Fetching 4K wildlife footage from Pexels...")
clips = fetch_pexels_videos(search_kw, max_clips=8)
print(f"Got {{len(clips)}} clips")

# ---- GENERATE TTS VOICE ----
all_lines = [hook_sentence] + script_lines
full_script = " ".join(all_lines)

print("Generating Christopher Neural narration...")
voice_file = f"/content/voice_{{safe_name}}.mp3"

async def gen_voice():
    communicate = edge_tts.Communicate(full_script, voice="en-US-ChristopherNeural", rate="-5%")
    await communicate.save(voice_file)

asyncio.get_event_loop().run_until_complete(gen_voice())
voice_audio = AudioSegment.from_mp3(voice_file)
total_duration_ms = len(voice_audio)
total_duration_sec = total_duration_ms / 1000.0
print(f"Voice duration: {{total_duration_sec:.1f}}s")

# ---- FETCH BACKGROUND MUSIC ----
bgm_file = "/content/bgm.mp3"
bgm_urls = [
    "https://cdn.pixabay.com/download/audio/2022/10/18/audio_2e60f8d01b.mp3",
    "https://cdn.pixabay.com/download/audio/2023/03/22/audio_c8b8dfe0f9.mp3",
    "https://cdn.pixabay.com/download/audio/2022/08/02/audio_884fe92c21.mp3",
]
for bgm_url in bgm_urls:
    try:
        r = requests.get(bgm_url, timeout=30)
        if r.status_code == 200:
            with open(bgm_file, "wb") as f:
                f.write(r.content)
            print("BGM downloaded.")
            break
    except Exception:
        continue

# ---- TRIM AND CONCATENATE CLIPS ----
per_clip = max(3.0, total_duration_sec / max(len(clips), 1))
clip_trimmed_list = []
for i, clip in enumerate(clips):
    out = f"/content/trimmed_{{i}}.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-i", clip,
        "-t", str(per_clip + 1),
        "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1",
        "-c:v", "libx264", "-crf", "23", "-preset", "fast",
        "-an", out
    ], capture_output=True)
    if os.path.exists(out) and os.path.getsize(out) > 10000:
        clip_trimmed_list.append(out)

concat_file = "/content/concat_list.txt"
with open(concat_file, "w") as f:
    for c in clip_trimmed_list:
        f.write(f"file '{{c}}'\n")

raw_video = "/content/raw_video.mp4"
subprocess.run([
    "ffmpeg", "-y", "-f", "concat", "-safe", "0",
    "-i", concat_file,
    "-t", str(total_duration_sec + 1),
    "-c:v", "libx264", "-crf", "22", "-preset", "fast",
    raw_video
], capture_output=True)
print(f"Raw video created: {{os.path.getsize(raw_video)/(1024*1024):.2f}} MB")

# ---- GENERATE SUBTITLE FRAMES (Yellow Badge Style) ----
print("Generating yellow-badge subtitle overlays...")

def make_subtitle_images(lines_with_times):
    font_path = None
    # Try to install and use a bold font
    try:
        subprocess.run(["apt-get", "install", "-y", "-q", "fonts-open-sans"], capture_output=True)
        font_path = "/usr/share/fonts/truetype/open-sans/OpenSans-ExtraBold.ttf"
        if not os.path.exists(font_path):
            font_path = None
    except Exception:
        pass
    
    subtitle_clips = []
    for idx, (line, start_t, end_t) in enumerate(lines_with_times):
        words = line.upper().split()
        chunks = [" ".join(words[i:i+4]) for i in range(0, len(words), 4)]
        chunk_dur = (end_t - start_t) / max(len(chunks), 1)
        
        for ci, chunk in enumerate(chunks):
            t_start = start_t + ci * chunk_dur
            t_end   = t_start + chunk_dur
            img_path = f"/content/sub_{{idx}}_{{ci}}.png"
            
            W, H = 1080, 1920
            img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            try:
                font_size = 72
                if font_path and os.path.exists(font_path):
                    font = ImageFont.truetype(font_path, font_size)
                else:
                    font = ImageFont.load_default()
            except Exception:
                font = ImageFont.load_default()
            
            # Get text size
            bbox = draw.textbbox((0, 0), chunk, font=font)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]
            
            pad_x, pad_y = 32, 18
            radius = 22
            rect_w = tw + pad_x * 2
            rect_h = th + pad_y * 2
            rx = (W - rect_w) // 2
            ry = H // 2 + 400  # Bottom third of screen
            
            # Draw yellow rounded rectangle
            draw.rounded_rectangle([rx, ry, rx + rect_w, ry + rect_h],
                                    radius=radius, fill="#FFE000")
            
            # Draw black text
            draw.text((rx + pad_x, ry + pad_y), chunk, font=font, fill="#000000")
            
            img.save(img_path, "PNG")
            subtitle_clips.append((img_path, t_start, t_end))
    
    return subtitle_clips

# Estimate timing per line
approx_wpm = 140
total_words = sum(len(l.split()) for l in all_lines)
times = []
t = 0
for line in all_lines:
    words = len(line.split())
    dur = (words / approx_wpm) * 60 * 1.1
    times.append((line, t, t + dur))
    t += dur

subtitle_data = make_subtitle_images(times)
print(f"Generated {{len(subtitle_data)}} subtitle overlay chunks")

# ---- OVERLAY SUBTITLES WITH FFMPEG FILTER COMPLEX ----
print("Compositing subtitles onto video...")
temp_video = "/content/subbed_video.mp4"

# Build overlay filter chain
filter_parts = []
current = "[0:v]"
for i, (img_path, t_start, t_end) in enumerate(subtitle_data):
    next_label = f"[v{{i}}]" if i < len(subtitle_data) - 1 else "[vout]"
    filter_parts.append(
        f"{{current}}[{{i+1}}:v] overlay=(W-w)/2:(H-h)/2*1+400:enable='between(t,{{t_start:.2f}},{{t_end:.2f}})'{{next_label}}"
    )
    current = next_label

filter_str = ";".join(filter_parts)
inputs = ["-i", raw_video]
for img_path, _, _ in subtitle_data:
    inputs += ["-i", img_path]

subprocess.run([
    "ffmpeg", "-y",
    *inputs,
    "-filter_complex", filter_str,
    "-map", "[vout]",
    "-t", str(total_duration_sec),
    "-c:v", "libx264", "-crf", "22", "-preset", "fast",
    "-an", temp_video
], capture_output=True)
print(f"Subtitled video: {{os.path.getsize(temp_video)/(1024*1024):.2f}} MB")

# ---- MIX AUDIO (Voice + BGM Duck) ----
print("Mixing audio: voiceover + ambient BGM...")
bgm_audio = AudioSegment.from_mp3(bgm_file)
bgm_looped = bgm_audio * (int(total_duration_ms / len(bgm_audio)) + 2)
bgm_looped = bgm_looped[:total_duration_ms]
bgm_looped = bgm_looped - 18  # Duck BGM by 18dB under voice

mixed = voice_audio.overlay(bgm_looped)
mixed_file = "/content/mixed_audio.mp3"
mixed.export(mixed_file, format="mp3", bitrate="192k")
print("Audio mix done.")

# ---- FINAL MERGE VIDEO + AUDIO ----
final_file = f"/content/{{safe_name}}.mp4"
subprocess.run([
    "ffmpeg", "-y",
    "-i", temp_video,
    "-i", mixed_file,
    "-c:v", "libx264", "-crf", "20", "-preset", "fast",
    "-c:a", "aac", "-b:a", "192k",
    "-movflags", "+faststart",
    "-shortest", final_file
], capture_output=True)

# ---- COPY TO GOOGLE DRIVE ----
drive_path = f"{{DRIVE_OUTPUT}}/{{safe_name}}.mp4"
shutil.copy(final_file, drive_path)

sz = os.path.getsize(drive_path) / (1024*1024)
print("=" * 60)
print("PRODUCTION COMPLETE!")
print(f"File: {{drive_path}} ({{sz:.2f}} MB)")
print("=" * 60)
print(f"READY_FILE:{{safe_name}}.mp4")
