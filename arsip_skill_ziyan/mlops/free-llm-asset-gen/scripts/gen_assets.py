#!/usr/bin/env python3
# gen_assets.py — Generate a YouTube Short script + full metadata via 9Router FREE models.
# Portable technique: stdlib urllib client (no `requests` needed), raw_decode trailing-text-safe
# parsing, delimited-output extraction, laguna -> groq fallback, word-count enforcement.
# Windows-native python safe (pass Windows-native or relative paths).
import argparse, urllib.request, json, os, re

API = "http://127.0.0.1:20128/v1/chat/completions"
KEY = os.environ.get("HERMES_CUSTOM_9ROUTER_API_KEY", "")
LAGUNA = "openrouter/poolside/laguna-s-2.1:free"
GROQ = "groq/llama-3.3-70b-versatile"

DEFAULT_TOPIC = "Wall Street week ahead: Home Depot and Walmart report earnings, minutes of Fed meeting are released"
DEFAULT_URL = "https://news.google.com/rss/articles/CBMimgJBVV95cUxOUWoyc0g5cHQycVU5c29uOU9tNU1QQU8tZEpvSDdqV083QlBldWRZMXJDRDhQTzdBNzhSVFM4Nm9Sb3dfdEpYRG81SjZVMDR2dnFDdkxSaWVQOWtoNDkwLU1NQTdhNHVlNUowTHF3TmlFRGk3eC1RVDlwRmFmZ0FFNVZHX2pFSU41OEVkc3NKY2xkcDVTWEJ1RW1ZYkhnMXZraWFCaGVKSHFidTZzUlVUdjJFR081c09tTHBhTGJZRnZtN3RMQlZSdTJRMFZ0U011T181M2s4UEw4SkhiNVcyUmkzZWo5cVNreVNFaDZNREhVTFNfZ1lkM3Vua1NZdXVDMmY4VlY2ZVdVNmRpb2FOUzFxeVoyWEZWX1E?oc=5"

PROMPT_VIDEO = """You are a YouTube Shorts scriptwriter for 'Compound Daily' — a channel on Technology, AI, Business, and Finance for a US/international audience. Write a YouTube SHORT script (exactly {lo}-{hi} words, spoken English, hook in the FIRST sentence, factual, no fluff, no hashtags inside the script). Topic: {topic}. Then provide YouTube upload metadata. Output EXACTLY this format, one value per line, NO newlines inside a value, NO markdown code fences, NO extra text:
SCRIPT: <narration script, {lo}-{hi} words>
TITLE: <YouTube title, max 60 chars, catchy, English>
DESC: <1-2 sentence description with 3-5 relevant hashtags>
TAGS: <comma separated SEO tags>"""

PROMPT_SOCIAL = """Write social-media promo posts for a YouTube Short about: {topic}. Output EXACTLY this format, one value per line, NO newlines inside a value, NO markdown code fences, NO extra text:
X1: <tweet 1>
X2: <tweet 2>
X3: <tweet 3>
X4: <tweet 4>
X5: <tweet 5>
TG: <Telegram post>
LI: <LinkedIn post>
BLOG: <short blog paragraph 60-90 words>"""

PROMPT_EXPAND = """Expand the following YouTube Short script to EXACTLY {lo}-{hi} words. Keep the opening hook. Return ONLY one line in this exact format, no extra text:
SCRIPT: <expanded script>

Original script:
<<<{script}>>>"""


def call(prompt, max_tokens, prefer_laguna=True):
    order = [LAGUNA, LAGUNA, GROQ, GROQ] if prefer_laguna else [GROQ, GROQ]
    last = None
    for m in order:
        try:
            body = json.dumps({"model": m,
                               "messages": [{"role": "user", "content": prompt}],
                               "max_tokens": max_tokens, "temperature": 0.7}).encode()
            req = urllib.request.Request(API, data=body,
                 headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=120) as r:
                raw = r.read().decode("utf-8", "replace")
            obj, _ = json.JSONDecoder().raw_decode(raw)  # tolerate trailing text
            c = obj["choices"][0]["message"]["content"]
            if c and c.strip():
                return c, m
            last = f"{m}:empty"
        except Exception as e:
            last = f"{m}:{e}"
    raise RuntimeError(f"all models failed: {last}")


def parse(text):
    d = {}
    for line in text.splitlines():
        m = re.match(r'^([A-Z0-9]+):\s*(.*)$', line)
        if m:
            d[m.group(1)] = m.group(2).strip()
    return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--topic", default=DEFAULT_TOPIC)
    ap.add_argument("--url", default=DEFAULT_URL)
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--min-words", type=int, default=120)
    ap.add_argument("--max-words", type=int, default=180)
    a = ap.parse_args()
    os.makedirs(a.outdir, exist_ok=True)

    v_txt, v_model = call(PROMPT_VIDEO.format(topic=a.topic, lo=a.min_words, hi=a.max_words), 800)
    v = parse(v_txt)
    script = v.get("SCRIPT", "")
    wc = len(script.split())
    if wc < a.min_words or wc > a.max_words:
        ex_txt, ex_model = call(PROMPT_EXPAND.format(lo=a.min_words, hi=a.max_words, script=script), 500)
        ex = parse(ex_txt)
        if ex.get("SCRIPT"):
            script = ex["SCRIPT"]
            v_model = f"{v_model}->expand:{ex_model}"

    s_txt, s_model = call(PROMPT_SOCIAL.format(topic=a.topic), 900)
    s = parse(s_txt)

    title = v.get("TITLE", "")
    desc = v.get("DESC", "")
    tags = [t.strip() for t in v.get("TAGS", "").split(",") if t.strip()]
    x = [s.get(f"X{i}", "") for i in range(1, 6)]
    tg = s.get("TG", "")
    li = s.get("LI", "")
    blog = s.get("BLOG", "")

    with open(f"{a.outdir}/script_short.md", "w", encoding="utf-8") as f:
        f.write(script + "\n")
    meta = {
        "primary_topic": a.topic,
        "source_url": a.url,
        "model_used": f"{v_model} (video) / {s_model} (social) via 9Router",
        "youtube": {"title": title, "description": desc, "tags": tags, "category": 28, "privacy": "public"},
        "x_thread": x,
        "telegram": tg,
        "linkedin": li,
        "blog": blog,
        "qc": {"script_word_count": len(script.split()),
               "script_in_range": a.min_words <= len(script.split()) <= a.max_words},
    }
    with open(f"{a.outdir}/metadata_qc.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)

    print("models:", v_model, "/", s_model)
    print("script words:", len(script.split()), "(range", a.min_words, "-", a.max_words, ")")
    print("WROTE script_short.md + metadata_qc.json ->", a.outdir)


if __name__ == "__main__":
    main()
