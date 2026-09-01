# Job Hunter — ZIYAN Build Blueprint

## Architecture (proven patterns from research)
- **Multi-agent > single agent.** Winning pattern: Scout (find) → Analyst (verify) → Scorer (rank vs CV) → Writer (docs) → Critic (review) → Captain (orchestrate). Human-in-loop: only post/apply when score ≥ threshold.
- **Anti-ban:** avoid raw LinkedIn scraping. Use **JSearch / Adzuna** via RapidAPI (free tier) — stable, covers Indeed/Glassdoor/LinkedIn aggregated.
- **Notify:** Telegram (Orion) or WhatsApp deep-link.

## Reference repos (GitHub)
- `adarsh-ajay/Job-Hunter` (18★) — n8n workflow: Schedule → Drive CV → Sheet profil → Scrape LinkedIn → AI Agent (Gemini) → Score → If ≥50 → Telegram. Downloaded to `ziyan_n8n_templates/job_hunter_workflow.json`.
- `leopu00/job-hunter-team` (39★) — multi-agent team, container, Telegram, ~€40-200/mo LLM.
- `powerycy/BossHunter` (175★), `pedrohlucena/hunter` (91★), `saeedkolivand/ai-job-hunter-app` (41★).

## ZIYAN adaptation (built this session)
- **Workflow:** `ziyan_n8n_templates/ziyan_job_hunter.json` — Schedule 08:00 → JSearch API (not LinkedIn) → Parse → AI Score via **9router** (openrouter/auto, score≥70) → Telegram Orion.
- **Landing page (FREE):** section `#job-hunter` injected into `ziyan/ziyancorp/src/App.jsx` (React+Vite+Tailwind). Deploy: `npx gh-pages -d dist`. Live at https://yangmulia96.github.io/ziyancorp/ . Paket Rp99.000/bln, WhatsApp CTA (placeholder number — replace before launch).
- **Budget:** $0 — GitHub Pages + free API tiers + open-source. No paid tools.

## Pitfalls
- JSearch needs `RAPIDAPI_KEY` env + `TELEGRAM_CHAT_ID`.
- LinkedIn raw scrape → IP block; prefer aggregated APIs.
- WhatsApp link in landing is placeholder (`6281234567890`) — must be replaced with Bos's real number.
