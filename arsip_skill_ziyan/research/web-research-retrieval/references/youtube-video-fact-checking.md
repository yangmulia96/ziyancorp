# YouTube Video Fact-Checking — API Validation Ladder

When a YouTube video cites specific tools, models, prices, repos, or API endpoints,
**verify each claim against the live source** before trusting or reusing it. This is
an extension of the "climb the ladder, never fabricate" principle — applied to
claims made *in* video content rather than found *via* search.

## When to use

- A tutorial video names specific GitHub repos, model IDs, pricing, or voice names.
- The video's claims will drive ZIYAN build decisions or cost estimates.
- You need to confirm tools are still live and claims still hold.

## The validation checklist

For each named entity in the video, hit its **primary source API**:

| Claim type | Source to hit | What to verify |
|---|---|---|
| GitHub repo | `api.github.com/repos/{owner}/{repo}` | Exists, not archived, language, star count, last updated |
| Model name | Provider's model API | Exists, pricing (free vs paid), context length |
| Voice name | Provider's voice list API | Voice exists, voice_id matches |
| Web URL | `curl -sL -o /dev/null -w "%{http_code}" <url>` | HTTP 200, final URL (watch redirects) |
| Pricing | Provider's pricing/API page | Free tier limits, per-token/credit cost |

## OpenRouter-specific pattern

```bash
# 1. Fetch all models with pricing
curl -sL "https://openrouter.ai/api/v1/models" | python3 -c "
import sys, json
data = json.load(sys.stdin)
models = data.get('data', [])
for m in models:
    mid = m.get('id','')
    pricing = m.get('pricing', {})
    print(f'{mid} | prompt={pricing.get(\"prompt\",\"?\")} | completion={pricing.get(\"completion\",\"?\")}')
"
```

**Key insight:** A model ID containing `:free` is genuinely free. Models without `:free`
(like `z-ai/glm-5.2` at $0.50/$3.15 per 1M tokens, or `minimax/minimax-m3` at $0.30/$1.20)
are **paid** — even if the video claims they're "free." Always check `pricing` in the API
response, not just the model name.

```bash
# Filter for genuinely free models only
free_models = [m for m in models if ':free' in m.get('id', '')]
```

## GitHub repo validation pattern

```bash
# Check if repo exists and is active
curl -sL "https://api.github.com/repos/{owner}/{repo}" | python3 -c "
import sys, json
data = json.load(sys.stdin)
if data.get('message') == 'Not Found':
    print('REPO NOT FOUND')
else:
    print(f'Stars: {data.get(\"stargazers_count\")}')
    print(f'Language: {data.get(\"language\")}')
    print(f'Created: {data.get(\"created_at\")}')
    print(f'Updated: {data.get(\"updated_at\")}')
    print(f'Archived: {data.get(\"archived\")}')
"
```

## ElevenLabs voice validation pattern

```bash
# Verify voice exists before using a claimed voice_id
curl -H "Accept: application/json" "https://api.elevenlabs.io/v1/voices" | python3 -c "
import sys, json
data = json.load(sys.stdin)
voices = data.get('voices', [])
target = 'JBFqnCBsd6RMkjVDRZzb'  # George from video
match = [v for v in voices if v['voice_id'] == target]
print(f'Voice found: {match[0][\"name\"]}' if match else 'NOT FOUND')
"
```

## Cross-check pricing claims

- **NVIDIA** (build.nvidia.com): "Free inference with leading models" — verify rate
  limits (~40 rpm, ~10K req/day) and which models are actually free vs. paid NIMs.
- **ElevenLabs** (elevenlabs.io/pricing): Free tier = 10,000 credits/month, then
  $0.36 → $0.20 → $0.18 → $0.17 per 1k chars (descending with tier).
- **Zapier**: Free tier exists (100 tasks/mo). n8n can be self-hosted for $0.
- Always cross-check the video's specific URL (e.g., `build.nvidia/models` vs `build.nvidia.com`).

## Confidence grading

After validation:
- **HIGH**: 2+ independent sources confirm; pricing/model/voice all verified live.
- **MEDIUM**: 1 primary source verified; some details inferred or from docs only.
- **LOW**: Single source (the video itself); claims unverified.
- **BUNK**: Repo 404, model not in API, voice not found, URL returns 404/403.

## Example from session (2026-08-13)

Video claimed NVIDIA free models include "GLM 5.2" and "MiniMax M3".
- **GLM 5.2** (`z-ai/glm-5.2`): Found on NVIDIA catalog AND on OpenRouter, but on OpenRouter
  it is **paid** ($0.50/$3.15 per 1M tokens). On NVIDIA, pricing not explicit but likely
  requires API key + rate-limited. Verdict: MEDIUM — not clearly "free."
- **MiniMax M3** (`minimax/minimax-m3`): Not found on NVIDIA models page at all. On OpenRouter
  it is **paid** ($0.30/$1.20 per 1M tokens). Verdict: BUNK for "NVIDIA free model."
- **Actual free models on OpenRouter** (16 total): nvidia/nemotron-*, poolside/laguna-*,
  google/gemma-4-*, openai/gpt-oss-20b:free, liquid/lfm-2.5-2.6b:free.

## Complement: metadata extraction

`yt-dlp --dump-json <url>` returns complete video metadata (title, channel, duration,
chapters, description, thumbnail URLs) in one call. Use this alongside the transcript
API to get both metadata and text. The JSON output also reveals all available subtitle
languages via the `_x` / subtitle fields — useful when a video's transcript language
isn't obvious.

## Related techniques

- `references/curl-html-retrieval.md` — when browser tools return empty pages
- `references/ai-youtube-agent-case-studies.md` — YouTube AI channel case studies
- `media/youtube-content` skill — transcript fetching (uses youtube-transcript-api v1.x
  `.fetch()` method on `YouTubeTranscriptApi()` instance, not the legacy `.get_transcript()`)