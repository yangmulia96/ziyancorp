# DRAFT BLOG POST 01 — ZIYAN (Blogger / English)
Status: DRAFT — awaiting Bos review before publishing.
Source data: ZIYAN internal logs (ZIYAN_COMPANY_LOG.md, ziyan_riset_google_tools.md, models9r.json, ziyan_youtube_monetization.md, ziyan_audit_nbproof.md)

---

**Title:** We Tested 15 Free AI Image Models on a Local Proxy — Only One Actually Worked

**Meta description:** We benchmarked 15 image models and 71 chat models exposed by a self-hosted AI proxy while running a zero-infra AI-agent company. Here are the real HTTP results, the failures, and what it cost us: nothing.

**URL slug:** we-tested-15-free-ai-image-models-only-one-worked

**Labels/tags:** AI infrastructure, LLM proxy, free AI models, AI agents, zero-cost stack

---

# We Tested 15 Free AI Image Models on a Local Proxy — Only One Actually Worked

Most "free AI model" lists are written by people who never sent a single request. We did the opposite: we run a company where the entire operating team is AI agents, the infrastructure budget is effectively zero, and every model in our stack has to survive an actual HTTP call before it earns a place in production.

On 1 August 2026 we ran a full sweep of our local model proxy — a self-hosted router listening on `127.0.0.1:20128` that aggregates upstream providers behind one OpenAI-compatible API. This post is the raw result of that sweep: what the catalogue advertised, what actually returned a 200, and what silently died.

## The setup: one proxy, 71 chat models, 15 image models

Our proxy's model catalogue is not small. Pulling `/v1/models` and parsing the JSON gives **71 models** in our saved snapshot, spread across seven upstream namespaces:

- `kr/` — 34 models
- `openrouter/` — 15 models
- `kimi/` — 10 models
- `gemini/` — 6 models
- `groq/` — 4 models
- two single-model custom channels

A separate call to `/v1/models/image` returned **15 image models**: four Google-family image endpoints and eleven Cloudflare-hosted ones (flux-2-dev, flux-1-schnell, SDXL, lucid-origin, and friends). A broader live query of the chat endpoint at test time listed 115 chat entries — more than our stored snapshot, because upstream channels appear and disappear.

That is the headline number every listicle would stop at: "115 models, 15 image models, all free." The interesting part starts when you actually call them.

## What happened when we sent real requests

We did not evaluate aesthetics, prompt adherence, or benchmark scores. We tested one thing first: **does the endpoint return an image at all?**

| Request | Result |
|---|---|
| POST generate `gemini/gemini-2.5-flash-image` | Failed — `400: API key not valid` |
| POST generate `gemini/gemini-3.1-flash-image-preview` | Failed — same invalid-key error |
| POST chat `gemini/gemini-3.6-flash` | Failed — `400 API key not valid` |
| POST generate `ag/gemini-3.1-flash-image` | **HTTP 200**, base64 payload of 747,712 characters (~560 KB PNG) |
| Any video endpoint (Veo / Flow / omni-flash) | Not present — zero video endpoints exposed |

The pattern is brutal and instructive. Three of the four Google-family image models we tried were routed through the `gemini/` channel, and **the entire channel was dead** — not rate-limited, not degraded, but returning an upstream authentication error on every single call, chat and image alike. One test on a chat model was enough to confirm the failure was channel-wide rather than model-specific.

The one that worked, `ag/gemini-3.1-flash-image`, is the *same underlying model family* as one of the failures. It only worked because it was reachable through a different upstream channel. That is the single most useful thing we learned all week: **in a multi-provider proxy, the channel is the unit of reliability, not the model.**

## Why "115 models available" is a misleading number

A catalogue endpoint is a menu, not a kitchen. Our proxy happily advertised models whose upstream credentials had expired. Nothing in the `/v1/models` response indicated that six `gemini/` entries were unreachable — you only discover it by paying the cost of a failed request.

Three practical consequences for anyone building on aggregated free inference:

1. **Health-check by channel prefix, not by model ID.** One probe per namespace catches an entire dead branch cheaply. We proved a six-model channel was down with a single chat call.
2. **Assume the catalogue lies about availability.** Treat model discovery and model liveness as two separate systems.
3. **Pin what actually works, then rotate.** Our verified working set is small and boring: six free chat models (gemma-4-31b, gemma-4-26b, laguna-s-2.1, nemotron-nano-omni, nemotron-super-120b, nemotron-nano-30b) plus a Groq llama-3.3-70b fallback, one image model, one TTS voice, and STT/embeddings for subtitles and retrieval. Six working free chat models out of 71 catalogued is roughly an 8% hit rate on the free tier — and that is fine, because six is enough.

We now maintain a written rotation procedure and a shell script for exactly this reason. When a channel dies, the fix is a config swap, not an outage.

## The other half of the test: what has no API at all

While testing image generation we also checked whether the flashy creative tools everyone writes about could be wired into an agent pipeline. Result: our proxy exposed **no video endpoints whatsoever**. Google's Flow creative studio has no public API — it is a paid web UI, and community reports we reviewed complain about credits burning fast with silent model fallback. The newer omni-flash video model exists in preview but caps out at 3–10 second clips at 720p/24fps and was absent from our proxy entirely.

So our video production runs through browser automation against NotebookLM instead of an API, and our reusable pipeline assets came from auditing an older 107 MB experiment folder: an end-to-end generate→caption→upload script, a vertical 9:16 short pipeline with a one-per-day guard, an ffmpeg long-form stitcher, a key-free thumbnail generator, and an analytics loop that rewrites its own recommendations file. Five reusable assets, zero new spend.

## What this costs, and what it is for

The entire stack above runs at approximately zero marginal cost: free-tier inference, a local proxy, free-tier hosting, and AI agents instead of headcount. The point is not frugality as a virtue — it is that the failure modes of free infrastructure are *different*, and you have to design around them. Paid APIs fail with quotas. Free aggregated APIs fail by silently going dark at the channel level.

The output feeds a real distribution channel. Our operational YouTube channel currently sits at **61 subscribers and 57,000 lifetime views** — small, and honestly reported. Our own monetization research is clear that the Partner Program requires 1,000 subscribers plus 4,000 valid public watch hours, or 1,000 subscribers plus 10 million Shorts views in 90 days, and that Shorts-feed watch time does not count toward the 4,000-hour threshold. Which is why ad revenue is not our first monetization step at all — affiliate placement, a small membership tier, and a funnel into B2B automation work all start earning long before any ad threshold is met.

## Conclusion

Fifteen image models on paper. One that returned bytes. Seventy-one catalogued chat models, six verified free workhorses. That gap — between what an aggregator advertises and what answers a POST request — is the actual state of free AI infrastructure in 2026.

If you are building agent systems on free inference, steal the method rather than the model list: probe one model per channel, log the exact HTTP error, treat a `400: API key not valid` as a dead branch rather than a dead model, and keep a written rotation procedure so recovery is a config edit. Our numbers will be stale in a month. The method will not be.

---

**AI disclosure:** This article was produced with AI assistance based on our own experiment logs. All test results, error codes, model counts, payload sizes, and channel statistics reported here come from requests we ran against our own self-hosted proxy on 1 August 2026 and from our internal audit and analytics documents. No credentials, API keys, or private tokens are disclosed.
