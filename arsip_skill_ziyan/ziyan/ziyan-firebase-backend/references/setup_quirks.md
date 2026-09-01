# Firebase Setup Quirks — ZIYAN

## Quirk 1: venv Hermes rusak cryptography
Error:
```
ModuleNotFoundError: No module named '_cffi_backend'
  File ".../cryptography/hazmat/bindings/_rust/...
```
Penyebab: venv `hermes-agent/venv` rusak native dep `cffi`/`cryptography`.
Fix (bukan reinstall di venv itu):
```bash
cd "$HOME/AppData/Local/hermes"
uv venv .venv_firebase
uv pip install --python .venv_firebase firebase-admin
# jalankan script dengan:
.venv_firebase/Scripts/python.exe script.py
```
JANGAN pakai `python3` (Hermes) atau `uv run` (pakai venv rusak).

## Quirk 2: database_id wajib explicit
Error:
```
google.api_core.exceptions.NotFound: 404 The database (default) does not exist
for project ziyancorp ... add a Cloud Datastore or Cloud Firestore database.
```
Fix: `firestore.client(app=app, database_id='default')`. Tanpa arg itu SDK cari DB
default tapi gagal kalau belum explicit di client.

## Quirk 3: Enable API ≠ Create Database
- GCP API Library "Firestore API" enable → IZINKAN request tembus (error berubah jadi 404 DB).
- Firebase Console → Firestore → "Create database" (Native mode, region asia-southeast2)
  → BARU instance DB jadi. Console sudah nampil `/firestore/databases/default/data`
  tapi SDK tetap butuh database_id + tunggu ~1 menit propagate.

## Verify (write+read+delete dummy)
```python
doc=db.collection('shopee_affiliate').document('test_ziyan')
doc.set({'link_affiliate':'TEST','kategori':'elektronik','posted':False,'ts':'init'})
print(doc.get().to_dict())
doc.delete()
```
