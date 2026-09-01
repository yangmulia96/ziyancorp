import asyncio
import os
import sys
import requests
from edge_tts import Communicate
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips

sys.stdout.reconfigure(encoding='utf-8')

async def generate_voiceover(text, output_mp3):
    communicate = Communicate(text, "id-ID-ArdiNeural")
    await communicate.save(output_mp3)

def create_short(niche_title, scenes_data, output_mp4):
    print(f"🎬 Creating Short for Niche: {niche_title}...")
    clips = []
    temp_files = []

    for idx, scene in enumerate(scenes_data):
        img_path = f"temp_scene_{idx}.jpg"
        audio_path = f"temp_audio_{idx}.mp3"
        temp_files.extend([img_path, audio_path])

        # 1. Download image from Pollinations AI or generate synthetic 9:16 background
        prompt_encoded = requests.utils.quote(scene['image_prompt'])
        img_url = f"https://pollinations.ai/p/{prompt_encoded}?width=1080&height=1920&seed={idx+42}&model=flux"
        print(f"  🖼️ Downloading Scene {idx+1} Image...")
        try:
            r = requests.get(img_url, timeout=10)
            if r.status_code == 200 and len(r.content) > 5000:
                with open(img_path, 'wb') as f:
                    f.write(r.content)
            else:
                raise ValueError("Downloaded content invalid")
        except Exception as e:
            print(f"  ⚠️ Image download fallback: generating synthetic 9:16 canvas ({e})")
            from PIL import Image, ImageDraw, ImageFont
            canvas = Image.new('RGB', (1080, 1920), color=(15, 23, 42))
            draw = ImageDraw.Draw(canvas)
            draw.rectangle([60, 60, 1020, 1860], outline=(56, 189, 248), width=8)
            canvas.save(img_path)

        # 2. Generate Voiceover via Edge-TTS
        print(f"  🗣️ Generating Voiceover: '{scene['text'][:30]}...'")
        asyncio.run(generate_voiceover(scene['text'], audio_path))

        # 3. Build MoviePy Clip
        from PIL import Image
        import numpy as np
        pil_img = Image.open(img_path)
        img_np = np.array(pil_img)

        audio_clip = AudioFileClip(audio_path)
        img_clip = ImageClip(img_np).with_duration(audio_clip.duration).with_audio(audio_clip)
        clips.append(img_clip)

    # Concatenate all scenes into 9:16 Short
    final_video = concatenate_videoclips(clips, method="compose")
    final_video.write_videofile(output_mp4, fps=24, codec="libx264", audio_codec="aac")

    # Cleanup temp files
    for tf in temp_files:
        if os.path.exists(tf):
            os.remove(tf)
            
    print(f"✅ SHORT CREATED SUCCESSFULLY: {output_mp4}")

if __name__ == "__main__":
    sample_scenes = [
        {
            "text": "Tahukah kamu? Rahasia terbesar para pembuat konten sukses bukan pada kameranya!",
            "image_prompt": "Cinematic vertical 9:16 shot of a mysterious glowing neon AI content creator studio, high detail 8k"
        },
        {
            "text": "Tetapi pada otomatisasi sistem yang bekerja saat mereka tertidur lelap.",
            "image_prompt": "Futuristic cyberpunk robot working on multiple holographic screens at night, vertical 9:16"
        },
        {
            "text": "Dengan n8n dan AI Studio, kamu bisa menghasilkan ratusan klip viral otomatis setiap hari!",
            "image_prompt": "Golden YouTube play button floating in a digital matrix network, vertical 9:16, unreal engine 5 render"
        }
    ]
    
    out_dir = r"C:\Users\arija\ziyancorp\arsip_celine_aurel\tmp_assets"
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "autotube_demo_short.mp4")
    create_short("Tech & AI Automation", sample_scenes, out_file)
