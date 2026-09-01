# Curl-based HTML Retrieval — when browser tools return empty pages

When `browser_navigate` / `browser_snapshot` returns `(empty page)` or a Cloudflare
challenge page, but `curl` in `terminal` succeeds, the content is served as
server-rendered HTML that bots-with-heads (the browser tool) can't render, or
the site's JS is behind a bot-gate that curl bypasses.

## Quick pattern

```bash
# 1. Save the page to a temp file
curl -s <url> -o /tmp/page.html

# 2. Grep for the data you need — titles, URLs, dates
grep -oP '(?<=<a href=")[^"]*(?=" class="storylink")' /tmp/page.html
grep -oP '(?<=class="title">)[^<]+' /tmp/page.html
grep -oP '(?<=content=")[^"]+' /tmp/page.html | head -10

# 3. Or extract JSON-LD / meta tags
curl -s <url> | grep -oP '(?<="og:title" content=")[^"]+'
```

## Sites that work well with curl (plain HTML)

| Site | Notes |
|------|-------|
| Hacker News (`news.ycombinator.com`) | Plain HTML tables, trivially grep-able. `storylink` class for article links. |
| The Verge (`theverge.com`) | Full HTML via curl, no bot challenge. |
| Substack (`blog.comfy.org`) | Returns JSON-LD + full post HTML via curl. |
| Personal blogs (Gatsby, Markdown-rendered) | Usually works. |

## Sites that block curl (Cloudflare / bot walls)

| Site | Symptom |
|------|---------|
| `openai.com/blog` | Cloudflare `__cf_chl_opt` challenge page. |
| `arstechnica.com` | Bot detection / redirect loop. |

## When curl fails, fall back further

1. `r.jina.ai` reader proxy (covered in main skill escalations).
2. Hacker News Algolia API for HN content instead of HTML scraping.
3. For article-level content, check if the site has an RSS feed (often clean XML).

## Pro Tip

```bash
# Extract meta description + title in one shot
curl -s <url> | grep -oP '<(title|meta name="description" content=")[^>]*>' | \
  sed 's/.*content="//;s/"[^>]*$//'
```