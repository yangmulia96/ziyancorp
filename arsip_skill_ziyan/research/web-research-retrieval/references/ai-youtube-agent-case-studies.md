# Knowledge bank: YouTube channels run by AI agents (real cases, not theory)

Gathered via the reader-proxy + HN-API ladder. Reddit was unreachable (403) during
collection, so no r/juststart or r/thesidehustle data is included.

## Cases with published detail

| Case | Stack | Published results |
|---|---|---|
| `pranshu97/content-foundry` → channel `@TheCrackedEng` (states "100% generated, voiced, published autonomously") | Multi-agent Python: Data Fetcher → Script Generator (LLM) → **Judge** (quality rubric) → Voiceover → Visuals → Render → Publish. TTS: Edge (free) / Piper offline / Chatterbox local voice-clone (MIT) / ElevenLabs. Visuals: Pexels+Pixabay B-roll or Pillow title cards. Research: free DuckDuckGo + YouTube API "outlier mining". SQLite state, per-stage resume, Streamlit review dashboard, Telegram notify, hard monthly budget cap, synthetic-content disclosure by default, publishes Private/Unlisted first | subs/revenue not published (unverified) |
| dev.to "I Let AI Agents Run My YouTube Channel for 6 Weeks" (wcamon, Feb 2026), medical-history Shorts | Two Claude agents with **persistent memory**: "Midnight" (production, analytics, strategy), "Dusk" (X/Twitter, blog, distribution). Custom media engine + TTS, 14–15 language translations per video, YouTube Data API upload. Explicitly anti-n8n/Make: "tools have no memory, context, or judgment" | **6 weeks: 52 videos, 30,170 views, 29 subscribers**, 4–5% like rate (niche normal 1–2%), one video 474 min watch time / 109% loop rate. Human-in-the-loop: agent pitches, human approves |
| dev.to "I Built This Entire YouTube Channel With AI — The Full Stack" (The Machine Pulse, Mar 2026), 4 channels 1 codebase | 10-step one-command CLI: script JSON + SHA-256 hash → Google Cloud TTS Chirp 3 HD (per-channel voice) → Whisper word-alignment for timing → Vertex AI Imagen 3 (65 images/episode) → FFmpeg (mix, music, subs, grading) → artifact verification. **100-point "humanize score"** (AI-fingerprint words, "you"-count, avg sentence <12 words, named people/exact numbers, hook quality); <90 → Gemini 2.5 Flash auto-rewrites. Gemini + Google Search live fact-grounding. Auto 5 Shorts/episode, each scored /10. Channels differ only by YAML config | **< $5 per episode** (images $4.20, TTS $0.21, Gemini $0.10, FFmpeg/Whisper free). ~80% automated; topic choice and taste stay human |
| Medium "Fully Automated Top 10 Channel With n8n" (owaiss, Apr 2026) | n8n: AI generates 10 evergreen ideas → Google Sheets as content queue → LLM structured JSON (intro/outro/ranking/image prompts) → video API → async polling → auto-upload | Works end-to-end; no performance numbers |
| Medium (Nitin Gavhane, Jun 2026) | Google **NotebookLM Video Overviews** uploaded straight to YouTube. Automation ecosystem: `void-mckenzie/NotebookLM_Youtube_Automator`, `rumilog/notebooklm-automate`, Chrome ext "Video Automator for NotebookLM" | Practical walkthrough; numbers not disclosed |
| Medium/MoneyHive "What I Learned After Failing My First Automated Channel" | Slideshow + robotic TTS | First channel failed; now runs 4 faceless tech-tutorial channels that earn. "Automation isn't a scam, but how it's sold to beginners is" |
| HN threads 45894359 / 45949988 / 43101593 | MoviePy + upload bot; gaming highlights | 20 videos → 47 subs; 8 months → 50k subs but only ~$200/mo on a $2–4 CPM niche |
| Screen Culture, KH Studio (negative case) | Mass-produced fake AI movie trailers | **Terminated.** Jan 2026: 16 large channels (4.7B views, ~$10M/yr) removed from YPP |

## NotebookLM-Specific Monetization Case Studies (Aug 2026)

### AIpreneur — "NotebookLM + Gemini: How I'd Start a Faceless Channel to Get Monetized Fast"
- **Source**: YouTube video (10,072 views as of Jul 5, 2026), channel 23.9K subs
- **System**: 6 NotebookLM notebooks feeding 2 custom Gemini Gems
  - **Research Notebooks**: competitor research, audience psychology, hook & retention, video technique, visual identity, AI tool reference
  - **Gemini Gems**: Story Engine (voiceover scripts) + Asset Generator (image/video prompt tables)
- **Production Stack**: ElevenLabs (voiceover) → Google Flow/Nano Banana 2 + Veo 3 (visuals) → CapCut (assembly)
- **Workflow**: Build notebooks once → every new video starts from a single topic
- **Commentary (real user feedback)**:
  - "@a1.republic": "notebooklm + gemini combo is slept on for research speed. 'monetized fast' is doing some heavy lifting tho, that part's never fast"
  - "@chewch3223": "SYSTEM. Self improvement, motivation."
  - "@MillieMacko": "Great video !! SYSTEM: roman empire history"
- **Confidence**: MEDIUM (direct video transcript + comments, no revenue numbers disclosed)
- **Access path**: YouTube search worked; direct video access hit "element not found" / bot detection barriers

### NotebookLM Video Overview Automation (Medium sources)
- **Tools**: `void-mckenzie/NotebookLM_Youtube_Automator`, `rumilog/notebooklm-automate`
- **Approach**: Generate Video Overviews from NotebookLM → upload directly to YouTube
- **Revenue/performance**: Not disclosed in available sources
- **Access**: Medium blocked by Cloudflare during this research session

### Research Access Barriers Encountered (Aug 2026)
| Platform | Method | Result |
|---|---|---|
| Reddit | Direct API (`/r/notebooklm/new.json`) | HTTP 403 |
| Reddit | Browser (`old.reddit.com`) | Cloudflare challenge |
| Medium | Search + article access | Cloudflare "Just a moment..." |
| YouTube | Search results | Accessible (found 10+ relevant videos) |
| YouTube | Individual video pages | Mixed — some accessible, some "element not found" / unavailable |
| Jina AI Reader | Not tested this session | Recommended as rung 2 fallback |

## Engineering pitfalls that actually bit people

- **Silent failures are the killer**: image generation failed, pipeline continued, three episodes shipped with black frames. Fail loud; verify every artifact before render.
- **Stale cache on resume**: edited script, restarted mid-pipeline, old audio reused. Hash content and compare on resume.
- **Async handling is the hardest part** of any video pipeline — needs state tracking, polling, recovery.
- **Duration control is unreliable**: a 60s target came out 41s. What worked: spell numbers as words, explicitly request "SLOW PACING", specify 8–10 seconds per scene.
- **YouTube Analytics API lags 72+ hours** — real-time optimization is impossible; agents decide on incomplete data.
- **Agents can't judge story quality** — they fact-check and produce; they can't tell whether something makes a person *feel*.
- **Volume ≠ subscribers**: 52 videos / 30k views → 29 subs.
- **CTAs on Shorts get ~zero replies** regardless of format — platform behavior, not an agent defect.
- **Niche CPM decides everything**: check CPM before producing. Tech/AI/business/finance are high; gaming commentary is $2–4.
- **NotebookLM output uniformity risk**: two-host talking-head format is highly templated — strong candidate for "mass-produced" flagging if used raw at volume. Differentiate with format variation and editorial fingerprint.

## Platform policy (the existential risk)

- YouTube now evaluates **whole channels**, not individual videos, under the Inauthentic Content Policy.
- Flag triggers: overposting at a cadence no human editorial process supports; template clones (identical but for title); static image slideshows; zero commentary/added value.
- July 2025 policy update: **mass-produced AI content cannot be monetized**; human+AI hybrid is allowed and explicitly encouraged.
- Three strikes and the channel is gone. Keep asset backups and a multi-platform plan.
- Winning pattern: agent does 80–95% of the work, but the channel carries a visible editorial fingerprint (a point of view, exclusive data, format variation) and a human-plausible upload cadence.

## Tooling gap worth knowing

NotebookLM is a proven production route with public automation tooling, but its output is
highly uniform (two-host talking-head format) — a strong candidate for "templated /
mass-produced" flagging if used raw at volume. **OpenMontage has zero published case
studies** — no playbook exists, which is both a risk and a differentiation opportunity.