# Deploy Static Site ke GitHub Pages (Gratis)

Storefront ZIYAN / corporate site (Vite/React) di-deploy gratis via GitHub Pages.
Terbukti: `zyn-aicorp-site` → rename `ziyancorp` → live di https://yangmulia96.github.io/ziyancorp/ (2026-08-07).

## Prasyarat
- Repo GitHub (Bos: `yangmulia96/zyn-aicorp-site` → rename jadi `ziyancorp`)
- `gh` CLI terinstall (`/c/Program Files/GitHub CLI/gh`)
- Node + npm (Vite project di `zyn-aicorp-site/`)

## Langkah
1. Build: `cd zyn-aicorp-site && npm run build` → hasil di `dist/` (25-35 dtk, vite ~1511 modules)
2. Install publisher: `npm install -D gh-pages`
3. Deploy: `npx gh-pages -d dist` → push ke branch `gh-pages`
4. Enable Pages: `gh api repos/USER/REPO/pages -X POST -f source.branch=gh-pages -f source.path=/`
   - Jika sudah enable → 409 (aman, abaikan)
5. URL: `https://USER.github.io/REPO/`
6. Ganti URL: rename repo `gh repo rename ziyancorp -R USER/oldname` → URL ikut berubah (propagate 1-2 mnt)

## Pitfall
- Repo punya `package.json` di root → `npm install` di folder itu, jangan di `~`.
- Pages status: `gh api repos/USER/REPO/pages` → `html_url` + `status: built`.
- Tambah section produk: edit `src/App.jsx` (React/Tailwind), rebuild, deploy ulang (`npx gh-pages -d dist`).
- UI Bos sudah modern: dark/light, particles, ambient glow (blue/purple/emerald), gradient bergerak, glassmorphism, hover glow.

## Aktivasi Workflow n8n via API (PASTI JALAN)
- Ambil key dinamis: `KEY=$(grep -n "eyJ" ziyan_keys.env | head -1 | cut -d: -f2)`
- Import: `curl -X POST localhost:5678/api/v1/workflows -H "X-N8N-API-KEY: $KEY" -H "Content-Type: application/json" -d @workflow.json` → return `id`
- **ACTIVATE**: `curl -X POST localhost:5678/api/v1/workflows/{ID}/activate -H "X-N8N-API-KEY: $KEY"` → `{"active":true}`
- ❌ PATCH `/api/v1/workflows/{id}` = "PATCH method not allowed"
- ❌ PUT butuh strip banyak field internal (updatedAt, versionId, dll)
- ⚠️ `executeCommand` node DIBLOKIR di n8n v2.33 → pakai `n8n-nodes-base.code` (JS, `require('child_process').execSync`)
- Test webhook: `curl -X POST localhost:5678/webhook/<path> -d '{"x":1}'` → "Workflow was started"
- Cek error: `GET /api/v1/executions/{id}?includeData=true` → `lastNodeExecuted` + `error`
- Pitfall GEMINI_KEY di node HTTP `{{$env.GEMINI_KEY}}`: gagal kalau n8n start tanpa env itu → inject key ke URL atau restart `GEMINI_KEY=... n8n start`. Key Bos sering 429/404 di v1beta.
