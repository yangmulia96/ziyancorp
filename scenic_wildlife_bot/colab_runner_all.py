
# Google Colab Production Runner - 3 Video Shorts
# Upload files: pending_colab_cell_1/2/3.py + pending_meta_1/2/3.json

import os
import json
import subprocess

print('='*60)
print('PRODUCTION RUNNER - 3 VIDEO SHORTS')
print('='*60)

# Configuration
DRIVE_OUTPUT = '/content/drive/MyDrive/ZIYANCORP_AI_FACTORY'
os.makedirs(DRIVE_OUTPUT, exist_ok=True)

# Pip install deps
print('Installing dependencies...')
subprocess.run(['pip', 'install', '-q', 'pydub', 'edge-tts', 'Pillow', 'requests', 'google-generativeai'], check=True)

import requests
from PIL import Image, ImageDraw, ImageFont
import asyncio, edge_tts
from pydub import AudioSegment

# Function to produce one video
def produce_video(video_id, cell_code, meta):
    print(f'
{"="*60}')
    print(f'RENDERING VIDEO #{video_id}')
    print(f'Topic: {meta["topic_title"]}')
    print(f'YT Title: {meta["youtube_title"]}')
    print(f'{"="*60}')
    
    # Write cell to temp file and execute
    cell_path = f'/content/pending_colab_cell_{video_id}.py'
    meta_path = f'/content/pending_meta_{video_id}.json'
    
    with open(cell_path, 'w', encoding='utf-8') as f:
        f.write(cell_code)
    with open(meta_path, 'w', encoding='utf-8') as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    
    # Execute cell
    exec(compile(cell_code, cell_path, 'exec'))
    
    print(f'
✅ VIDEO #{video_id} PRODUCTION COMPLETE')

# Run all 3 videos
for cell in cells:
    produce_video(cell['id'], cell['cell'], cell['meta'])
    print(f'
--- Video {cell["id"]} complete, waiting 30s before next ---')
    time.sleep(30)

print('
' + '='*60)
print('ALL 3 VIDEOS PRODUCTION COMPLETE!')
print('='*60)
print('Files saved to: /content/drive/MyDrive/ZIYANCORP_AI_FACTORY/')
for cell in cells:
    print(f'  Video #{cell["id"]}: {cell["topic"]}')
