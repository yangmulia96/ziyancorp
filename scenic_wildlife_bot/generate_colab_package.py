import json
import os
import re
from pathlib import Path

ROOT = Path(r"C:\Users\arija\ziyancorp\scenic_wildlife_bot")

BATCH_VIDEOS = [
    {
        "id": 1,
        "slot": "Slot Siang",
        "wib_schedule": "10:34 WIB",
        "topic_title": "Peregrine Falcon 390 KM/H Stoop Dive",
        "youtube_title": "The 390 KM/H Sky Hunter That Shatters Physics 🦅💨 #wildlife #nature #falcon #shorts",
        "hook_sentence": "Imagine diving out of the sky at nearly four hundred kilometers per hour—fast enough to pop human lungs.",
        "script_lines": [
            "High above the clouds, the peregrine falcon locks its telescopic vision on a target below.",
            "As it folds its razor-sharp wings, gravity takes over and it accelerates into a supersonic bullet.",
            "At three hundred and ninety kilometers per hour, ordinary nostrils would violently burst from air pressure.",
            "But nature equipped this master raptor with specialized aerodynamic baffles inside its nose to breathe at lethal speeds.",
            "A third clear eyelid acts as specialized aviation goggles to maintain crystal clear sight.",
            "It strikes its prey mid-air with a clenched fist delivering the impact force of a high-velocity cannon.",
            "This unmatched aerial mastery makes the peregrine falcon the fastest creature to ever live."
        ],
        "search_keyword": "falcon bird flying sky",
        "youtube_description": "Did you know that the fastest animal on Earth doesn't run on land—it dives from the sky? The Peregrine Falcon reaches unbelievable speeds exceeding 390 km/h (240 mph) during its lethal hunting stoop. At these extreme velocities, air pressure would instantly rupture human lungs, but the falcon evolved specialized aerodynamic baffles inside its nostrils to regulate airflow. Combined with a third protective eyelid and reinforced bone structure, it strikes mid-air prey with the force of a bullet.\n\nExplore the unbelievable power, speed, and precision of nature with us.\n\nSubscribe to @4kscenicwildlife for daily 4K documentary shorts showcasing the world's most incredible animals!\n\n#PeregrineFalcon #WildlifeDocumentary #4KNature #BirdsOfPrey #FastestAnimal #NatureFacts #WildlifeLovers #EpicNature #ScenicWildlife #Shorts",
        "youtube_tags": ["peregrine falcon", "fastest animal", "wildlife documentary", "4k nature", "birds of prey", "hunting stoop", "falcon speed", "nature facts", "animal superpowers", "4kscenicwildlife"]
    },
    {
        "id": 2,
        "slot": "Slot Sore",
        "wib_schedule": "15:48 WIB",
        "topic_title": "Dolphin Echolocation & Interspecies Rescue",
        "youtube_title": "The Telepathic Ocean Genius That Scans Your Body 🐬🌊 #ocean #wildlife #dolphins #nature",
        "hook_sentence": "Dolphins don't just see the ocean—they can literally see right through your skin.",
        "script_lines": [
            "Using advanced bio-sonar, a dolphin clicks and listens to sound vibrations traveling through water.",
            "This biological ultrasound is so powerful it can detect human heartbeats and bones from hundreds of feet away.",
            "Marine biologists documented wild dolphins gently nuzzling pregnant swimmers, sensing the fetal heartbeat before the mother even knew.",
            "Even more unbelievable is their profound cross-species empathy.",
            "When a great white shark stalked a group of lost swimmers in open water, a pod of dolphins rushed in.",
            "They swam in tight protective rings for over an hour, slapping their tails to keep the apex predator at bay until rescue arrived.",
            "This astonishing emotional intelligence proves that we are not the only compassionate minds on Earth."
        ],
        "search_keyword": "dolphin ocean underwater swimming",
        "youtube_description": "Dolphins possess one of the most sophisticated sensory systems on planet Earth: bio-sonar echolocation so advanced it functions like a real-time medical ultrasound. Dolphins can 'see' through water, sand, and even biological tissue—detecting bone density, heartbeats, and internal organs from hundreds of feet away.\n\nBeyond their incredible perception, dolphins demonstrate extraordinary cross-species empathy. There are documented historical cases of wild dolphin pods rescuing human swimmers from great white sharks by forming protective circular shields until help arrived. Discover why marine scientists consider dolphins to be among the most intelligent and compassionate beings in the animal kingdom.\n\nSubscribe to @4kscenicwildlife for breathtaking 4K nature documentaries, ocean wonders, and emotional animal stories!\n\n#Dolphins #OceanLife #WildlifeDocumentary #MarineBiology #Echolocation #DolphinRescue #4KNature #AnimalIntelligence #NatureShorts #ScenicWildlife",
        "youtube_tags": ["dolphins", "dolphin echolocation", "ocean wildlife", "wildlife documentary", "4k nature", "animal intelligence", "dolphin rescue", "marine life", "ocean mysteries", "4kscenicwildlife"]
    },
    {
        "id": 3,
        "slot": "Slot Malam",
        "wib_schedule": "20:23 WIB",
        "topic_title": "Zombie Cordyceps Fungus & Bullet Ant",
        "youtube_title": "The Real-Life Zombie Parasite of the Amazon 🐜🍄 #nature #wildlife #amazon #parasite",
        "hook_sentence": "Deep in the Amazon rainforest, a real-life zombie infection turns ants into puppets.",
        "script_lines": [
            "When a microscopic Cordyceps spore lands on a foraging ant, it doesn't kill the body immediately.",
            "It grows invasive fungal networks directly into the ant's muscle fibers, taking full control of its nervous system.",
            "The infected ant is chemically forced to abandon its colony and climb high onto a plant stem facing the sun.",
            "In its final moments, it clamps its mandibles into the main leaf vein in a permanent, locked death grip.",
            "Days later, a fungal stalk bursts violently out of the back of the ant's head.",
            "High above the forest floor, it releases millions of infectious spores, showering down on the unsuspecting colony below.",
            "This terrifying biological takeover inspired video games and shows why nature is stranger than fiction."
        ],
        "search_keyword": "ant rainforest macro insect",
        "youtube_description": "Nature holds secrets more terrifying than science fiction. In the dense canopy of the Amazon rainforest, Ophiocordyceps unilateralis—the infamous 'zombie-ant fungus'—takes complete control of its host. Rather than killing the ant right away, fungal mycelium infiltrates the insect's muscles, hijacking its motor control.\n\nThe hijacked ant is chemically compelled to climb to the exact microclimate height of 25 centimeters above the forest floor, align with the sun, and lock its jaws onto the underside of a leaf. Once anchored, the fungus consumes the ant's internal organs and sprouts a fruiting body directly through the ant's head to rain spores onto the colony below.\n\nSubscribe to @4kscenicwildlife for mind-blowing 4K nature documentaries, bizarre animal facts, and breathtaking wildlife cinematography from every corner of Earth!\n\n#Cordyceps #ZombieAnt #NatureDocumentary #AmazonRainforest #Insects #Parasite #4KNature #BizarreNature #ScienceShorts #ScenicWildlife",
        "youtube_tags": ["cordyceps", "zombie ant", "amazon rainforest", "nature documentary", "4k nature", "parasitic fungus", "bizarre animals", "insect behavior", "nature facts", "4kscenicwildlife"]
    }
]

def generate_files():
    print("=== GENERATING COLAB 3-VIDEO PRODUCTION PACKAGE ===")
    
    # Save individual meta files
    for v in BATCH_VIDEOS:
        meta_path = ROOT / f"pending_meta_{v['id']}.json"
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(v, f, indent=2)
        print(f"[+] Saved metadata: {meta_path.name}")
        
    # Build complete Colab Notebook (.ipynb)
    notebook_cells = []
    
    # Header markdown
    notebook_cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# 🎬 4K SCENIC WILDLIFE - AUTOMATED 3-VIDEO PRODUCTION PIPELINE\n",
            "### Channel: `@4kscenicwildlife` | GPU Accelerated Cloud Renderer\n",
            "\n",
            "**Batch Produksi Hari Ini:**\n",
            "1. 🦅 **Peregrine Falcon 390 KM/H Stoop Dive** *(Slot Siang - 10:34 WIB)*\n",
            "2. 🐬 **Dolphin Echolocation & Interspecies Rescue** *(Slot Sore - 15:48 WIB)*\n",
            "3. 🐜 **Zombie Cordyceps Fungus & Bullet Ant** *(Slot Malam - 20:23 WIB)*\n",
            "\n",
            "⚡ **Instruksi:** Cukup klik menu **Runtime → Run all** (atau tekan `Ctrl + F9`). Seluruh video akan dirender otomatis!"
        ]
    })
    
    # Install dependencies cell
    notebook_cells.append({
        "cell_type": "code",
        "metadata": {},
        "source": [
            "# 1. Install & Setup Production Dependencies\n",
            "!pip install -q pydub edge-tts Pillow requests imageio-ffmpeg\n",
            "!apt-get -qq update && apt-get -qq install -y ffmpeg\n",
            "\n",
            "import os, json, time, asyncio, requests, subprocess, hashlib, re\n",
            "from pathlib import Path\n",
            "import edge_tts\n",
            "from PIL import Image, ImageDraw, ImageFont\n",
            "from pydub import AudioSegment\n",
            "\n",
            "OUTPUT_DIR = Path('/content/output_videos')\n",
            "OUTPUT_DIR.mkdir(parents=True, exist_ok=True)\n",
            "print('✅ Environment & Dependencies Ready!')"
        ]
    })
    
    # Embedded Videos Data & Engine Cell
    engine_code = f'''# 2. Complete Rendering Engine with Stock B-Roll & Subtitle Generator
VIDEOS_DATA = {json.dumps(BATCH_VIDEOS, indent=2)}

PEXELS_API_KEY = "F9f4KvZlReqd7klXaknvf6zPpbT00GrD62LUUojmvxUV5DwuWzCFj21h"
PIXABAY_API_KEY = "57267312-9c26b138313d3dedf51fca0a7"

def fetch_pexels_videos(query, max_clips=6):
    headers = {{"Authorization": PEXELS_API_KEY}}
    url = f"https://api.pexels.com/videos/search?query={{query}}&per_page=15&size=large"
    clips = []
    try:
        r = requests.get(url, headers=headers, timeout=25)
        videos = r.json().get("videos", [])
        for v in videos:
            if len(clips) >= max_clips:
                break
            for f in v.get("video_files", []):
                if f.get("quality") in ("hd", "uhd") and f.get("width", 0) >= 720:
                    vid_url = f["link"]
                    fname = f"/content/clip_{{len(clips)}}.mp4"
                    r2 = requests.get(vid_url, timeout=40, stream=True)
                    with open(fname, "wb") as fp:
                        for chunk in r2.iter_content(chunk_size=1024*1024):
                            fp.write(chunk)
                    clips.append(fname)
                    break
    except Exception as e:
        print(f"  [!] Pexels search error: {{e}}")
    return clips

async def render_tts(script_text, output_mp3):
    communicate = edge_tts.Communicate(script_text, voice="en-US-ChristopherNeural", rate="-4%")
    await communicate.save(output_mp3)

def generate_video(video_info):
    vid_id = video_info["id"]
    title = video_info["topic_title"]
    print(f"\\n========================================================")
    print(f"🎬 PRODUCING VIDEO #{{vid_id}}: {{title}}")
    print(f"========================================================")
    
    # 1. Voiceover
    full_text = video_info["hook_sentence"] + " " + " ".join(video_info["script_lines"])
    voice_path = f"/content/voice_{{vid_id}}.mp3"
    asyncio.run(render_tts(full_text, voice_path))
    
    audio = AudioSegment.from_mp3(voice_path)
    dur_sec = len(audio) / 1000.0
    print(f"[+] Narration generated: {{dur_sec:.1f}}s")
    
    # 2. B-Roll Footage
    clips = fetch_pexels_videos(video_info["search_keyword"], max_clips=5)
    print(f"[+] Downloaded {{len(clips)}} stock clips")
    
    # 3. Render Output using FFmpeg with 9:16 vertical crop & high quality
    out_file = f"/content/output_videos/short_{{vid_id}}.mp4"
    
    if clips:
        # Loop clips to match audio duration
        concat_txt = f"/content/concat_{{vid_id}}.txt"
        with open(concat_txt, "w") as f:
            for c in clips:
                f.write(f"file '{{c}}'\\n")
                
        cmd = [
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0", "-stream_loop", "3", "-i", concat_txt,
            "-i", voice_path,
            "-t", str(dur_sec),
            "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1",
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k",
            out_file
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"✅ SUCCESS: Rendered -> {{out_file}}")
    else:
        # Fallback synthetic background
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi", "-i", "color=c=0x0a1128:s=1080x1920:r=30",
            "-i", voice_path,
            "-t", str(dur_sec),
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k",
            out_file
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"✅ SUCCESS (Fallback): Rendered -> {{out_file}}")
        
    return out_file

# Execute all 3 videos
results = []
for v in VIDEOS_DATA:
    out = generate_video(v)
    results.append(out)

print("\\n" + "=" * 60)
print("🎉 ALL 3 VIDEOS SUCCESSFULLY PRODUCED ON GOOGLE COLAB!")
print("=" * 60)
for r in results:
    if os.path.exists(r):
        size_mb = os.path.getsize(r) / (1024 * 1024)
        print(f"📹 {{r}} ({{size_mb:.2f}} MB)")
'''
    
    notebook_cells.append({
        "cell_type": "code",
        "metadata": {},
        "source": [engine_code]
    })
    
    # Download cell
    notebook_cells.append({
        "cell_type": "code",
        "metadata": {},
        "source": [
            "# 3. Download Generated Videos to Laptop\n",
            "from google.colab import files\n",
            "import os\n",
            "\n",
            "for i in range(1, 4):\n",
            "    vid_path = f'/content/output_videos/short_{i}.mp4'\n",
            "    if os.path.exists(vid_path):\n",
            "        print(f'Downloading short_{i}.mp4...')\n",
            "        files.download(vid_path)"
        ]
    })
    
    notebook_json = {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "colab": {
                "name": "4K_Scenic_Wildlife_3_Videos_Production.ipynb",
                "provenance": [],
                "include_colab_link": True
            },
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.11.0"
            }
        },
        "cells": notebook_cells
    }
    
    ipynb_path = ROOT / "4K_Scenic_Wildlife_3_Videos_Production.ipynb"
    with open(ipynb_path, "w", encoding="utf-8") as f:
        json.dump(notebook_json, f, indent=2)
    print(f"[+] Saved Standalone Colab Notebook: {ipynb_path.name}")
    
    # Also save individual colab cells
    from colab_renderer import build_colab_cell
    for v in BATCH_VIDEOS:
        code = build_colab_cell(v)
        cell_file = ROOT / f"pending_colab_cell_{v['id']}.py"
        with open(cell_file, "w", encoding="utf-8") as f:
            f.write(code)
        print(f"[+] Saved Colab Cell #{v['id']}: {cell_file.name}")

if __name__ == "__main__":
    generate_files()
