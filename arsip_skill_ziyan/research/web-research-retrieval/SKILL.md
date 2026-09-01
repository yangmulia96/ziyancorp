---
name: web-research-retrieval
description: Search engine blocked or junk? Ladder to real sources.
---

# Web Research Retrieval — when the normal search path is blocked

Use whenever a research task needs real external sources and the direct route
misbehaves: captcha pages, `ERR_SSL_VERSION_OR_CIPHER_MISMATCH`, empty snapshots,
SERP results that are wildly off-topic (a sign the engine served a cached/junk
page), or a site returning 403 to scripted requests.

The rule: **climb the ladder, never fabricate.** A report with 6 real sources plus
an honest "this platform was unreachable" note beats 10 invented ones.

## Escalation ladder

1. **Reader proxy over a SERP** — most reliable general fallback:
   ```bash
   curl -s --max-time 60 "https://r.jina.ai/https://duckduckgo.com/html/?q=<urlencoded query>"
   ```
   Parse titles + destination URLs out of the markdown:
   ```python
   items = re.findall(r'## \[(.+?)\]\(https://duckduckgo\.com/l/\?uddg=([^&]+)', out)
   [(t, urllib.parse.unquote(u)) for t, u in items]
   ```
2. **Reader proxy over the article** — `https://r.jina.ai/<article-url>` renders
   Medium, dev.to, Substack, GitHub READMEs and most blogs as clean markdown.
   Save each fetch to a scratch dir (`_res/<slug>.md`) and read it back in slices
   with `read_file(offset=..)`. Never dump a whole article into context.
3. **Open APIs instead of scraping** — for practitioner experience and real numbers:
   - Hacker News: `https://hn.algolia.com/api/v1/search?query=<q>&tags=story&hitsPerPage=15`,
     then `https://hn.algolia.com/api/v1/items/<objectID>` and walk `children` for
     the comment tree (where the honest numbers usually live).
   - arXiv, GitHub REST, PyPI, npm registry — unauthenticated and unblocked.
4. **Source repos / docs as primary evidence** — a GitHub README often states the
   architecture, the live product URL, and cost details better than any blog post.
5. **Batch it.** Put the whole loop (queries → fetch → regex → print a compact
   digest) inside one `execute_code` call. Serial one-tool-per-turn burns context
   and time; a single script over 5 queries returns a clean shortlist.

## Reporting discipline

- Record every URL actually opened, with the date of access.
- Explicitly list sources you could **not** reach and why (403, paywall, truncated).
  This is part of the deliverable, not an admission of failure.
- Do not quote figures from an article whose body was paywalled/truncated — mark
  them "unverified" or drop them.
- Grade confidence: HIGH (≥2 independent sources, ≥1 primary), MEDIUM (1 primary or
  ≥3 secondary), LOW (single blog / opinion).

## Pitfalls

- Verify result titles actually relate to the query before mining them. If a query
  about AI YouTube channels returns Intel XTU forum threads, the engine served junk
  — switch rungs rather than reading the results.
- `r.jina.ai` can be slow; always pass `--max-time 60..70` so a hung fetch doesn't
  eat the turn.
- Marketing/SEO blogs dominate SERPs for "case study" queries. Prefer first-person
  engineering write-ups (dev.to, personal blogs, repos) and forum threads over
  vendor "case study" landing pages, which rarely contain real numbers.

## Knowledge banks

- `references/ai-youtube-agent-case-studies.md` — real case studies of YouTube
  channels run by AI agents: stacks, published numbers, pitfalls, platform policy.
- `references/youtube-video-fact-checking.md` — API validation ladder for verifying
  tools, models, pricing, repos, and voice claims cited in YouTube tutorial videos.
