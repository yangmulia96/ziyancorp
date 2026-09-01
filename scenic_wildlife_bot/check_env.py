import sys, os, shutil
print("Python:", sys.version)
print("FFmpeg on PATH:", shutil.which("ffmpeg"))

for pkg in ["edge_tts", "pydub", "PIL", "requests", "google.genai", "googleapiclient"]:
    try:
        __import__(pkg)
        print(f"Package {pkg}: OK")
    except ImportError as e:
        print(f"Package {pkg}: MISSING ({e})")
