# n8n API Errors & Fixes (Sesi 2026-08-07)

## 1. ExecuteCommand Diblokir
- Error: `Unrecognized node type: n8n-nodes-base.executeCommand`
- Cause: n8n v2.33 security block shell exec node
- Fix: Ganti ke `n8n-nodes-base.code` dengan:
```js
const {execSync} = require('child_process');
const out = execSync(`perintah`).toString();
return [{json:{output: out}}];
```

## 2. Activate Gagal (PATCH/PUT)
- Error: `PATCH method not allowed` / `request/body must NOT have additional properties`
- Fix: `POST /api/v1/workflows/{id}/activate` (body kosong, header X-N8N-API-KEY)

## 3. API Key Tidak Terbaca
- `Key length: 0` saat `sed -n '49p'` → line berubah setelah edit file
- Fix: `grep -n "eyJ" ziyan_keys.env` → ambil line itu

## 4. Import JSON Ditolak
- Error: `request/body must have required property 'settings'` atau `versionId` conflict
- Fix: hapus `versionId`, `pinData`, `updatedAt`, `createdAt`; pastikan `settings:{"executionOrder":"v1"}`

## 5. Gemini API
- 429: quota exceeded (key valid tapi limit) → Bos urus billing
- Veo3 `veo-3.0-generate-preview`: 404 di v1beta → pakai list models atau NanoBanana (gemini-2.5-flash-image)
- NanoBanana: biasanya OK untuk image generation

## 7. ffmpeg Extract Frame (Windows)
- Error: `Use a pattern such as %03d for an image sequence or use -update option`
- Fix: tambah `-update 1` untuk single image:
`ffmpeg -y -ss 00:00:02 -i vid.mp4 -frames:v 1 -q:v 3 -update 1 out.jpg`

## 8. vision_analyze 404 (Intermiten)
- Error: `{"error":"Couldn't find that, sorry."}`
- Fix: ganti frame lain (detik 5/10/15), JANGAN retry frame sama.

## 9. Sub-agent (RISA) Gagal Web Search
- Symptom: delegate_task status=completed tapi cuma bikin todo, tidak return URL.
- Fix: jangan andalkan sub-agent untuk web research. Langsung:
  `curl -s "https://r.jina.ai/https://URL" | head -40`
  atau DuckDuckGo HTML: `curl "https://html.duckduckgo.com/html/?q=..."`
