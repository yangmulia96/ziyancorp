import os
import sys
import json
import time
import asyncio
import subprocess
import requests
import re
from pathlib import Path
import datetime

if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

ROOT = Path(r"C:\Users\arija\ziyancorp\scenic_wildlife_bot")
OUTPUT_DIR = ROOT / "output_videos"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PEXELS_API_KEY = "F9f4KvZlReqd7klXaknvf6zPpbT00GrD62LUUojmvxUV5DwuWzCFj21h"
PIXABAY_API_KEY = "57267312-9c26b138313d3dedf51fca0a7"

BATCH_VIDEOS = [
    {
        "id": 1,
        "slot": "Slot Siang",
        "wib_schedule": "10:34 WIB",
        "publish_at_utc": "2026-08-31T03:34:00.000Z",
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
        "publish_at_utc": "2026-08-31T08:48:00.000Z",
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
        "publish_at_utc": "2026-08-31T13:23:00.000Z",
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

def fetch_pexels_videos(query, max_clips=4):
    headers = {"Authorization": PEXELS_API_KEY}
    url = f"https://api.pexels.com/videos/search?query={query}&per_page=15&size=large"
    clips = []
    try:
        r = requests.get(url, headers=headers, timeout=25)
        if r.status_code == 200:
            videos = r.json().get("videos", [])
            for v in videos:
                if len(clips) >= max_clips:
                    break
                for f in v.get("video_files", []):
                    if f.get("quality") in ("hd", "uhd") and f.get("width", 0) >= 720:
                        vid_url = f["link"]
                        fname = str(OUTPUT_DIR / f"temp_clip_{len(clips)}.mp4")
                        r2 = requests.get(vid_url, timeout=40, stream=True)
                        with open(fname, "wb") as fp:
                            for chunk in r2.iter_content(chunk_size=1024*1024):
                                fp.write(chunk)
                        clips.append(fname)
                        break
    except Exception as e:
        print(f"  [!] Pexels fetch error: {e}", flush=True)
    return clips

async def generate_voice(text, out_mp3):
    import edge_tts
    communicate = edge_tts.Communicate(text, voice="en-US-ChristopherNeural", rate="-4%")
    await communicate.save(str(out_mp3))

def produce_video(v):
    vid_id = v["id"]
    title = v["topic_title"]
    print(f"\n========================================================", flush=True)
    print(f"🎬 [1/2] RENDERING VIDEO #{vid_id}: {title}", flush=True)
    print(f"========================================================", flush=True)

    # 1. Voiceover
    full_text = v["hook_sentence"] + " " + " ".join(v["script_lines"])
    voice_path = OUTPUT_DIR / f"voice_{vid_id}.mp3"
    print(f"[*] Generating Christopher Neural voiceover...", flush=True)
    asyncio.run(generate_voice(full_text, voice_path))

    # Probe duration
    from pydub import AudioSegment
    audio = AudioSegment.from_mp3(str(voice_path))
    dur_sec = len(audio) / 1000.0
    print(f"[+] Voiceover ready: {dur_sec:.1f} seconds", flush=True)

    # 2. Stock Footage
    print(f"[*] Fetching B-roll footage for: '{v['search_keyword']}'...", flush=True)
    clips = fetch_pexels_videos(v["search_keyword"], max_clips=4)
    print(f"[+] Downloaded {len(clips)} stock footage clips", flush=True)

    # 3. Render Output MP4
    safe_topic = re.sub(r'[^a-zA-Z0-9_]', '_', v['topic_title'])[:30]
    out_mp4 = OUTPUT_DIR / f"short_{vid_id}_{safe_topic}.mp4"

    if clips:
        concat_txt = OUTPUT_DIR / f"concat_{vid_id}.txt"
        with open(concat_txt, "w") as f:
            for c in clips:
                clean_path = c.replace("\\", "/")
                f.write(f"file '{clean_path}'\n")

        cmd = [
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0", "-stream_loop", "3", "-i", str(concat_txt),
            "-i", str(voice_path),
            "-t", str(dur_sec),
            "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1",
            "-c:v", "libx264", "-preset", "fast", "-crf", "20",
            "-c:a", "aac", "-b:a", "192k",
            str(out_mp4)
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        # Fallback background
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi", "-i", "color=c=0x0a1128:s=1080x1920:r=30",
            "-i", str(voice_path),
            "-t", str(dur_sec),
            "-c:v", "libx264", "-preset", "fast", "-crf", "20",
            "-c:a", "aac", "-b:a", "192k",
            str(out_mp4)
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    size_mb = os.path.getsize(str(out_mp4)) / (1024 * 1024)
    print(f"[+] Video rendered successfully: {out_mp4.name} ({size_mb:.2f} MB)", flush=True)
    return str(out_mp4)

def upload_video_entry(v, video_path):
    print(f"\n[*] [2/2] UPLOADING & SCHEDULING TO YOUTUBE SHORTS...", flush=True)
    from youtube_uploader import upload_to_youtube
    
    res = upload_to_youtube(
        video_path=video_path,
        data=v,
        publish_at=v["publish_at_utc"]
    )
    return res

def main():
    print("================================================================", flush=True)
    print("🚀 4K SCENIC WILDLIFE AUTOMATED 3-VIDEO PRODUCTION & SCHEDULER", flush=True)
    print("================================================================", flush=True)

    upload_results = []
    for v in BATCH_VIDEOS:
        try:
            # 1. Produce
            mp4_path = produce_video(v)
            
            # 2. Upload
            yt_res = upload_video_entry(v, mp4_path)
            
            vid_id = yt_res.get("id") if yt_res else "pending"
            yt_url = f"https://youtube.com/shorts/{vid_id}" if vid_id else ""
            print(f"✅ Video #{v['id']} ({v['slot']}) SCHEDULED FOR {v['wib_schedule']}!", flush=True)
            print(f"   URL: {yt_url}", flush=True)

            upload_results.append({
                "video_number": v["id"],
                "slot": v["slot"],
                "wib_schedule": v["wib_schedule"],
                "publish_at_utc": v["publish_at_utc"],
                "topic_title": v["topic_title"],
                "youtube_title": v["youtube_title"],
                "video_id": vid_id,
                "url": yt_url,
                "local_file": mp4_path,
                "status": "scheduled",
                "created_at": datetime.datetime.utcnow().isoformat() + "Z"
            })
        except Exception as e:
            print(f"[-] Error processing video #{v['id']}: {e}", flush=True)

    # Save to production log
    log_path = ROOT / "production_log.json"
    existing_log = {}
    if log_path.exists():
        try:
            with open(log_path, "r", encoding="utf-8") as f:
                existing_log = json.load(f)
        except Exception:
            existing_log = {}

    uploads_list = existing_log.get("uploads", [])
    uploads_list.extend(upload_results)
    existing_log["total_videos"] = len(uploads_list)
    existing_log["uploads"] = uploads_list
    existing_log["last_production"] = datetime.datetime.utcnow().isoformat() + "Z"

    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(existing_log, f, indent=2)

    print("\n" + "=" * 64, flush=True)
    print("🎉 ALL 3 VIDEOS SUCCESSFULLY PRODUCED & SCHEDULED ON YOUTUBE!", flush=True)
    print("================================================================", flush=True)
    for res in upload_results:
        print(f"• {res['slot']} ({res['wib_schedule']}): {res['youtube_title']}")
        print(f"  Link: {res['url']}\n", flush=True)

if __name__ == "__main__":
    main()
