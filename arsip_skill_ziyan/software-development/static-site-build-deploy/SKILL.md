---
name: static-site-build-deploy
description: Build Vite/React/Tailwind sites and deploy to GitHub Pages.
---

# Static Site Build & Deploy (Vite + Tailwind → GitHub Pages)

Class of task: turn loose React source (often pasted from an LLM canvas) into a
built, verified, publicly live static site.

## 1. Scaffold (when only package.json + src/App.jsx exist)

- `vite.config.js` — **`base: '/<repo-name>/'`** is mandatory for project Pages,
  otherwise assets 404 at `/assets/...`.
- `tailwind.config.js` — `darkMode: 'class'`, `content: ['./index.html','./src/**/*.{js,jsx,ts,tsx}']`.
- `postcss.config.js`, `src/index.css` (`@tailwind base/components/utilities`).
- `src/main.jsx` → `createRoot(document.getElementById('root'))`.
- `index.html` with `<div id="root">` + `<script type="module" src="/src/main.jsx">`,
  and a `<link>` preload for any Google Font the design uses (don't rely only on
  a CSS `@import` inside a component `<style>` tag).
- Add `"type": "module"` to package.json, else ESM `export default` configs fail.
- `.gitignore`: `node_modules`, `dist`.

Never delete the previous `App.jsx` — copy it to `App_v1_old.jsx` first.

## 2. Build, and expect source repair

`npm run build`. If the source was pasted from an LLM canvas (Gemini/Claude/ChatGPT),
it is very likely **hard-wrap corrupted**: string literals broken across newlines
and sometimes the file truncated mid-token. Do not hand-fix line by line —
see `references/repairing-hardwrapped-jsx.md` and `scripts/unwrap-jsx.mjs`.

esbuild reports syntax errors one at a time — budget several build passes.

## 3. Verify BEFORE deploying

Run `npx vite preview --port <p> --strictPort` in the background, open it, and
assert the design features exist in the DOM rather than eyeballing:

```js
[document.querySelectorAll('.animate-float').length,
 document.querySelectorAll('.animate-ambient-pulse').length,
 document.querySelectorAll('.animate-gradient-xy').length,
 getComputedStyle(document.querySelector('h1')).fontFamily]
```

This catches missing fonts and dead animation classes a screenshot may not.

## 4. Deploy to GitHub Pages

```bash
git add -A && git commit -m "..." && git push origin main
rm -rf /tmp/ghp && mkdir -p /tmp/ghp && cp -r dist/. /tmp/ghp/
touch /tmp/ghp/.nojekyll
cd /tmp/ghp && git init -q && git checkout -q -b gh-pages && git add -A \
  && git commit -q -m "Deploy" \
  && git remote add origin "$(cd <repo> && git remote get-url origin)" \
  && git push -q -f origin gh-pages
```

Set the Pages source via API (token read from an env file, never printed):

```bash
curl -s -o /dev/null -w "%{http_code}\n" -X PUT \
  -H "Authorization: Bearer $PAT" -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/<owner>/<repo>/pages \
  -d '{"source":{"branch":"gh-pages","path":"/"}}'      # 204 = success
```

## 5. Verify live (and beat the CDN)

```bash
curl -s https://<owner>.github.io/<repo>/ | grep -o 'assets/[^"]*'
curl -s -o /dev/null -w "%{http_code}\n" https://<owner>.github.io/<repo>/assets/<file>
```

## Pitfalls

- **Root 200 but assets 404** — the Pages CDN served the *old* `index.html` for
  minutes after the push. Fix: `POST /repos/<o>/<r>/pages/builds` to force a
  rebuild, wait ~60s, re-check. Confirm the `pages` API shows `"status":"built"`
  and branch `gh-pages`. Don't call the deploy broken before a forced rebuild.
- Missing `base` in vite.config → assets resolve to `/assets/...` at domain root.
- Missing `.nojekyll` → paths starting with `_` get dropped.
- JSX text like `Aktif ·\n{expr}` collapses without a space; use `{' '}`.
- If `execute_code` is unavailable in the current profile, use `terminal` +
  `write_file` + `patch` instead; don't stall on it.
- Report honestly which sections you *rewrote* vs. which came from the original
  source when the paste was truncated.
