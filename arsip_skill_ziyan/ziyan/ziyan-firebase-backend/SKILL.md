---
name: ziyan-firebase-backend
description: "ZIYAN Firestore master DB setup + Admin SDK quirks."
version: 1.0.0
author: ZIYAN Orchestrator
license: MIT
platforms: [windows, linux, macos]
---

# ZIYAN Firebase Backend

Firebase/Firestore = master DB ZIYAN (NoSQL) untuk data terstruktur (affiliate products, status
posted, multi-channel). Dikelola penuh Hermes via Firebase Admin SDK (Python), bukan manual
browser. Menggantikan Google Sheets untuk skalabilitas + akses tanpa OAuth tiap kali.

## Kapan pakai
- Butuh penyimpanan terstruktur scalable (ganti Google Sheets).
- Multi-channel / multi-klien (Shopee Affiliate, Threads, YouTube).
- Read/write otomatis dari n8n/Hermes via Service Account (akses penuh, no browser).

## SETUP (sekali)
1. Firebase Console → project (mis. `ziyancorp`) → ⚙️ Project Settings → Service accounts →
   "Generate new private key" → download JSON (ini SA, BUKAN Web API Key tab General).
2. Simpan ke `ziyan_credentials/firebase_admin.json` (JANGAN di-chat).
3. **Enable Firestore API** di GCP + **Create database** di Firebase Console (Native, region
   `asia-southeast2`/Singapore). Enable API ≠ create database — dua langkah beda.
4. venv Hermes rusak `cryptography` → buat venv bersih:
   `uv venv .venv_firebase && uv pip install --python .venv_firebase firebase-admin`

## USAGE (Python Admin SDK)
```python
import firebase_admin
from firebase_admin import credentials, firestore
cred=credentials.Certificate('ziyan_credentials/firebase_admin.json')
app=firebase_admin.initialize_app(cred, name='x', options={'databaseURL':'https://<project>.firebaseio.com'})
db=firestore.client(app=app, database_id='default')  # WAJIB explicit database_id
doc=db.collection('shopee_affiliate').document('id')
doc.set({...}); got=doc.get().to_dict(); doc.delete()
```
Jalankan dengan `.venv_firebase/Scripts/python.exe` (BUKAN `python3` Hermes).

## PITFALL
- `database_id='default'` WAJIB — tanpa itu error 404 "database (default) does not exist".
- Enable API di GCP ≠ Create database di Firebase Console. Dua langkah terpisah.
- venv Hermes (`hermes-agent/venv`) rusak cryptography (`_cffi_backend` missing) → pakai `.venv_firebase`.
- Service Account key = akses penuh (bukan Web API Key tab General = client SDK browser).
- Setelah create database, tunggu ~1 menit propagate sebelum tes write.

## STRUKTUR COLLECTION (Shopee Affiliate)
`shopee_affiliate/{doc}` → link_affiliate, url_foto_asli, kategori(elektronik/fashion),
harga, diskon, caption, posted(bool), timestamp.

## REFERENCES
- `references/setup_quirks.md` — transcript error + fix venv cryptography, database_id, create database.
