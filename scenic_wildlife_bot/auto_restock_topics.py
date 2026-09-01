#!/usr/bin/env python3
"""
Scenic Wildlife — Auto-Restock Watchdog Engine
Monitors content_queue.json. If remaining READY topics < 5,
automatically generates 15 new unique viral 4K wildlife documentary topics
using Gemini API, verifying against used_topics.json to guarantee 0 duplicates.
"""
import os
import sys
import json
import re
from pathlib import Path
from google import genai
from google.genai import types

ROOT = Path(__file__).parent
QUEUE_FILE = ROOT / "content_queue.json"
USED_TOPICS_FILE = ROOT / "used_topics.json"

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AQ.Ab8RN6Jh-jeCGKc3YTcSuVsaHUrVonnc4mUeJGqvAtbmGSd9mQ")

def load_queue():
    if QUEUE_FILE.exists():
        try:
            with open(QUEUE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_queue(queue):
    with open(QUEUE_FILE, "w", encoding="utf-8") as f:
        json.dump(queue, f, indent=2, ensure_ascii=False)

def load_used_topics():
    if USED_TOPICS_FILE.exists():
        try:
            with open(USED_TOPICS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def check_and_restock(min_threshold=5, batch_size=15):
    queue = load_queue()
    ready_items = [q for q in queue if q.get("status") == "READY"]
    used_topics = load_used_topics()
    
    print(f"[+] Current Queue: {len(queue)} total, {len(ready_items)} READY, {len(used_topics)} historically used.")
    
    if len(ready_items) >= min_threshold:
        print(f"[+] Stock sufficient ({len(ready_items)} >= {min_threshold}). No restock needed.")
        return False
        
    print(f"[!] Stock low ({len(ready_items)} < {min_threshold})! Triggering AI Research Engine for {batch_size} new topics...")
    
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        
        system_instruction = (
            "You are the world-class Chief Wildlife Documentary Researcher & Scriptwriter for the global YouTube channel '4K Scenic Wildlife'. "
            "You produce ultra-engaging, scientifically accurate, awe-inspiring 4K nature documentary short scripts with extreme audience retention."
        )
        
        prompt = f"""
Generate {batch_size} UNIQUE 4K wildlife documentary short concepts.
DO NOT use any of these historically used or existing topics:
{json.dumps([u for u in used_topics + [q.get('topic_title') for q in queue]], ensure_ascii=False)}

For EACH topic, provide a JSON object with:
- topic_title: Catchy awe-inspiring concept name
- hook_sentence: 0-3 second scroll-stopping hook (English)
- script_lines: array of 5-7 dramatic, punchy narration lines (~45-55s total)
- search_keyword: 3-5 English keywords to search 4K video clips on Pexels (e.g. 'eagle flying mountains')
- youtube_title: Clickable title under 80 chars ending with #Shorts
- youtube_description: 2-3 sentences description with 5 relevant hashtags
- youtube_tags: array of 6-8 tags
- slot_time: Rotate sequentially between '10:34', '15:48', '20:23'

Output valid JSON array ONLY.
"""
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7,
                response_mime_type="application/json"
            )
        )
        
        new_topics = json.loads(response.text)
        print(f"[+] Generated {len(new_topics)} fresh topics from Gemini API.")
        
        slots = ["10:34", "15:48", "20:23"]
        start_idx = len(queue) + 1
        
        for i, t in enumerate(new_topics):
            t["id"] = f"WILDLIFE_{start_idx + i:03d}"
            t["status"] = "READY"
            if not t.get("slot_time"):
                t["slot_time"] = slots[i % 3]
            queue.append(t)
            
        save_queue(queue)
        print(f"[+] Successfully restocked! New queue total: {len(queue)} items ({len([q for q in queue if q.get('status') == 'READY'])} READY).")
        return True
    except Exception as e:
        print(f"[-] Restock failed with error: {e}")
        return False

if __name__ == "__main__":
    check_and_restock()
