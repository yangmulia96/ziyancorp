import subprocess, os, json

VENV = r"C:\Users\arija\clip_test\.venv\Scripts\python.exe"
VIDEO = r"C:\Users\arija\clip_test\test.mp4"
TXT = r"C:\Users\arija\clip_test\transcript.txt"
PLAN = r"C:\Users\arija\clip_test\clip_plan.txt"
OUT = r"C:\Users\arija\clip_test\clip_output.mp4"

# 1. Transcribe (skip if exists)
if not os.path.exists(TXT) or os.path.getsize(TXT) == 0:
    code = ("import faster_whisper\n"
            "m = faster_whisper.WhisperModel('base', device='cpu', compute_type='int8')\n"
            "segs, _ = m.transcribe(r'" + VIDEO + "', beam_size=5)\n"
            "open(r'" + TXT + "', 'w', encoding='utf-8').write(' '.join(s.text for s in segs))\n")
    subprocess.run([VENV, "-c", code], capture_output=True, text=True)

transcript = open(TXT, encoding="utf-8").read()

# 2. Sonnet via curl SSE
KEY = os.environ.get("HERMES_CUSTOM_9ROUTER_API_KEY", "")
prompt = f"Dari transcript ini, pilih 1 momen paling viral (max 30 detik). Buat caption TikTok/Reels (hook + 5 hashtag).\nTranscript: {transcript[:1500]}"
raw = subprocess.run(["curl", "-s", "-m", "40", "http://localhost:20128/v1/chat/completions",
    "-H", "Content-Type: application/json", "-H", f"Authorization: Bearer {KEY}",
    "-d", json.dumps({"model": "kr/claude-sonnet-4.5", "messages": [{"role": "user", "content": prompt}], "temperature": 0.7, "stream": True})],
    capture_output=True, text=True).stdout

out = ""
for line in raw.split("\n"):
    line = line.strip()
    if line.startswith("data: ") and "[DONE]" not in line:
        try:
            j = json.loads(line[6:])
            out += j["choices"][0]["delta"].get("content", "")
        except: pass
open(PLAN, encoding="utf-8", mode="w").write(out)
print("CAPTION:", out[:300])

# 3. FFmpeg potong 9:16
r2 = subprocess.run(f'ffmpeg -y -i "{VIDEO}" -t 15 -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1" -c:v libx264 -preset ultrafast "{OUT}"', shell=True, capture_output=True, text=True)
print("FFmpeg exit:", r2.returncode, "| Output exists:", os.path.exists(OUT))
