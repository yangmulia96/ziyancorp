"""
Scenic Wildlife Full Local Production & Scheduling Engine
Generates 4K YouTube Shorts with:
1. Gemini-powered viral script
2. Edge-TTS voiceover
3. Pexels HD/4K nature stock clips
4. Animated/Styled subtitle overlays
5. Ambient background music mixing
6. FFmpeg 1080x1920 video composition
7. YouTube Data API v3 upload & scheduling
"""
import os
import sys
import json
import asyncio
import requests
import subprocess
import datetime
import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import edge_tts
from google import genai
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

ROOT = Path(r"C:\Users\arija\ziyancorp\scenic_wildlife_bot")
TOKEN_PATH = ROOT / "token_scenic_wildlife.json"
PRODUCTION_LOG = ROOT / "production_log.json"
USED_TOPICS_FILE = ROOT / "used_topics.json"
OUTPUT_DIR = ROOT / "output_videos"
OUTPUT_DIR.mkdir(exist_ok=True)

PEXELS_API_KEY = "F9f4KvZlReqd7klXaknvf6zPpbT00GrD62LUUojmvxUV5DwuWzCFj21h"
GEMINI_API_KEY = "AQ.Ab8RN6Jh-jeCGKc3YTcSuVsaHUrVonnc4mUeJGqvAtbmGSd9mQ"

FFMPEG = r"C:\Users\arija\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin\ffmpeg.EXE"

# Royal royalty-free ambient documentary audio tracks
BGM_URLS = [
    "https://cdn.pixabay.com/download/audio/2022/10/18/audio_2e60f8d01b.mp3",
    "https://cdn.pixabay.com/download/audio/2023/03/22/audio_c8b8dfe0f9.mp3",
    "https://cdn.pixabay.com/download/audio/2022/08/02/audio_884fe92c21.mp3",
]


def load_used_topics():
    if USED_TOPICS_FILE.exists():
        with open(USED_TOPICS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_used_topic(topic_title):
    used = load_used_topics()
    used.append(topic_title)
    with open(USED_TOPICS_FILE, "w", encoding="utf-8") as f:
        json.dump(used, f, ensure_ascii=False, indent=2)


def generate_wildlife_topic():
    """Generate 1 viral wildlife documentary topic and script using Gemini."""
    used_topics = load_used_topics()
    used_str = "\n".join(f"- {t}" for t in used_topics[-30:]) if used_topics else "(none yet)"

    prompt = f"""You are an elite viral YouTube Shorts content strategist specializing in GLOBAL 4K nature and wildlife documentaries.

Your task: Generate ONE new, unique, emotionally powerful wildlife/nature fact video concept that has strong potential to go viral on YouTube Shorts globally (US, UK, Australia, India).

STRICT REQUIREMENTS:
1. Topic must NOT be any of these already-used topics:
{used_str}

2. Topic must tap into STRONG HUMAN EMOTIONS: awe, heartbreak, wonder, shock, hope, or disbelief.
3. Apply "Cognitive Gap" - the hook must shatter a common assumption (e.g. "This animal that looks deadly... is actually protecting you")
4. Apply "Anthropomorphism" - show human-like qualities in the animal (love, loyalty, grief, sacrifice, friendship)
5. Apply "Open Loop" - withhold the most shocking fact until the final 10 seconds
6. Apply "Seamless Loop" - the last sentence must connect perfectly back to the first sentence

OUTPUT FORMAT (return ONLY valid JSON, no explanation, no markdown):
{{
  "topic_title": "Short title for internal tracking",
  "youtube_title": "Full YouTube title with emotional hook and 2-3 hashtags (max 100 chars)",
  "hook_sentence": "The very FIRST sentence (0-3 sec). Must cause immediate curiosity or shock. MAX 12 words.",
  "script_lines": [
    "Line 1 (3-8 sec): Expand the hook. Set the scene emotionally.",
    "Line 2 (8-14 sec): Introduce the deeper context or backstory.",
    "Line 3 (14-20 sec): Build emotional tension. Drop a surprising detail.",
    "Line 4 (20-28 sec): The story's turning point. Viewer must feel something.",
    "Line 5 (28-36 sec): Reveal the key fact/behavior that is mind-blowing.",
    "Line 6 (36-44 sec): THE OPEN LOOP PAYOFF - the most jaw-dropping moment.",
    "Line 7 (44-50 sec): Philosophical or emotional closing line. Connects back to hook."
  ],
  "search_keyword": "Best 3-word Pexels/Pixabay search keyword for relevant 4K footage (e.g. 'ocean whale underwater')",
  "youtube_description": "Full YouTube description (200-250 words) with storytelling, hashtags, and channel CTA for @4kscenicwildlife",
  "youtube_tags": ["tag1", "tag2", "tag3", "tag4", "tag5", "tag6", "tag7", "tag8", "tag9", "tag10"]
}}"""

    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )
    raw = response.text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()
    data = json.loads(raw)
    return data


async def generate_voiceover(text: str, output_path: Path):
    """Generate professional voiceover using Edge TTS."""
    communicate = edge_tts.Communicate(text, voice="en-US-ChristopherNeural", rate="-2%")
    await communicate.save(str(output_path))


def get_audio_duration(audio_path: Path) -> float:
    """Get audio duration in seconds using ffprobe/ffmpeg."""
    cmd = [
        FFMPEG, "-i", str(audio_path),
        "-f", "null", "-"
    ]
    res = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    # Parse Duration: 00:00:45.32
    m = re.search(r"Duration:\s*(\d+):(\d+):([\d\.]+)", res.stderr)
    if m:
        hours, mins, secs = m.groups()
        return int(hours) * 3600 + int(mins) * 60 + float(secs)
    return 45.0


def fetch_pexels_videos(query: str, work_dir: Path, max_clips: int = 6) -> list:
    """Download relevant HD/4K nature stock clips from Pexels."""
    headers = {"Authorization": PEXELS_API_KEY}
    url = f"https://api.pexels.com/videos/search?query={query}&per_page=15&size=medium"
    clips = []
    try:
        r = requests.get(url, headers=headers, timeout=30)
        videos = r.json().get("videos", [])
        for v in videos:
            if len(clips) >= max_clips:
                break
            for f in v.get("video_files", []):
                # Prefer HD/UHD vertical or horizontal that can be cropped
                if f.get("width", 0) >= 720:
                    vid_url = f["link"]
                    fname = work_dir / f"clip_{len(clips)}.mp4"
                    try:
                        r2 = requests.get(vid_url, timeout=60, stream=True)
                        with open(fname, "wb") as fp:
                            for chunk in r2.iter_content(chunk_size=1024 * 1024):
                                fp.write(chunk)
                        if fname.exists() and fname.stat().st_size > 50000:
                            clips.append(fname)
                        break
                    except Exception as ex:
                        print(f"Clip download failed: {ex}")
                        continue
    except Exception as e:
        print(f"Pexels fetch error: {e}")

    # Fallback to generic wildlife queries if none found
    if len(clips) < 2:
        print("Fallback search with 'wildlife nature 4k'...")
        try:
            r = requests.get("https://api.pexels.com/videos/search?query=wildlife+nature+animals&per_page=10", headers=headers, timeout=30)
            videos = r.json().get("videos", [])
            for v in videos:
                if len(clips) >= max_clips:
                    break
                for f in v.get("video_files", []):
                    if f.get("width", 0) >= 720:
                        vid_url = f["link"]
                        fname = work_dir / f"clip_fb_{len(clips)}.mp4"
                        r2 = requests.get(vid_url, timeout=60, stream=True)
                        with open(fname, "wb") as fp:
                            for chunk in r2.iter_content(chunk_size=1024 * 1024):
                                fp.write(chunk)
                        if fname.exists() and fname.stat().st_size > 50000:
                            clips.append(fname)
                        break
        except Exception:
            pass

    return clips


def download_bgm(work_dir: Path) -> Path:
    """Download ambient background music."""
    bgm_path = work_dir / "bgm.mp3"
    for url in BGM_URLS:
        try:
            r = requests.get(url, timeout=30)
            if r.status_code == 200 and len(r.content) > 10000:
                with open(bgm_path, "wb") as f:
                    f.write(r.content)
                return bgm_path
        except Exception:
            continue
    return bgm_path


def create_subtitle_overlays(lines_with_times: list, work_dir: Path) -> list:
    """Generate high-contrast yellow badge subtitles for 1080x1920 shorts."""
    font_path = "C:\\Windows\\Fonts\\arialbd.ttf"
    if not os.path.exists(font_path):
        font_path = "C:\\Windows\\Fonts\\segoeuib.ttf"

    overlay_items = []
    W, H = 1080, 1920

    for idx, (line, start_t, end_t) in enumerate(lines_with_times):
        words = line.upper().split()
        # 3-4 words per badge
        chunks = [" ".join(words[i:i+4]) for i in range(0, len(words), 4)]
        chunk_dur = (end_t - start_t) / max(len(chunks), 1)

        for ci, chunk in enumerate(chunks):
            t_start = start_t + ci * chunk_dur
            t_end = t_start + chunk_dur
            img_path = work_dir / f"sub_{idx}_{ci}.png"

            img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)

            font_size = 64
            try:
                font = ImageFont.truetype(font_path, font_size)
            except Exception:
                font = ImageFont.load_default()

            bbox = draw.textbbox((0, 0), chunk, font=font)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]

            pad_x, pad_y = 30, 16
            radius = 18
            rect_w = tw + pad_x * 2
            rect_h = th + pad_y * 2
            rx = (W - rect_w) // 2
            ry = H // 2 + 350  # Lower center of screen

            # Yellow pill background
            draw.rounded_rectangle([rx, ry, rx + rect_w, ry + rect_h], radius=radius, fill="#FFE000")
            # Black bold text
            draw.text((rx + pad_x, ry + pad_y), chunk, font=font, fill="#000000")

            img.save(str(img_path), "PNG")
            overlay_items.append((img_path, t_start, t_end))

    return overlay_items


def render_short_video(data: dict, output_video_path: Path) -> bool:
    """Render full YouTube Short video locally with FFmpeg."""
    work_dir = output_video_path.parent / f"temp_{output_video_path.stem}"
    work_dir.mkdir(exist_ok=True)

    topic_title = data["topic_title"]
    hook_sentence = data["hook_sentence"]
    script_lines = data["script_lines"]
    search_kw = data.get("search_keyword", "wildlife nature 4k")

    print(f"\n[RENDER] Starting video production for: '{topic_title}'")

    # 1. Voiceover
    print("-> Generating voiceover...")
    voice_path = work_dir / "voice.mp3"
    all_lines = [hook_sentence] + script_lines
    full_script = " ".join(all_lines)
    asyncio.run(generate_voiceover(full_script, voice_path))

    duration = get_audio_duration(voice_path)
    print(f"-> Voiceover generated. Duration: {duration:.2f} seconds")

    # 2. Download footage
    print(f"-> Fetching 4K clips from Pexels for '{search_kw}'...")
    clips = fetch_pexels_videos(search_kw, work_dir, max_clips=7)
    if not clips:
        print("ERROR: No clips could be downloaded.")
        return False
    print(f"-> Downloaded {len(clips)} clips")

    # 3. Download BGM
    print("-> Fetching background music...")
    bgm_path = download_bgm(work_dir)

    # 4. Trim and format clips to 1080x1920 (vertical 9:16)
    clip_dur = max(3.5, duration / len(clips))
    trimmed_clips = []
    for i, clip in enumerate(clips):
        trimmed = work_dir / f"trimmed_{i}.mp4"
        cmd = [
            FFMPEG, "-y", "-i", str(clip),
            "-t", str(clip_dur + 0.5),
            "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30",
            "-c:v", "libx264", "-crf", "23", "-preset", "veryfast",
            "-an", str(trimmed)
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if trimmed.exists() and trimmed.stat().st_size > 10000:
            trimmed_clips.append(trimmed)

    if not trimmed_clips:
        print("ERROR: Failed to process video clips.")
        return False

    # 5. Concat clips
    concat_list = work_dir / "concat_list.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        for tc in trimmed_clips:
            clean_p = str(tc).replace("\\", "/")
            f.write(f"file '{clean_p}'\n")

    raw_video = work_dir / "raw_video.mp4"
    cmd_concat = [
        FFMPEG, "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-t", str(duration + 0.5),
        "-c:v", "libx264", "-crf", "22", "-preset", "veryfast",
        "-an", str(raw_video)
    ]
    subprocess.run(cmd_concat, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 6. Generate Subtitles
    print("-> Generating subtitle badges...")
    approx_wpm = 135
    times = []
    t = 0.0
    for line in all_lines:
        words = len(line.split())
        dur = (words / approx_wpm) * 60.0
        times.append((line, t, t + dur))
        t += dur

    subtitles = create_subtitle_overlays(times, work_dir)

    # 7. Subtitle Overlay Filter
    subbed_video = work_dir / "subbed_video.mp4"
    if subtitles:
        filter_parts = []
        current = "[0:v]"
        for idx, (img_p, s_t, e_t) in enumerate(subtitles):
            next_lbl = f"[v{idx}]" if idx < len(subtitles) - 1 else "[vout]"
            filter_parts.append(
                f"{current}[{idx+1}:v]overlay=0:0:enable='between(t,{s_t:.2f},{e_t:.2f})'{next_lbl}"
            )
            current = next_lbl
        filter_complex = ";".join(filter_parts)

        inputs = ["-i", str(raw_video)]
        for img_p, _, _ in subtitles:
            inputs.extend(["-i", str(img_p)])

        cmd_sub = [
            FFMPEG, "-y",
            *inputs,
            "-filter_complex", filter_complex,
            "-map", "[vout]",
            "-t", str(duration),
            "-c:v", "libx264", "-crf", "22", "-preset", "veryfast",
            "-an", str(subbed_video)
        ]
        subprocess.run(cmd_sub, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        subbed_video = raw_video

    # 8. Audio Mixing (Voiceover + Ducked Looped BGM)
    mixed_audio = work_dir / "mixed_audio.mp3"
    if bgm_path.exists() and bgm_path.stat().st_size > 10000:
        # Loop BGM and duck volume by -18dB, overlay with voice
        filter_audio = (
            f"[1:a]aloop=loop=-1:size=2e+09,volume=0.13[bgm];"
            f"[0:a]volume=1.0[voice];"
            f"[voice][bgm]amix=inputs=2:duration=first:dropout_transition=2[aout]"
        )
        cmd_audio = [
            FFMPEG, "-y",
            "-i", str(voice_path),
            "-i", str(bgm_path),
            "-filter_complex", filter_audio,
            "-map", "[aout]",
            "-t", str(duration),
            str(mixed_audio)
        ]
        subprocess.run(cmd_audio, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        mixed_audio = voice_path

    # 9. Final Mux (Subbed Video + Mixed Audio)
    print("-> Merging video and audio to final 1080x1920 MP4...")
    cmd_final = [
        FFMPEG, "-y",
        "-i", str(subbed_video if subbed_video.exists() else raw_video),
        "-i", str(mixed_audio if mixed_audio.exists() else voice_path),
        "-c:v", "libx264", "-crf", "20", "-preset", "medium",
        "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart",
        "-shortest",
        str(output_video_path)
    ]
    subprocess.run(cmd_final, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if output_video_path.exists() and output_video_path.stat().st_size > 100000:
        sz_mb = output_video_path.stat().st_size / (1024 * 1024)
        print(f"[SUCCESS] Video rendered: {output_video_path.name} ({sz_mb:.2f} MB)")
        return True
    else:
        print(f"[ERROR] Failed to produce final video at {output_video_path}")
        return False


def upload_and_schedule_to_youtube(video_path: Path, metadata: dict, publish_utc_iso: str) -> dict:
    """Upload video to YouTube and schedule publication."""
    creds = Credentials.from_authorized_user_file(str(TOKEN_PATH))
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
    youtube = build("youtube", "v3", credentials=creds)

    body = {
        "snippet": {
            "title": metadata["youtube_title"][:100],
            "description": metadata["youtube_description"],
            "tags": metadata.get("youtube_tags", []),
            "categoryId": "15"  # Pets & Animals
        },
        "status": {
            "privacyStatus": "private",
            "publishAt": publish_utc_iso,
            "selfDeclaredMadeForKids": False
        }
    }

    media = MediaFileUpload(str(video_path), chunksize=-1, resumable=True, mimetype="video/mp4")
    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    print(f"Uploading '{metadata['youtube_title']}' with scheduled publishAt={publish_utc_iso}...")
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            pct = int(status.progress() * 100)
            print(f"Upload progress: {pct}%")

    video_id = response.get("id")
    url = f"https://youtube.com/shorts/{video_id}"
    print(f"[YOUTUBE_UPLOAD_SUCCESS] Video ID: {video_id} | URL: {url} | Scheduled: {publish_utc_iso}")
    return {"video_id": video_id, "url": url, "publish_at": publish_utc_iso}
