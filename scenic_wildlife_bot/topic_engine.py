import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
import json
import random
import datetime
from google import genai

GEMINI_API_KEY = "AQ.Ab8RN6Jh-jeCGKc3YTcSuVsaHUrVonnc4mUeJGqvAtbmGSd9mQ"
client = genai.Client(api_key=GEMINI_API_KEY)

TOPICS_ARCHIVE_FILE = os.path.join(os.path.dirname(__file__), "used_topics.json")


def load_used_topics():
    if os.path.exists(TOPICS_ARCHIVE_FILE):
        with open(TOPICS_ARCHIVE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_used_topic(topic_title):
    used = load_used_topics()
    used.append(topic_title)
    with open(TOPICS_ARCHIVE_FILE, "w", encoding="utf-8") as f:
        json.dump(used, f, ensure_ascii=False, indent=2)


def generate_topic_and_script():
    used_topics = load_used_topics()
    used_str = "\n".join(f"- {t}" for t in used_topics[-30:]) if used_topics else "(none yet)"

    prompt = f"""You are a viral YouTube Shorts content strategist specializing in GLOBAL 4K nature and wildlife documentaries.

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

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )
    raw = response.text.strip()

    # Clean markdown if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    data = json.loads(raw)
    return data


if __name__ == "__main__":
    print("Generating viral wildlife topic and script...")
    data = generate_topic_and_script()
    print(json.dumps(data, indent=2, ensure_ascii=False))
