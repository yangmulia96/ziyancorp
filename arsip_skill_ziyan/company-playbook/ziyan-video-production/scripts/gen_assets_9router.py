#!/usr/bin/env python3
"""Generate Compound Daily content assets via 9Router (FREE models).
Delimited per-line output (NO JSON - free models emit bad JSON) +
poolside->groq fallback + Windows-native paths (avoid MSYS double-prefix bug).
Usage: python3 gen_assets_9router.py <stage_dir>
EDIT the PROMPT block below per topic before running.
"""
import os, json, re, urllib.request, sys

KEY = os.environ.get("HERMES_CUSTOM_9ROUTER_API_KEY")
URL = "http://127.0.0.1:20128/v1/chat/completions"

# ===== EDIT THIS PROMPT PER TOPIC (use real verified facts) =====
PROMPT = """You are a senior tech-finance video scriptwriter for YouTube channel "Compound Daily" (niche: Technology, AI, Business, Finance; US English audience). Write assets about this REAL breaking news.

FACTS:
- <fill with verified facts>

Output ONLY the delimited fields below, exactly one value per line, NO markdown, NO blank lines between fields, NO extra commentary. Do not put newlines inside any value.
SCRIPT: <NotebookLM source narrative, English, 300-340 words, engaging hook + 3 clear points + tight close. Video voiceover source. Factual, no hype.>
TITLE: <YouTube title, max 95 characters, punchy, curiosity/number-driven>
DESC: <YouTube description, 2-3 sentences, end with soft CTA to subscribe. No price.>
TAGS: <6-9 comma-separated YouTube tags>
X1: <Tweet 1 hook, max 280 chars>
X2: <Tweet 2>
X3: <Tweet 3>
X4: <Tweet 4>
X5: <Tweet 5>
TG: <Telegram post, 2-3 sentences, natural, no price, 4 hashtags at end>
LI: <LinkedIn post, professional, 3-4 sentences, hook + insight>
BLOG: <Blog article, 160-200 words, informational, short headline line first>
"""
# =======================================================

def call(model):
    body = json.dumps({"model": model, "messages": [{"role": "user", "content": PROMPT}],
                       "max_tokens": 2500, "temperature": 0.7}).encode()
    req = urllib.request.Request(URL, data=body, headers={
        "Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        raw = r.read().decode("utf-8")
    try:
        data = json.loads(raw)
    except Exception:
        data, _ = json.JSONDecoder().raw_decode(raw)
    return data["choices"][0]["message"]["content"]

content = None
used = None
# NOTE (2026-08-17): a green poolside TEST call is NOT proof generation works.
# Always wrap the real generation call in this fallback loop.
for m in ["openrouter/poolside/laguna-s-2.1:free", "groq/llama-3.3-70b-versatile"]:
    try:
        content = call(m); used = m; print("OK", m, len(content)); break
    except Exception as e:
        print("FAIL", m, repr(e)[:160]); content = None
if not content:
    raise SystemExit("ALL MODELS FAILED")

fields = {m.group(1).upper(): m.group(2).strip()
          for m in re.finditer(r"^([A-Z0-9_]+):\s*(.*)$", content, re.MULTILINE | re.I)}
print("PARSED:", list(fields.keys()), "MODEL:", used)
json.dump(fields, open("gen_fields.json", "w"), indent=2)

STAGE = sys.argv[1] if len(sys.argv) > 1 else "C:/Users/arija/workdir/videos/compound_stage"
os.makedirs(STAGE, exist_ok=True)
open(f"{STAGE}/script.md", "w").write(fields.get("SCRIPT", ""))
tags = [t.strip() for t in fields.get("TAGS", "").split(",") if t.strip()]
meta = {"youtube_title": fields.get("TITLE", ""), "youtube_description": fields.get("DESC", ""),
        "tags": tags, "model_used": used}
json.dump(meta, open(f"{STAGE}/metadata_qc.json", "w"), indent=2)
open(f"{STAGE}/social_twitter_thread.md", "w").write("\n\n".join(fields.get(f"X{i}", "") for i in range(1, 6)))
open(f"{STAGE}/social_linkedin.md", "w").write(fields.get("LI", ""))
open(f"{STAGE}/social_telegram.md", "w").write(fields.get("TG", ""))
open(f"{STAGE}/blog.md", "w").write(fields.get("BLOG", ""))
print("STAGED ->", STAGE)
