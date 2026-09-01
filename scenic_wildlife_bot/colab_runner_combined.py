"""
Google Colab Production Runner - 3 Video Shorts
Upload ke Colab: colab_runner_combined.py + 6 file pendukung
Run di notebook: !python colab_runner_combined.py

Target:
- Video #1: slot 15:48 WIB
- Video #2: slot 20:23 WIB  
- Video #3: besok 10:34 WIB
"""
import os
import json
import subprocess
import time

print('='*70)
print('GOOGLE COLAB PRODUCTION RUNNER - 3 VIDEO SHORTS')
print('='*70)

# Install dependencies
print('Installing dependencies...')
subprocess.run(['pip', 'install', '-q', 'pydub', 'edge-tts', 'Pillow', 'requests', 'google-generativeai'], check=True)
import requests
from PIL import Image, ImageDraw, ImageFont
import asyncio, edge_tts
from pydub import AudioSegment

DRIVE_OUTPUT = '/content/drive/MyDrive/ZIYANCORP_AI_FACTORY'
os.makedirs(DRIVE_OUTPUT, exist_ok=True)

# Load all 3 videos
videos = []
for i in range(1, 4):
    with open(f'/content/pending_meta_{i}.json', 'r', encoding='utf-8') as f:
        meta = json.load(f)
    with open(f'/content/pending_colab_cell_{i}.py', 'r', encoding='utf-8') as f:
        cell_code = f.read()
    videos.append({'id': i, 'meta': meta, 'cell_code': cell_code})

for vid in videos:
    print(f'\n{"#"*70}')
    print(f'RENDERING VIDEO #{vid["id"]}')
    print(f'Topic: {vid["meta"]["topic_title"]}')
    print(f'YT Title: {vid["meta"]["youtube_title"]}')
    print(f'{"#"*70}')
    
    data = vid['meta']
    cell_code = vid['cell_code']
    
    exec(compile(cell_code, f'video_{vid["id"]}', 'exec'))
    
    print(f'\n✅ VIDEO #{vid["id"]} COMPLETE')
    print(f'File: {DRIVE_OUTPUT}/{vid["meta"]["topic_title"][:20].replace(" ", "_")}.mp4')
    time.sleep(30)

print('\n' + '='*70)
print('ALL 3 VIDEOS PRODUCTION COMPLETE!')
print('='*70)
print('Files saved to: /content/drive/MyDrive/ZIYANCORP_AI_FACTORY/')
for vid in videos:
    print(f'  Video #{vid["id"]}: {vid["meta"]["topic_title"]}')
