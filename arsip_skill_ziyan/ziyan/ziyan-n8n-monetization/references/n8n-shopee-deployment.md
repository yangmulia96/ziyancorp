# n8n Shopee Affiliate — Working Deployment (Windows no-Docker, n8n 2.33.4)

Bukti jalan: post FB Page `975723622288353_122141094105223725` (foto produk + BG AI + caption + link).

## 1. n8n import — REST API (terbukti jalan 2026-08-07, KOREKSI)
Catatan lama "REST /api/v1/* TIDAK enable" SALAH. REST jalan ASALKAN API key diset.
- **Set API key**: insert `settings` key=`security` value=`{"apiKey":"<hex64>"}` (hex random 48 byte). Restart n8n.
- **Import**: `POST http://localhost:5678/api/v1/workflows` header `X-N8N-API-KEY: <key>` + JSON body `{"name","nodes","connections","settings":{}}`. Python `requests.post(json=wf)` lebih andal dari curl `--data-binary` (MSYS sering gagal baca file).
- Balas 401 = key tidak kebaca (restart n8n belum kejar) atau salah header. Balas 200 + `id` = sukses → itu ID FRESH yang 100% valid di instance ini.
- **Activate**: `POST /api/v1/workflows/{id}/activate`.
- JANGAN pakai CLI `n8n import:workflow` (FAIL `SQLITE_CONSTRAINT id NOT NULL` karena node bawa `id` string).
- **Fallback jika REST tetap gagal**: insert langsung SQLite `workflow_entity` (id=UUID, nodes/connections=JSON string STRIP `id` tiap node, settings=`{"executionOrder":"v1"}`, restart n8n).

### "WORKFLOW NOT FOUND" — FALSE ALARM (2026-08-07)
Bos buka `localhost:5678/entity-not-found/workflow` → "Workflow not found". Penyebab: link pakai ID dari DB export/bookmark lama, bukan ID valid instance n8n yang jalan.
- VERIFIKASI: `SELECT id,name FROM workflow_entity` di `C:/Users/arija/.n8n/database.sqlite` → pastikan ID ADA. Cek n8n hidup (`curl /healthz`=200) SEBELUM panggil API (connection refused = n8n mati, bukan API gagal).
- RESOLUSI: export workflow ke JSON dari DB, **import ulang via REST API** (dapat ID baru), atau suruh Bos buka `localhost:5678/workflows` → klik nama. JANGAN berulang kirim link gagal.

## 2. n8n API key + env vars
- API key: insert tabel `user_api_keys` (id=UUID, userId=<user.id dari tabel user>, label, apiKey=sha256(raw), createdAt, updatedAt). Restart n8n.
- Workflow env `{{ $env.FB_PAGE_TOKEN }}`: simpan di tabel `settings` key=`env` sebagai JSON:
  `{"FB_PAGE_TOKEN":"...","HERMES_CUSTOM_9ROUTER_API_KEY":"..."}`. Restart n8n.
- REST `/api/v1/*` TIDAK enable default di 2.33.4 → SQLite insert adalah jalur andal (REST balas "Cannot GET/POST /api/v1/...").

## 3. Restart n8n di Windows
`terminal` tool jalan di bash(MSYS) → `taskkill //F` GAGAL. Pakai:
```bash
PID=$(netstat -ano 2>/dev/null | grep ':5678' | awk '{print $5}' | head -1)
cmd.exe /c "taskkill /F /PID $PID"
# lalu jalankan: n8n start  (background)
```
Boot ~40-60s; cek `curl localhost:5678/healthz` → `{"status":"ok"}`.

## 4. FB Graph posting (single photo — tidak butuh review)
Carousel via `/{page}/media` + `/feed` attached_media → ERROR subcode 33
(fitur butuh app review Meta). Pakai single photo:
```python
requests.post(
  f'https://graph.facebook.com/v19.0/{PAGE_ID}/photos',
  files={'source': ('slide.png', png_bytes, 'image/png')},
  data={'message': caption + '\n🔗 Link: ' + link, 'access_token': PAGE_TOKEN}
)
```
JSON body dengan `url:data:image/png;base64,...` DITOLAK FB
(`url should represent a valid URL`). Multipart file upload = works.
Page token butuh scope `pages_manage_posts` — tambah via FB App →
Products → "Pages" (card "Manage everything on your Page") → regenerate User
Token dengan scope tsb → tukar ke Page token via `GET /me/accounts`.
Test post: `POST /{page}/feed` dengan `message` saja.

## 5. 9router-image (gratis)
- Endpoint `http://127.0.0.1:20128/v1/images/generations`
- Header `Authorization: Bearer $HERMES_CUSTOM_9ROUTER_API_KEY`
- List model: `GET /v1/models/image`
- Model `flux` → 400 "No credentials for provider". Model GRATIS yang jalan:
  `cf/@cf/black-forest-labs/flux-1-schnell` (return `data[0].b64_json`)
- `nb/nanobanana-flash` return URL tapi credit terbatas (429 setelah beberapa call)
- `gemini/*` kena 429 quota
- Payload: `{"model":<free>,"prompt":<txt>,"size":"1024x1024"}`

## 6. Firestore Admin SDK
- Butuh `database_id='default'` eksplisit, else 404 "database does not exist".
- Hermes venv cryptography rusak (`_cffi_backend` missing) →
  `uv venv .venv_firebase && uv pip install firebase-admin`, jalankan dengan
  `.venv_firebase/Scripts/python.exe`.
- Collection affiliate: `shopee_affiliate`, field:
  `link_affiliate, url_foto_asli, kategori, harga, diskon, caption, posted(bool)`.

## 7b. Caption otomatis (9router chat)
Node `AI: Generate Caption` = HTTP Request ke `http://127.0.0.1:20128/v1/chat/completions`:
`{"model":"openrouter/auto","messages":[{"role":"user","content":"Buat caption promo Shopee untuk {{kategori}}, harga Rp{{harga}}, diskon {{diskon}}%. Max 2 kalimat, emoji, ajakan klik link."}],"max_tokens":200}`
Response: `choices[0].message.content`. Disisipkan antara Parse Firestore → Build Prompts.
Bos tidak perlu ketik caption manual di Firestore (cukup link+foto+kategori+harga+diskon).

## 7c. STYLE ke Bos (sinyal 2026-08)
Bos bilang "aku gak paham itu" saat dijelaskan node chain/endpoint. Strategi: lapor ringkas
"apa yang sudah jalan + apa yang harus Bos lakukan" (tabel), sembunyikan detail node ke skill ini.

## 7. PIL composite (Python)
```python
bg = Image.open(b64_or_url).convert('RGBA').resize((1080,1080))
fg = Image.open(url_foto_asli).convert('RGBA')
w = int(1080*0.6); h = int(w*fg.height/fg.width); fg = fg.resize((w,h))
c = bg.copy(); c.paste(fg, ((1080-w)//2,(1080-h)//2), fg)
buf = io.BytesIO(); c.save(buf,'PNG')
b64 = base64.b64encode(buf.getvalue()).decode()
```
