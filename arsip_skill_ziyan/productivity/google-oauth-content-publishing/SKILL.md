---
name: google-oauth-content-publishing
description: Agent Youtube/Blogger OAuth publishing and debug.
---

# Google OAuth Content Publishing

Use when the user wants to upload videos to YouTube, post/autopublish to Blogger, theme a Blogspot blog, or debug `403`/`400` from Google publishing APIs — driven by a Hermes agent holding a local OAuth token (no manual browser paste every run).

## Hard rules
1. **Verify before claiming.** After obtaining a token, call the API (list channels / list blogs) and report what actually comes back. Do NOT say "channel connected" / "our asset" just because a token file exists on disk — it may have been created by another instance (e.g. Hermes Desktop) or belong to a different account. This directly caused a real hallucination incident. Always pair the claim with the API response (HTTP 200 + entity name/id).
2. **Desktop client, not Web, for localhost/oob.** A Web OAuth client rejects `urn:ietf:wg:oauth:2.0:oob` ("must contain a domain"). Create an **OAuth client ID of type Desktop app**; its `redirect_uris` includes `http://localhost`, which works with the `code` exchange flow (Google redirects to `http://localhost?code=XXXX`, which 404s in browser — that's expected; copy the `code=` value).
3. **Consent screen = In production + External** lets the owner's Google account authorize without Google verification; refresh_token then does NOT expire after 7 days (unlike Testing mode, which expires in 7 days). User cap 100 is enough for personal use.
4. **Enable the API first.** Blogger API v3 must be enabled in the GCP project or every call 403s with "Blogger API has not been used". YouTube Data API v3 similarly. Enable at `console.cloud.google.com/apis/library`.

## Scopes
- YouTube upload: `https://www.googleapis.com/auth/youtube.upload` + `https://www.googleapis.com/auth/youtube.readonly`
- Blogger post: `https://www.googleapis.com/auth/blogger`
- Combine in one `scope` string (space-separated) so a single token covers both.

## Token exchange & refresh
See `scripts/exchange_token.py` (exchange auth `code` for tokens) and `scripts/verify_google_token.py` (refresh + list blogs/channels as proof). Store JSON at `ziyan_credentials/youtube_token.json`. Access tokens expire ~1h; always refresh before a publishing call. If a call returns 401 mid-session, refresh and retry — don't re-prompt the user for a new code.

## Blogger API v3 — works vs doesn't
- ✅ `posts.insert` (set `"status":"DRAFT"` to require human review before `LIVE`), `posts.update/delete/publish/revert/list/search`, `blogs.listByUser` (get Blog ID from auth user), `pageViews`.
- ❌ **NO `blogs.insert`** — a blog CANNOT be created via API. User creates it once at blogger.com; agent only fills content.
- ❌ Theme/template write is NOT covered by the `blogger` scope — changing the HTML theme must be done manually in Blogger UI. The agent can only generate the XML file.

## Blogger theme XML (critical)
To import a theme via Theme > Backup/Restore > Restore, the file MUST be well-formed XML:
- Start with `<?xml version="1.0" encoding="UTF-8" ?>` then `<!DOCTYPE html>` then `<html ...>`. NO text outside tags (else `org.xml.sax.SAXParseException: Content is not allowed in prolog`).
- Wrap ALL CSS in `<b:skin><![CDATA[ ...css... ]]></b:skin>` inside `<head>`. Do NOT paste raw CSS into the body or document root.
- Escape any literal `]]>` inside CSS comments as `]]]]><![CDATA[>`.
- Replace undefined XML entities (`&copy;`, `&mdash;`) with numeric (`&#169;`, `&#8212`).
- Keep `<b:section>`/`<b:widget>` (Header1, Blog1 type=Blog, Sidebar HTML1, Footer HTML2) so posts render.
- Verify with `python -c "import xml.dom.minidom; xml.dom.minidom.parse('file.xml')"` before handing over.
- Heavy CSS (80 particle dots, aurora `@keyframes`, `blur(120px)`, canvas) makes the blog slow and hurts perceived SEO — prefer a light theme (dark + Outfit font + static glow) unless the user asks for animation. Note: pasting raw `.css` into Edit HTML root also throws SAXParseException; either import the full XML or use Advanced > Add CSS.

## YouTube upload
- `yt-dlp` can upload with the OAuth token; verify channel with `channels?part=snippet,statistics&mine=true` first.
- NotebookLM video generation has NO public API — requires a logged-in browser session, so it is semi-manual, not fully agent-automatable.

## Verification
Run `scripts/verify_google_token.py` after any token change: refreshes, lists Blogger blogs, lists YouTube channels. Use its output as the proof in your report.

## Pitfalls
- Don't assume the authorized account is the blog/video owner — the consent screen picks whatever Google account the user clicks.
- Don't paste a Blogger theme CSS file into Edit HTML root — it SAX-errors. Import the XML or use Advanced > Add CSS.
- Access token 401 mid-session = expired; refresh and retry, don't re-prompt for a new code.
